"""
============================================================================
Course: Multimedia Systems & Programming
Session: 03 - Digital Sound: Synthesis, Sampling, Quantization & DAC
Instructor: Muhammad Ali Abdul Kareem
Faculty of IT and CS, Sinai University
============================================================================

Topics Covered:
  1. Analog Signal Simulation: Continuous-time Sine wave generation.
  2. Loudness & Amplitude Scaling: Applying gain to control volume.
  3. Sampling (ADC Time Discretization):
     - Sampling rate (Fs) in samples per second (Hz).
     - Nyquist-Shannon Theorem: Fs > 2 * f_max to avoid Aliasing.
     - Visualizing Aliasing when Fs <= 2 * f.
  4. Quantization (ADC Amplitude Discretization):
     - Bit depth (B bits) -> 2^B discrete amplitude levels.
     - Snapping continuous voltages into discrete quantization bins.
     - Quantization error and noise.
  5. Digital-to-Analog Reconstruction (DAC):
     - Zero-Order Hold (ZOH) staircase signal reconstruction.
  6. Real Audio Synthesis (.wav Export):
     - Exporting raw PCM audio using standard library 'wave' module.
     - Listening to bit-depth degradation and aliasing effects.

Requirements:
  pip install numpy matplotlib

How to run:
  python session03_digital_sound.py
============================================================================
"""

import math
import struct
import wave
import sys
import os

try:
    import numpy as np
    import matplotlib.pyplot as plt
    HAS_NUMPY_MPL = True
except ImportError:
    HAS_NUMPY_MPL = False


def print_header(title: str):
    print("\n" + "=" * 68)
    print(f"  {title}")
    print("=" * 68)


def check_dependencies():
    if not HAS_NUMPY_MPL:
        print("\n[Notice] 'numpy' and 'matplotlib' are recommended to display graphs.")
        print("Install them via:")
        print("    pip install numpy matplotlib\n")


# ============================================================================
# 1. SINE WAVE GENERATION (THE ANALOG SIGNAL SIMULATION)
# ============================================================================
def demo_sine_wave(freq: float = 5.0, duration: float = 1.0, show_plot: bool = True):
    """
    Generates a dense sine wave representing a continuous analog audio tone.
    Formula: y(t) = A * sin(2 * pi * f * t)
    """
    print_header("Step 1 · Analog Signal Simulation: Sine Wave")
    print(f"Signal Frequency (f) : {freq} Hz (cycles per second)")
    print(f"Duration             : {duration} second(s)")
    print("Dense time vector (500 pts) acts as continuous analog time.\n")

    if not HAS_NUMPY_MPL:
        # Fallback pure python print
        times = [i * 0.05 for i in range(11)]
        for t in times:
            val = math.sin(2 * math.pi * freq * t)
            bar = "#" * int((val + 1) * 15)
            print(f"  t = {t:.2f}s | {val:+.3f} | {bar}")
        return None, None

    t = np.linspace(0, duration, int(500 * duration), endpoint=False)
    sine = np.sin(2 * np.pi * freq * t)

    if show_plot:
        plt.figure(figsize=(9, 4))
        plt.plot(t, sine, label=f"Analog Sine ({freq} Hz)", color='#a855f7', lw=2)
        plt.axhline(0, color='#6b7280', linestyle='--', alpha=0.5)
        plt.title(f"Continuous Analog Tone: {freq} Hz", fontsize=13, fontweight='bold')
        plt.xlabel("Time (seconds)")
        plt.ylabel("Amplitude")
        plt.grid(True, alpha=0.3)
        plt.legend(loc="upper right")
        plt.tight_layout()
        plt.show()

    return t, sine


# ============================================================================
# 2. LOUDNESS / GAIN CONTROL
# ============================================================================
def demo_gain(freq: float = 5.0, gain: float = 2.0, show_plot: bool = True):
    """
    Demonstrates audio volume / loudness adjustment by multiplying signal by gain.
    gain > 1.0 -> amplification (louder)
    gain < 1.0 -> attenuation (quieter)
    """
    print_header(f"Step 2 · Loudness Adjustment (Gain = {gain}x)")
    print(f"Original signal multiplied by scalar {gain}.")
    print(f"Peak amplitude changes from 1.0 to {1.0 * gain:.2f}.\n")

    if not HAS_NUMPY_MPL:
        print(f"  Max peak is now: {1.0 * gain}")
        return

    t = np.linspace(0, 1.0, 500, endpoint=False)
    original = np.sin(2 * np.pi * freq * t)
    scaled = original * gain

    if show_plot:
        plt.figure(figsize=(9, 4))
        plt.plot(t, original, label="Original Wave (Gain = 1.0)", color='#3b82f6', lw=1.8, linestyle='--')
        plt.plot(t, scaled, label=f"Amplified Wave (Gain = {gain})", color='#ec4899', lw=2.2)
        plt.axhline(0, color='#6b7280', linestyle='--', alpha=0.4)
        plt.title(f"Gain Effect on Signal Loudness (Gain = {gain})", fontsize=13, fontweight='bold')
        plt.xlabel("Time (seconds)")
        plt.ylabel("Amplitude")
        plt.grid(True, alpha=0.3)
        plt.legend(loc="upper right")
        plt.tight_layout()
        plt.show()


# ============================================================================
# 3. SAMPLING & NYQUIST THEOREM (TIME DISCRETIZATION)
# ============================================================================
def demo_sampling(freq: float = 5.0, fs: float = 25.0, show_plot: bool = True):
    """
    Demonstrates time sampling: capturing Fs samples per second.
    Nyquist Rate = 2 * freq.
    If Fs > 2 * freq: Signal is accurately captured.
    If Fs <= 2 * freq: Aliasing occurs (false frequencies appear).
    """
    nyquist_rate = 2 * freq
    is_safe = fs > nyquist_rate

    print_header(f"Step 3 · Sampling & Nyquist Criterion (Fs = {fs} Hz)")
    print(f"  Signal Frequency (f) : {freq} Hz")
    print(f"  Sampling Rate (Fs)   : {fs} Hz (samples per second)")
    print(f"  Nyquist Frequency    : 2 * {freq} = {nyquist_rate} Hz")
    if is_safe:
        print(f"  [STATUS: SAFE] Fs ({fs} Hz) > {nyquist_rate} Hz -> Accurate capture, no aliasing.")
    else:
        print(f"  [STATUS: ALIASING!] Fs ({fs} Hz) <= {nyquist_rate} Hz -> Signal will alias to a wrong frequency!")

    if not HAS_NUMPY_MPL:
        return

    t_dense = np.linspace(0, 1.0, 500, endpoint=False)
    y_dense = np.sin(2 * np.pi * freq * t_dense)

    t_sample = np.linspace(0, 1.0, int(fs), endpoint=False)
    y_sample = np.sin(2 * np.pi * freq * t_sample)

    if show_plot:
        plt.figure(figsize=(9, 4.5))
        plt.plot(t_dense, y_dense, label="Original Analog Wave", color='#94a3b8', lw=1.5, alpha=0.7)
        markerline, stemlines, baseline = plt.stem(
            t_sample, y_sample,
            linefmt='#06b6d4', markerfmt='o', basefmt=' '
        )
        plt.setp(markerline, markersize=5, color='#0891b2')
        status = "SAFE (No Aliasing)" if is_safe else "DANGER (Aliasing Occurs!)"
        plt.title(f"Sampling: Fs = {fs} Hz for f = {freq} Hz [{status}]", fontsize=13, fontweight='bold')
        plt.xlabel("Time (seconds)")
        plt.ylabel("Sample Amplitude")
        plt.grid(True, alpha=0.3)
        plt.legend(loc="upper right")
        plt.tight_layout()
        plt.show()

    return t_sample, y_sample


# ============================================================================
# 4. QUANTIZATION (AMPLITUDE DISCRETIZATION)
# ============================================================================
def demo_quantization(bits: int = 3, freq: float = 5.0, fs: float = 40.0, show_plot: bool = True):
    """
    Demonstrates uniform quantization mapping continuous values [-1, 1]
    into 2^bits discrete levels.
    """
    levels = 2 ** bits
    step_size = 2.0 / (levels - 1)

    print_header(f"Step 4 · Quantization ({bits} Bits = {levels} Discrete Levels)")
    print(f"  Bit Depth (B)      : {bits} bits")
    print(f"  Total Levels (2^B) : {levels}")
    print(f"  Quantization Step  : {step_size:.4f} amplitude units\n")

    if not HAS_NUMPY_MPL:
        return

    t_sample = np.linspace(0, 1.0, int(fs), endpoint=False)
    raw_samples = np.sin(2 * np.pi * freq * t_sample)

    # Normalize [-1, 1] to [0, levels - 1]
    norm = (raw_samples + 1.0) / 2.0 * (levels - 1)
    quantized_indices = np.round(norm)
    quantized_samples = (quantized_indices / (levels - 1)) * 2.0 - 1.0

    quant_error = raw_samples - quantized_samples
    max_error = np.max(np.abs(quant_error))
    print(f"  Maximum Quantization Error: {max_error:.4f} (Max theoretical: {step_size / 2:.4f})")

    if show_plot:
        plt.figure(figsize=(9, 4.5))
        plt.plot(t_sample, raw_samples, label="Sampled Analog Points", color='#94a3b8', linestyle=':', lw=1.5)
        markerline, stemlines, _ = plt.stem(
            t_sample, quantized_samples,
            linefmt='#10b981', markerfmt='s', basefmt=' '
        )
        plt.setp(markerline, markersize=5, color='#059669')
        plt.title(f"Quantization with {bits} Bits ({levels} Levels)", fontsize=13, fontweight='bold')
        plt.xlabel("Time (seconds)")
        plt.ylabel("Quantized Amplitude")
        plt.grid(True, alpha=0.3)
        plt.legend(loc="upper right")
        plt.tight_layout()
        plt.show()

    return quantized_samples


# ============================================================================
# 5. DIGITAL TO ANALOG CONVERTER (DAC) - ZERO ORDER HOLD
# ============================================================================
def demo_dac(bits: int = 3, freq: float = 5.0, fs: float = 30.0, show_plot: bool = True):
    """
    Demonstrates DAC Zero-Order Hold (ZOH) reconstruction.
    The converter holds each quantized sample until the next clock cycle.
    """
    print_header(f"Step 5 · DAC Reconstruction (Zero-Order Hold, {bits} Bits)")
    print("A Zero-Order Hold holds voltage constant between sample intervals,")
    print("producing a characteristic staircase waveform before smoothing filters.\n")

    if not HAS_NUMPY_MPL:
        return

    t_dense = np.linspace(0, 1.0, 500, endpoint=False)
    sine_dense = np.sin(2 * np.pi * freq * t_dense)

    levels = 2 ** bits
    t_sample = np.linspace(0, 1.0, int(fs), endpoint=False)
    raw = np.sin(2 * np.pi * freq * t_sample)
    norm = (raw + 1.0) / 2.0 * (levels - 1)
    quantized = (np.round(norm) / (levels - 1)) * 2.0 - 1.0

    if show_plot:
        plt.figure(figsize=(10, 4.5))
        plt.plot(t_dense, sine_dense, label="Original Analog Signal", color='#94a3b8', linestyle='--', lw=1.5)
        plt.step(t_sample, quantized, where='post', label=f"DAC Output (ZOH, {bits} Bits)", color='#f59e0b', lw=2)
        plt.title(f"DAC Zero-Order Hold Reconstruction (Fs = {fs} Hz, {bits}-bit)", fontsize=13, fontweight='bold')
        plt.xlabel("Time (seconds)")
        plt.ylabel("Output Voltage / Amplitude")
        plt.grid(True, alpha=0.3)
        plt.legend(loc="upper right")
        plt.tight_layout()
        plt.show()


# ============================================================================
# 6. WAV AUDIO GENERATION (LISTEN TO REAL SOUND WITH ZERO DEPENDENCIES)
# ============================================================================
def export_wav(filename: str, freq: float = 440.0, duration: float = 2.0, sample_rate: int = 44100, bit_depth: int = 16):
    """
    Generates a real playable .wav file using Python's standard 'wave' module.
    freq = 440 Hz is concert pitch A4.
    """
    print_header(f"Audio Synthesis · Generating '{filename}'")
    print(f"  Tone Frequency : {freq} Hz (Concert A4 = 440 Hz)")
    print(f"  Duration       : {duration} seconds")
    print(f"  Sample Rate    : {sample_rate} Hz (CD Quality = 44.1 kHz)")
    print(f"  Bit Depth      : {bit_depth}-bit PCM\n")

    total_samples = int(sample_rate * duration)
    max_amplitude = (2 ** (bit_depth - 1)) - 1

    with wave.open(filename, 'wb') as wav_file:
        wav_file.setnchannels(1)      # Mono
        wav_file.setsampwidth(2)      # 16-bit = 2 bytes per sample
        wav_file.setframerate(sample_rate)

        frames = bytearray()
        for i in range(total_samples):
            t = i / sample_rate
            sample_val = math.sin(2 * math.pi * freq * t)
            int_val = int(sample_val * max_amplitude)
            # Pack as signed 16-bit little-endian integer (<h)
            frames.extend(struct.pack('<h', max(-32768, min(32767, int_val))))

        wav_file.writeframes(frames)

    file_size_kb = os.path.getsize(filename) / 1024
    print(f"  [SUCCESS] File written: {filename} ({file_size_kb:.1f} KB)")
    print("  You can now open this .wav file in any media player or browser!\n")


# ============================================================================
# 7. INTERACTIVE MENU
# ============================================================================
def interactive_menu():
    check_dependencies()
    while True:
        print_header("Multimedia Session 03 — Digital Sound Interactive Lab")
        print("  1. Demo 1: Continuous Sine Wave (Analog Signal)")
        print("  2. Demo 2: Loudness & Gain Control")
        print("  3. Demo 3: Sampling & Nyquist Theorem (Safe vs Aliasing)")
        print("  4. Demo 4: Quantization (1-bit vs 3-bit vs 8-bit)")
        print("  5. Demo 5: DAC Zero-Order Hold Reconstruction")
        print("  6. Audio Export: Create Playable .WAV Audio File (A4 440Hz)")
        print("  7. Run All Demos Sequentially")
        print("  0. Exit")
        print("-" * 68)

        choice = input("Enter choice [0-7]: ").strip()
        if choice == '0':
            print("\nExiting. Happy Coding!\n")
            break
        elif choice == '1':
            demo_sine_wave(freq=5.0)
        elif choice == '2':
            demo_gain(freq=5.0, gain=2.0)
        elif choice == '3':
            print("\nComparing Safe Sampling vs Aliasing:")
            print("--- Run A: Safe Sampling (Fs = 30 Hz for 5 Hz wave) ---")
            demo_sampling(freq=5.0, fs=30.0)
            print("--- Run B: Undersampled / Aliased (Fs = 7 Hz for 5 Hz wave) ---")
            demo_sampling(freq=5.0, fs=7.0)
        elif choice == '4':
            print("\nComparing Bit Depths:")
            print("--- Run A: 1-Bit Quantization (2 levels) ---")
            demo_quantization(bits=1, freq=5.0, fs=40.0)
            print("--- Run B: 3-Bit Quantization (8 levels) ---")
            demo_quantization(bits=3, freq=5.0, fs=40.0)
            print("--- Run C: 8-Bit Quantization (256 levels) ---")
            demo_quantization(bits=8, freq=5.0, fs=40.0)
        elif choice == '5':
            demo_dac(bits=3, freq=5.0, fs=30.0)
        elif choice == '6':
            out_name = "sine_440hz.wav"
            export_wav(out_name, freq=440.0, duration=2.5, sample_rate=44100)
        elif choice == '7':
            demo_sine_wave(freq=5.0)
            demo_gain(freq=5.0, gain=2.0)
            demo_sampling(freq=5.0, fs=30.0)
            demo_sampling(freq=5.0, fs=7.0)
            demo_quantization(bits=3, freq=5.0, fs=40.0)
            demo_dac(bits=3, freq=5.0, fs=30.0)
            export_wav("sine_440hz.wav", freq=440.0, duration=1.5)
        else:
            print("[Warning] Invalid choice. Please enter a number from 0 to 7.")


if __name__ == "__main__":
    interactive_menu()
