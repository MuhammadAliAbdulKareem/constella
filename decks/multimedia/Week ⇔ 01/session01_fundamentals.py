"""
============================================================================
Course: Multimedia Programming - Python Fundamentals
Session: 01 - Introduction to Python & Core Programming Foundations
Instructor: Muhammad Ali Abdul Kareem
Faculty of IT and CS, Sinai University
============================================================================

Topics Covered:
  1. Standard Output & Input: print(), f-strings, input(), type casting (int, float).
  2. Student Task 1: Sum of two numbers with user input validation.
  3. Variables & Core Data Types: int, float, str, bool, list, tuple, dict, set.
  4. Operators: Arithmetic, relational, logical (and, or, not).
  5. Student Task 2: Conditional branching (if / elif / else - positive/zero/negative).
  6. Loops & Iteration: for loops with range(start, stop, step), while loops.
  7. Student Task 3: Even numbers generator from 2 to 20.
  8. Functions: def, arguments, return values, docstrings.
  9. Student Task 4: square(n) function and temperature converter.
  10. Multimedia Capstone: Pure Python PPM RGB Image Generator (creates an image with 0 dependencies!).

How to run:
  python session01_fundamentals.py
============================================================================
"""

import sys
import os

def print_header(title: str):
    print("\n" + "=" * 64)
    print(f"  {title}")
    print("=" * 64)

def safe_input_int(prompt: str) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print("  [Error] Invalid input. Please enter a valid integer.")

def safe_input_float(prompt: str) -> float:
    while True:
        raw = input(prompt).strip()
        try:
            return float(raw)
        except ValueError:
            print("  [Error] Invalid input. Please enter a valid number.")

# ============================================================================
# 1. OUTPUT, INPUT & TASK 1 (SUM OF TWO NUMBERS)
# ============================================================================
def demo_task1():
    print_header("Output, Input & Task 1: Sum of Two Numbers")
    print("Python input() always returns a string, so explicit casting is required.\n")
    
    num1 = 15
    num2 = 27
    total = num1 + num2
    print(f"  Example: num1 = {num1}, num2 = {num2}")
    print(f"  -> {num1} + {num2} = {total}")

def run_task1_interactive():
    print_header("Interactive Task 1: Calculate Sum")
    a = safe_input_int("Enter first number: ")
    b = safe_input_int("Enter second number: ")
    print(f"\n  Result: {a} + {b} = {a + b}")

# ============================================================================
# 2. DATA TYPES & COLLECTIONS
# ============================================================================
def demo_data_types():
    print_header("Variables & Core Python Data Types")
    
    val_int = 42
    val_float = 3.14159
    val_str = "Sinai University"
    val_bool = True
    val_list = [255, 128, 0]             # Mutable ordered RGB list
    val_tuple = (1920, 1080)            # Immutable Resolution tuple
    val_dict = {"width": 800, "height": 600, "format": "PNG"}  # Key-value map
    val_set = {"red", "green", "blue", "red"} # Unique elements

    print(f"  Integer:     {val_int:<18} (type: {type(val_int).__name__})")
    print(f"  Float:       {val_float:<18} (type: {type(val_float).__name__})")
    print(f"  String:      {val_str:<18} (type: {type(val_str).__name__})")
    print(f"  Boolean:     {str(val_bool):<18} (type: {type(val_bool).__name__})")
    print(f"  RGB List:    {str(val_list):<18} (type: {type(val_list).__name__})")
    print(f"  Res Tuple:   {str(val_tuple):<18} (type: {type(val_tuple).__name__})")
    print(f"  Metadata:    {str(val_dict):<18} (type: {type(val_dict).__name__})")
    print(f"  Color Set:   {str(val_set):<18} (type: {type(val_set).__name__})")

# ============================================================================
# 3. SELECTION & TASK 2 (POSITIVE, ZERO, NEGATIVE)
# ============================================================================
def classify_number(n: float) -> str:
    """Classifies a number as positive, zero, or negative."""
    if n > 0:
        return "Positive (+)"
    elif n < 0:
        return "Negative (-)"
    else:
        return "Zero (0)"

def demo_task2():
    print_header("Selection & Task 2: Positive / Zero / Negative Classifier")
    test_cases = [12.5, -7.0, 0, -0.001, 100]
    for x in test_cases:
        print(f"  Number: {x:>6}  ->  {classify_number(x)}")

# ============================================================================
# 4. REPETITION & TASK 3 (EVEN NUMBERS 2 TO 20)
# ============================================================================
def get_even_numbers(start: int = 2, stop: int = 20) -> list:
    """Generates even numbers in range [start, stop] using range(start, stop + 1, step)."""
    return list(range(start, stop + 1, 2))

def demo_task3():
    print_header("Repetition & Task 3: Even Numbers (2 to 20)")
    evens = get_even_numbers(2, 20)
    print("  Using range(2, 21, 2):")
    print(f"  -> Generated List: {evens}")
    print("  Iterating in for loop:")
    for num in evens:
        print(f"     [+] {num} is even")

# ============================================================================
# 5. FUNCTIONS & TASK 4 (SQUARE FUNCTION)
# ============================================================================
def square(n: float) -> float:
    """Returns the square of a number."""
    return n ** 2

def celsius_to_fahrenheit(c: float) -> float:
    """Converts Celsius temperature to Fahrenheit."""
    return (c * 9 / 5) + 32

def demo_task4():
    print_header("Functions & Task 4: square(n) & Conversions")
    numbers = [2, 3, 5, 8, 12, 15]
    print("  Testing square(n):")
    for n in numbers:
        print(f"    square({n:<2}) = {square(n):<4}")

    print("\n  Testing celsius_to_fahrenheit(c):")
    temps = [0, 20, 37, 100]
    for c in temps:
        print(f"    {c:>3} deg C = {celsius_to_fahrenheit(c):>5.1f} deg F")

# ============================================================================
# 6. MULTIMEDIA CAPSTONE: PURE PYTHON PPM RGB IMAGE GENERATOR
# ============================================================================
def generate_ppm_image(filename: str = "gradient.ppm", width: int = 256, height: int = 256):
    """
    Generates a portable pixel map (PPM) RGB image file using only standard Python.
    No PIL, no OpenCV required! Demonstrates RGB pixel matrix structure in multimedia.
    """
    print_header("Multimedia Capstone: Generating RGB PPM Image")
    print(f"  Rendering {width}x{height} RGB 24-bit gradient into '{filename}'...")
    
    # Netpbm format: P3 means ASCII color text
    with open(filename, "w") as f:
        f.write(f"P3\n{width} {height}\n255\n")
        for y in range(height):
            for x in range(width):
                r = int((x / width) * 255)
                g = int((y / height) * 255)
                b = int(128 + 127 * ((x + y) / (width + height)))
                f.write(f"{r} {g} {b} ")
            f.write("\n")

    size_kb = os.path.getsize(filename) / 1024
    print(f"  [Success] Saved '{filename}' ({size_kb:.1f} KB).")
    print("  Every pixel is an (R, G, B) tuple in a 2D matrix.")

# ============================================================================
# 7. MAIN INTERACTIVE CLI
# ============================================================================
def main():
    print("=" * 64)
    print("  CONSTELLA COURSE PORTAL - MULTIMEDIA PROGRAMMING SESSION 01")
    print("  Python Foundations, Control Flow & Multimedia Principles")
    print("=" * 64)

    while True:
        print("\nSelect an exercise to execute:")
        print("  1. Task 1: Output & Sum of Two Numbers")
        print("  2. Task 1 (Interactive): Enter your own numbers")
        print("  3. Variables & Core Data Types (Collections)")
        print("  4. Task 2: Selection & Number Classifier (Positive/Zero/Negative)")
        print("  5. Task 3: Repetition & Even Numbers Generator (2-20)")
        print("  6. Task 4: Functions (square & Celsius converter)")
        print("  7. Multimedia Capstone: Generate PPM RGB Color Gradient Image")
        print("  8. Run ALL Automated Demos")
        print("  0. Exit")

        choice = safe_input_int("\nEnter choice (0-8): ")

        if choice == 0:
            print("\nGoodbye! Happy Python coding.\n")
            break
        elif choice == 1: demo_task1()
        elif choice == 2: run_task1_interactive()
        elif choice == 3: demo_data_types()
        elif choice == 4: demo_task2()
        elif choice == 5: demo_task3()
        elif choice == 6: demo_task4()
        elif choice == 7: generate_ppm_image()
        elif choice == 8:
            demo_task1()
            demo_data_types()
            demo_task2()
            demo_task3()
            demo_task4()
            generate_ppm_image()
        else:
            print("  [!] Invalid choice. Please select from 0 to 8.")

if __name__ == "__main__":
    main()
