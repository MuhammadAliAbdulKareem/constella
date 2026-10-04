/**
 * ============================================================================
 * Course: Data Structures with C++
 * Session: 01 - From Structured Programming to Functions & Memory
 * Instructor: Muhammad Ali Abdul Kareem
 * Faculty of IT and CS, Sinai University
 * ============================================================================
 * 
 * Topics Covered:
 *   1. Sequence: Linear execution, variable tracing, rectangle area & perimeter (Task 1).
 *   2. Selection: if / else if / else ladders, grade/score validation (Task 2).
 *   3. Repetition: for / while loops, accumulator pattern, factorial calculation (Task 3).
 *   4. Functions: Prototype (declaration), definition, return types, Fahrenheit to Celsius (Task 4).
 *   5. Parameter Passing: Pass by Value vs Pass by Reference (&) vs Pointer (*), swap (Task 5).
 *   6. Memory Layout: Stack frames, call stack lifecycle, local scope vs heap overview.
 * 
 * How to compile & run:
 *   g++ -std=c++17 -O2 Functions_Memory.cpp -o session01
 *   ./session01      (Linux/macOS)
 *   session01.exe    (Windows)
 * ============================================================================
 */

#include <iostream>
#include <iomanip>
#include <string>
#include <limits>

using namespace std;

// ============================================================================
// 1. HELPER FUNCTIONS
// ============================================================================

void printHeader(const string& title) {
    cout << "\n================================================================\n";
    cout << "  " << title << "\n";
    cout << "================================================================\n";
}

int readInt(const string& prompt) {
    int value;
    while (true) {
        cout << prompt;
        if (cin >> value) {
            return value;
        }
        cout << "  [Error] Invalid input. Please enter a valid integer.\n";
        cin.clear();
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
    }
}

double readDouble(const string& prompt) {
    double value;
    while (true) {
        cout << prompt;
        if (cin >> value) {
            return value;
        }
        cout << "  [Error] Invalid input. Please enter a valid number.\n";
        cin.clear();
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
    }
}

// ============================================================================
// 2. PILLAR 1: SEQUENCE (Task 1)
// ============================================================================
// Sequence: Statements execute strictly top-to-bottom, line by line.

struct RectangleResult {
    double area;
    double perimeter;
};

RectangleResult calculateRectangle(double length, double width) {
    RectangleResult res;
    res.area = length * width;
    res.perimeter = 2.0 * (length + width);
    return res;
}

void demoSequence() {
    printHeader("Pillar 1: Sequence & Task 1 (Rectangle)");
    cout << "Calculating Area and Perimeter sequentially:\n\n";

    double length = 5.0;
    double width = 3.5;
    cout << "  Given Length = " << length << ", Width = " << width << "\n";

    RectangleResult res = calculateRectangle(length, width);
    cout << "  -> Area      = length * width       = " << res.area << "\n";
    cout << "  -> Perimeter = 2 * (length + width) = " << res.perimeter << "\n";
}

// ============================================================================
// 3. PILLAR 2: SELECTION (Task 2)
// ============================================================================
// Selection: Decisions branch based on boolean conditions evaluated in order.

string classifyScore(double score) {
    if (score < 0 || score > 100) {
        return "Invalid Score (Must be between 0 and 100)";
    } else if (score >= 50.0) {
        return "Passed";
    } else {
        return "Failed";
    }
}

void demoSelection() {
    printHeader("Pillar 2: Selection & Task 2 (Score Classifier)");
    cout << "Testing sample scores through the conditional ladder:\n\n";

    double testScores[] = { -5.0, 48.0, 50.0, 85.5, 102.0 };
    for (double s : testScores) {
        cout << "  Score: " << setw(5) << s << " -> Result: " << classifyScore(s) << "\n";
    }
}

// ============================================================================
// 4. PILLAR 3: REPETITION (Task 3)
// ============================================================================
// Repetition: Loops repeat a block until a termination condition is met.

long long factorial(int n) {
    if (n < 0) return -1; // Error code for invalid negative input
    long long fact = 1;
    for (int i = 1; i <= n; ++i) {
        fact *= i;
    }
    return fact;
}

long long sumOddNumbers(int limit) {
    long long sum = 0;
    for (int i = 1; i <= limit; i += 2) {
        sum += i;
    }
    return sum;
}

void demoRepetition() {
    printHeader("Pillar 3: Repetition & Task 3 (Factorial & Loops)");
    cout << "Testing iterative Factorial (N!) loop:\n\n";

    for (int n = 0; n <= 7; ++n) {
        cout << "  " << n << "! = " << factorial(n) << "\n";
    }

    cout << "\nSum of odd numbers up to 10:\n";
    cout << "  1 + 3 + 5 + 7 + 9 = " << sumOddNumbers(10) << "\n";
}

// ============================================================================
// 5. FUNCTIONS: DECLARATION, DEFINITION, RETURN VALUE (Task 4)
// ============================================================================
// Function Prototype:
double fahrenheitToCelsius(double fahrenheit);

// Function Definition:
double fahrenheitToCelsius(double fahrenheit) {
    // Formula: (F - 32) * 5 / 9
    return (fahrenheit - 32.0) * (5.0 / 9.0);
}

void demoFunctions() {
    printHeader("Functions & Task 4 (Fahrenheit to Celsius)");
    cout << "Demonstrating Function Prototype, Call & Return:\n\n";

    double fTemps[] = { 32.0, 68.0, 98.6, 212.0 };
    for (double f : fTemps) {
        double c = fahrenheitToCelsius(f);
        cout << "  " << setw(5) << f << " deg F  =  " 
             << fixed << setprecision(2) << setw(6) << c << " deg C\n";
    }
}

// ============================================================================
// 6. PARAMETER PASSING & MEMORY (Task 5)
// ============================================================================
// 1) Pass by Value: Copies the value. Original is UNTOUCHED.
void swapByValue(int a, int b) {
    int temp = a;
    a = b;
    b = temp;
}

// 2) Pass by Reference: Uses alias to caller's variable. Mutates original.
void swapByReference(int& a, int& b) {
    int temp = a;
    a = b;
    b = temp;
}

// 3) Pass by Pointer: Receives memory addresses. Mutates original.
void swapByPointer(int* a, int* b) {
    if (a == nullptr || b == nullptr) return;
    int temp = *a;
    *a = *b;
    *b = temp;
}

void demoParameterPassing() {
    printHeader("Parameter Passing & Task 5 (Swap by Value vs Reference)");

    int x = 10, y = 20;
    cout << "Initial values: x = " << x << " (address: " << &x << "), y = " << y << " (address: " << &y << ")\n\n";

    cout << "1. Calling swapByValue(x, y)...\n";
    swapByValue(x, y);
    cout << "   Result: x = " << x << ", y = " << y << "  -> [UNCHANGED! Value copies were swapped in local frame]\n\n";

    cout << "2. Calling swapByReference(x, y)...\n";
    swapByReference(x, y);
    cout << "   Result: x = " << x << ", y = " << y << "  -> [SWAPPED! References operate directly on x & y]\n\n";

    cout << "3. Calling swapByPointer(&x, &y)...\n";
    swapByPointer(&x, &y);
    cout << "   Result: x = " << x << ", y = " << y << "  -> [SWAPPED BACK! Pointers dereferenced original cells]\n";
}

// ============================================================================
// 7. CALL STACK & RECURSION TRACE
// ============================================================================
int recursivePower(int base, int exp, int depth = 0) {
    string indent(depth * 3, ' ');
    cout << indent << "|-- [Call frame depth " << depth << "] power(" << base << ", " << exp << ") called\n";
    
    if (exp <= 0) {
        cout << indent << "\\-- Base case reached! Returning 1\n";
        return 1;
    }
    
    int subResult = recursivePower(base, exp - 1, depth + 1);
    int myResult = base * subResult;
    cout << indent << "\\-- [Popping frame " << depth << "] Returning " << base << " * " << subResult << " = " << myResult << "\n";
    return myResult;
}

void demoCallStack() {
    printHeader("Call Stack Tracing: Recursive Power (2^4)");
    cout << "Observing stack frame allocation and unwinding:\n\n";
    int ans = recursivePower(2, 4);
    cout << "\nFinal Answer: 2^4 = " << ans << "\n";
}

// ============================================================================
// 8. INTERACTIVE MAIN MENU
// ============================================================================
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cout << "================================================================\n";
    cout << "  CONSTELLA COURSE PORTAL - DATA STRUCTURES SESSION 01\n";
    cout << "  Functions, Memory & Structural Foundations in C++\n";
    cout << "================================================================\n";

    while (true) {
        cout << "\nChoose a demonstration to run:\n";
        cout << "  1. Pillar 1: Sequence & Rectangle Calculator (Task 1)\n";
        cout << "  2. Pillar 2: Selection & Score Ladder (Task 2)\n";
        cout << "  3. Pillar 3: Repetition & Factorial (Task 3)\n";
        cout << "  4. Functions: Fahrenheit to Celsius (Task 4)\n";
        cout << "  5. Parameter Passing: Value vs Reference vs Pointer (Task 5)\n";
        cout << "  6. Call Stack & Recursion Tracing\n";
        cout << "  7. Run ALL Demos\n";
        cout << "  0. Exit\n";

        int choice = readInt("\nEnter your choice (0-7): ");

        if (choice == 0) {
            cout << "\nGoodbye! Keep coding with clean C++ style.\n\n";
            break;
        }

        switch (choice) {
            case 1: demoSequence(); break;
            case 2: demoSelection(); break;
            case 3: demoRepetition(); break;
            case 4: demoFunctions(); break;
            case 5: demoParameterPassing(); break;
            case 6: demoCallStack(); break;
            case 7:
                demoSequence();
                demoSelection();
                demoRepetition();
                demoFunctions();
                demoParameterPassing();
                demoCallStack();
                break;
            default:
                cout << "  [!] Unknown option. Please select 0 to 7.\n";
        }
    }

    return 0;
}
