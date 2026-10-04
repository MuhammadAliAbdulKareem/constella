"""
============================================================================
Course: Multimedia Programming - Python
Session: 02 - Object-Oriented Programming (OOP) in Python
Instructor: Muhammad Ali Abdul Kareem
Faculty of IT and CS, Sinai University
============================================================================

Topics Covered:
  1. Algorithmic Warm-up: Iterative Factorial & Interactive Parity Checker.
  2. Classes & Objects: Class definition, instantiation, and isinstance().
  3. Constructors & 'self': __init__(), instance attributes vs class attributes.
  4. Object Lifecycle: Modifying attributes and deleting properties with 'del'.
  5. Pillar 1 - Inheritance: Base class, derived class, super().__init__().
  6. Pillar 2 - Polymorphism: Unified interface and method overriding.
  7. Pillar 3 - Encapsulation: Private members with double underscore (__), getters & setters.
  8. Multimedia Architecture: Real-world MediaAsset, AudioTrack, VideoClip, and ImageLayer hierarchy.

How to run:
  python session02_oop.py
============================================================================
"""

import math
from typing import List

def print_header(title: str):
    print("\n" + "=" * 64)
    print(f"  {title}")
    print("=" * 64)

# ============================================================================
# 1. WARM-UP ALGORITHMIC FUNCTIONS
# ============================================================================
def factorial_iterative(n: int) -> int:
    """Calculates n! using an iterative loop."""
    if n < 0:
        raise ValueError("Factorial is not defined for negative integers.")
    res = 1
    for i in range(1, n + 1):
        res *= i
    return res

def check_even_odd(n: int) -> str:
    """Checks whether a number is Even or Odd."""
    return "Even" if n % 2 == 0 else "Odd"

def demo_warmup():
    print_header("Algorithmic Warm-up: Factorials & Parity")
    print("Factorial calculations:")
    for i in range(6):
        print(f"  {i}! = {factorial_iterative(i)}")
    
    print("\nParity check:")
    for num in [12, 17, 0, 99]:
        print(f"  {num} is {check_even_odd(num)}")

# ============================================================================
# 2. CLASS DEFINITION & OBJECT INSTANTIATION
# ============================================================================
class MyClass:
    """Simple class demonstration."""
    x = 5  # Class-level attribute

def demo_classes_objects():
    print_header("Classes & Objects: Blueprints and Instances")
    p1 = MyClass()
    print(f"  Instantiated p1 of type: {type(p1).__name__}")
    print(f"  Accessing p1.x: {p1.x}")
    print(f"  isinstance(p1, MyClass): {isinstance(p1, MyClass)}")

# ============================================================================
# 3. CONSTRUCTORS (__init__) & THE 'self' PARAMETER
# ============================================================================
class Person:
    """Represents a person with name and age."""
    species = "Homo sapiens"  # Class attribute (shared by all instances)

    def __init__(self, name: str, age: int):
        self.name = name  # Instance attribute
        self.age = age    # Instance attribute

    def introduce(self):
        print(f"  Hello, my name is {self.name} and I am {self.age} years old.")

    def __str__(self):
        return f"Person(name='{self.name}', age={self.age})"

def demo_constructor():
    print_header("Constructors (__init__) & self")
    john = Person("John Doe", 36)
    alice = Person("Alice Smith", 22)
    
    john.introduce()
    alice.introduce()
    print(f"  String representation: {john}")

# ============================================================================
# 4. MODIFYING & DELETING PROPERTIES (del)
# ============================================================================
def demo_properties_lifecycle():
    print_header("Object Lifecycle: Mutating & Deleting Attributes (del)")
    p = Person("Kareem", 25)
    print(f"  Initial age: {p.age}")
    
    # Modify property
    p.age = 40
    print(f"  Modified age: {p.age}")

    # Delete property
    print("  Deleting 'age' property using 'del p.age'...")
    del p.age
    
    has_age = hasattr(p, 'age')
    print(f"  Does p have 'age' now? {has_age}")

# ============================================================================
# 5. PILLAR 1: INHERITANCE & super()
# ============================================================================
class Student(Person):
    """Derived class inheriting from Person base class."""
    def __init__(self, name: str, age: int, graduation_year: int, major: str):
        # Call base class constructor
        super().__init__(name, age)
        self.graduation_year = graduation_year
        self.major = major

    def introduce(self):
        # Extend parent behavior
        super().introduce()
        print(f"  -> I am majoring in {self.major}, graduating class of {self.graduation_year}.")

def demo_inheritance():
    print_header("Pillar 1: Inheritance & super()")
    s = Student("Sara Ahmed", 20, 2027, "Computer Science & Multimedia")
    s.introduce()
    print(f"  isinstance(s, Student): {isinstance(s, Student)}")
    print(f"  isinstance(s, Person):  {isinstance(s, Person)}")

# ============================================================================
# 6. PILLAR 2: POLYMORPHISM & METHOD OVERRIDING
# ============================================================================
class Bird:
    def __init__(self, species_name: str):
        self.species_name = species_name

    def flight(self):
        print(f"  [{self.species_name}] Flying freely high in the sky.")

class Sparrow(Bird):
    def __init__(self):
        super().__init__("Sparrow")

class Ostrich(Bird):
    def __init__(self):
        super().__init__("Ostrich")

    # Method Overriding: Changing parent behavior
    def flight(self):
        print(f"  [{self.species_name}] Cannot fly. Runs rapidly across the ground!")

def demo_polymorphism():
    print_header("Pillar 2: Polymorphism (Unified Interface)")
    flock: List[Bird] = [Sparrow(), Ostrich(), Sparrow()]

    print("  Iterating through heterogeneous list of birds:")
    for bird in flock:
        bird.flight()  # Same method call behaves polymorphically!

# ============================================================================
# 7. PILLAR 3: ENCAPSULATION & PRIVATE MEMBERS
# ============================================================================
class BankAccount:
    """Demonstrates data protection with private attributes."""
    def __init__(self, owner: str, initial_balance: float):
        self.owner = owner
        self.__balance = max(0.0, initial_balance)  # Private attribute: starts with double underscore

    def deposit(self, amount: float):
        if amount > 0:
            self.__balance += amount
            print(f"  [Deposit] Added ${amount:.2f}. New Balance: ${self.__balance:.2f}")

    def withdraw(self, amount: float) -> bool:
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            print(f"  [Withdraw] Withdrew ${amount:.2f}. Remaining: ${self.__balance:.2f}")
            return True
        print(f"  [Denied] Insufficient funds for withdrawal of ${amount:.2f}")
        return False

    @property
    def balance(self) -> float:
        """Controlled getter property."""
        return self.__balance

def demo_encapsulation():
    print_header("Pillar 3: Encapsulation & Data Hiding")
    acc = BankAccount("Ali", 500.0)
    print(f"  Account owner: {acc.owner}")
    print(f"  Reading balance via property: ${acc.balance:.2f}")

    acc.deposit(150.0)
    acc.withdraw(200.0)

    print("\n  Trying to access private attribute 'acc.__balance' directly:")
    try:
        val = getattr(acc, '__balance')
    except AttributeError:
        print("  -> AttributeError: 'BankAccount' object has no attribute '__balance' (Protected by name mangling!)")

# ============================================================================
# 8. MULTIMEDIA DOMAIN MODEL: ASSET HIERARCHY
# ============================================================================
class MediaAsset:
    """Base class for all digital multimedia elements."""
    def __init__(self, title: str, file_path: str, size_bytes: int):
        self.title = title
        self.file_path = file_path
        self._size_bytes = size_bytes  # Protected member

    def render_info(self):
        print(f"  [Asset] '{self.title}' ({self._size_bytes / (1024*1024):.2f} MB)")

    def play(self):
        raise NotImplementedError("Subclasses must implement play()")

class AudioTrack(MediaAsset):
    def __init__(self, title: str, file_path: str, size_bytes: int, duration_sec: int, bitrate_kbps: int = 320):
        super().__init__(title, file_path, size_bytes)
        self.duration_sec = duration_sec
        self.bitrate_kbps = bitrate_kbps

    def play(self):
        print(f"  [Playing Audio] '{self.title}' -> Duration: {self.duration_sec}s @ {self.bitrate_kbps} kbps")

class VideoClip(MediaAsset):
    def __init__(self, title: str, file_path: str, size_bytes: int, width: int, height: int, fps: float = 60.0):
        super().__init__(title, file_path, size_bytes)
        self.resolution = (width, height)
        self.fps = fps

    def play(self):
        print(f"  [Streaming Video] '{self.title}' -> {self.resolution[0]}x{self.resolution[1]} @ {self.fps} fps")

def demo_multimedia_hierarchy():
    print_header("Multimedia Project: Digital Asset Hierarchy")
    assets: List[MediaAsset] = [
        AudioTrack("Background Theme", "audio/theme.mp3", 4_500_000, duration_sec=142),
        VideoClip("Intro Sequence", "video/intro.mp4", 45_000_000, width=1920, height=1080, fps=60.0),
        AudioTrack("Click SFX", "audio/sfx.wav", 150_000, duration_sec=1)
    ]

    print("  Playing all playlist assets via polymorphism:")
    for item in assets:
        item.render_info()
        item.play()

# ============================================================================
# 9. MAIN INTERACTIVE CLI
# ============================================================================
def main():
    print("=" * 64)
    print("  CONSTELLA COURSE PORTAL - MULTIMEDIA PROGRAMMING SESSION 02")
    print("  Object-Oriented Programming (OOP) in Python")
    print("=" * 64)

    while True:
        print("\nSelect a demonstration to run:")
        print("  1. Algorithmic Warm-up (Factorial & Parity)")
        print("  2. Classes & Object Instantiation (MyClass)")
        print("  3. Constructors (__init__) & self (Person)")
        print("  4. Modifying & Deleting Properties (del)")
        print("  5. Pillar 1: Inheritance & super() (Student)")
        print("  6. Pillar 2: Polymorphism & Method Overriding (Bird, Sparrow, Ostrich)")
        print("  7. Pillar 3: Encapsulation & Private Members (BankAccount)")
        print("  8. Real-world Multimedia Hierarchy (MediaAsset, AudioTrack, VideoClip)")
        print("  9. Run ALL Demonstrations")
        print("  0. Exit")

        raw = input("\nEnter choice (0-9): ").strip()
        if not raw.isdigit():
            print("  [!] Please enter a valid number.")
            continue
        choice = int(raw)

        if choice == 0:
            print("\nGoodbye! Master OOP patterns in your projects.\n")
            break
        elif choice == 1: demo_warmup()
        elif choice == 2: demo_classes_objects()
        elif choice == 3: demo_constructor()
        elif choice == 4: demo_properties_lifecycle()
        elif choice == 5: demo_inheritance()
        elif choice == 6: demo_polymorphism()
        elif choice == 7: demo_encapsulation()
        elif choice == 8: demo_multimedia_hierarchy()
        elif choice == 9:
            demo_warmup()
            demo_classes_objects()
            demo_constructor()
            demo_properties_lifecycle()
            demo_inheritance()
            demo_polymorphism()
            demo_encapsulation()
            demo_multimedia_hierarchy()
        else:
            print("  [!] Unknown choice. Please pick 0 to 9.")

if __name__ == "__main__":
    main()
