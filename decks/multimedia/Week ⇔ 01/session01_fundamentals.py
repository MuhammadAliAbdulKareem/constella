# ============================================================================
# Course: Multimedia Systems & Programming
# Session: 01 - Introduction to Python & Core Programming Foundations
# Instructor: Eng. Muhammad Ali Abdul Kareem — Sinai University
# ============================================================================

# ============================================================================
# 1. OUTPUT & INPUT CASTING
# ============================================================================
# print() displays output to the screen
print("Hello, Multimedia Programming!")

# input() returns a string; cast with int() or float() for numerical operations
num_str = "15"
print("Number + 5 =", int(num_str) + 5)

# ============================================================================
# TASK 1: SUM OF TWO NUMBERS
# ============================================================================
a = 15
b = 27
print(f"Task 1: Sum of {a} + {b} = {a + b}")

# ============================================================================
# 2. LISTS (COLLECTIONS)
# ============================================================================
thislist = ["apple", "banana", "cherry"]
print("\nList elements:", thislist)
print("First item:", thislist[0])
print("List size:", len(thislist))

list_mixed = ["abc", 34, True, 40, "male"]
print("Mixed list type:", type(list_mixed))

# ============================================================================
# 3. SELECTION (if / elif / else) & TASK 2
# ============================================================================
# Task 2: Positive / Zero / Negative Classifier
n = 10
if n > 0:
    print(f"\nTask 2: {n} is positive")
elif n == 0:
    print(f"\nTask 2: {n} is zero")
else:
    print(f"\nTask 2: {n} is negative")

# Logical Operators (and, or)
x = 200
y = 33
z = 500
if x > y and z > x:
    print("Both conditions are True (x > y and z > x)")
if x > y or x > z:
    print("At least one condition is True (x > y or x > z)")

# ============================================================================
# 4. REPETITION (for, while, break, continue) & TASK 3
# ============================================================================
# Task 3: Even numbers from 2 to 20 using range(start, stop, step)
print("\nTask 3: Even numbers from 2 to 20:")
for num in range(2, 21, 2):
    print(num, end=" ")
print()

# While loop
print("\nWhile loop count up:")
i = 1
while i < 6:
    print("  i =", i)
    i += 1

# Loop control: break and continue
print("\nLoop with continue (skipping 'banana'):")
fruits = ["apple", "banana", "cherry"]
for item in fruits:
    if item == "banana":
        continue
    print(" ", item)

# Accumulator with continue
total = 0
for k in range(1, 6):
    if k == 3:
        continue
    total += k
print("Total (1 to 5 skipping 3) =", total)

# ============================================================================
# 5. FUNCTIONS & TASK 4
# ============================================================================
def my_function(fname):
    print("Hello " + fname)

my_function("Emil")
my_function("Tobias")

def times_five(val):
    return 5 * val

print("times_five(3) =", times_five(3))

# Task 4: square(x) function
def square(val):
    return val * val

print("\nTask 4: Function square(x):")
print("  square(3) =", square(3))
print("  square(5) =", square(5))
print("  square(8) =", square(8))
