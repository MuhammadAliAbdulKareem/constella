# ============================================================================
# Course: Multimedia Systems & Programming
# Session: 02 - Object-Oriented Programming (OOP) in Python
# Instructor: Eng. Muhammad Ali Abdul Kareem — Sinai University
# ============================================================================

# ============================================================================
# 1. ALGORITHMIC WARM-UP & TASKS
# ============================================================================

# Task 1: Iterative Factorial
def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

print("=== Task 1: Factorial ===")
for test_val in [0, 1, 4, 5]:
    print(f"  {test_val}! = {factorial(test_val)}")

# Task 2: Even / Odd Parity Checker
def check_even_odd(num):
    return "Even" if num % 2 == 0 else "Odd"

print("\n=== Task 2: Even/Odd Checker ===")
for test_num in [12, 17, 0, 99]:
    print(f"  {test_num} is {check_even_odd(test_num)}")

# ============================================================================
# 2. CLASSES & OBJECTS
# ============================================================================
class MyClass:
    # Class attribute (shared by all instances)
    category = "Blueprint Example"
    x = 5

print("\n=== Classes & Objects ===")
p1 = MyClass()
print("  Value of x:", p1.x)
print("  Is p1 an instance of MyClass?", isinstance(p1, MyClass))

# ============================================================================
# 3. CONSTRUCTORS (__init__) & 'self'
# ============================================================================
class Person:
    def __init__(self, name, age):
        # Instance attributes
        self.name = name
        self.age = age

    def myfunc(self):
        print(f"  Hello, my name is {self.name} and I am {self.age} years old.")

    def __str__(self):
        return f"Person({self.name}, {self.age})"

print("\n=== Constructors & Methods ===")
person1 = Person("John", 36)
print(" ", person1)
person1.myfunc()

# ============================================================================
# 4. PILLAR 1: INHERITANCE & super()
# ============================================================================
class Student(Person):
    def __init__(self, name, age, graduation_year):
        super().__init__(name, age)
        self.graduation_year = graduation_year

    def welcome(self):
        print(f"  Welcome {self.name} to class of {self.graduation_year}!")

print("\n=== Inheritance ===")
student1 = Student("Mike Olsen", 22, 2025)
student1.myfunc()
student1.welcome()

# ============================================================================
# 5. PILLAR 2: POLYMORPHISM
# ============================================================================
class Bird:
    def flight(self):
        print("  [Bird] Most birds can fly, but some cannot.")

class Sparrow(Bird):
    def flight(self):
        print("  [Sparrow] Sparrows can fly high.")

class Ostrich(Bird):
    def flight(self):
        print("  [Ostrich] Ostriches cannot fly; they run fast.")

print("\n=== Polymorphism (Uniform Interface) ===")
birds = [Bird(), Sparrow(), Ostrich()]
for b in birds:
    b.flight()

# ============================================================================
# 6. PILLAR 3: ENCAPSULATION & PRIVATE MEMBERS
# ============================================================================
class Base:
    def __init__(self):
        self.a = "Public Member"
        self.__c = "Private Member"  # Private: name-mangled to _Base__c

print("\n=== Encapsulation ===")
base_obj = Base()
print("  Accessing public attribute:", base_obj.a)
# Attempting direct access to base_obj.__c raises AttributeError

# ============================================================================
# 7. OBJECT LIFECYCLE & del KEYWORD
# ============================================================================
class Counter:
    def __init__(self):
        self.count = 10
        self.__secret = 42

print("\n=== Attribute Deletion with del ===")
c = Counter()
print("  Before del: hasattr(c, 'count') =", hasattr(c, "count"))
del c.count
print("  After del:  hasattr(c, 'count') =", hasattr(c, "count"))
