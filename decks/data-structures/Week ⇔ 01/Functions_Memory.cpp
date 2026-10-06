// =============================================================================
// Course: Data Structures with C++
// Session 01: From Structured Programming to Functions & Memory
// Instructor: Eng. Muhammad Ali Abdul Kareem — Sinai University
// =============================================================================

#include <iostream>

using namespace std;

// =============================================================================
// 1. SEQUENCE (Task 1: Rectangle Area & Perimeter)
// =============================================================================
void demoSequence() {
    cout << "=== 1. Sequence: Linear Execution ===" << endl;
    double length = 5.0;
    double width = 3.5;

    double area = length * width;
    double perimeter = 2.0 * (length + width);

    cout << "Length = " << length << ", Width = " << width << endl;
    cout << "Area      = " << area << endl;
    cout << "Perimeter = " << perimeter << endl;

    // Quotient and Remainder
    int num1 = 13, num2 = 5;
    cout << "13 / 5 Quotient  = " << (num1 / num2) << endl;
    cout << "13 % 5 Remainder = " << (num1 % num2) << endl;
}

// =============================================================================
// 2. SELECTION (Task 2: Score Classifier)
// =============================================================================
void demoSelection(int score) {
    cout << "\n=== 2. Selection: Decision Branching ===" << endl;
    cout << "Evaluating Score: " << score << endl;

    char letterGrade;
    if (score >= 90) {
        letterGrade = 'A';
    } else if (score >= 80) {
        letterGrade = 'B';
    } else if (score >= 70) {
        letterGrade = 'C';
    } else {
        letterGrade = 'F';
    }
    cout << "Letter Grade: " << letterGrade << endl;

    // Pass / Fail Check
    if (score < 0 || score > 100) {
        cout << "Status: Invalid Score" << endl;
    } else if (score >= 50) {
        cout << "Status: Passed" << endl;
    } else {
        cout << "Status: Failed" << endl;
    }
}

// =============================================================================
// 3. REPETITION (Task 3: Loops & Factorial)
// =============================================================================
long long computeFactorial(int n) {
    long long fact = 1;
    for (int i = 1; i <= n; ++i) {
        fact *= i;
    }
    return fact;
}

void demoRepetition() {
    cout << "\n=== 3. Repetition: Loops ===" << endl;

    // Odd numbers sum
    int sum = 0;
    for (int i = 1; i <= 5; i += 2) {
        sum += i;
    }
    cout << "Sum of odd numbers (1 + 3 + 5) = " << sum << endl;

    // Factorial calculation
    int n = 5;
    cout << n << "! = " << computeFactorial(n) << endl;
}

// =============================================================================
// 4. FUNCTIONS (Task 4: Temperature Conversion)
// =============================================================================
// Function Prototype
double fahrenheitToCelsius(double fahrenheit);

// Function Definition
double fahrenheitToCelsius(double fahrenheit) {
    // 5.0 / 9.0 avoids integer truncation
    return (fahrenheit - 32.0) * (5.0 / 9.0);
}

void demoFunctions() {
    cout << "\n=== 4. Functions & Prototypes ===" << endl;
    double f = 98.6;
    cout << f << " deg F = " << fahrenheitToCelsius(f) << " deg C" << endl;
}

// =============================================================================
// 5. PARAMETER PASSING: VALUE VS REFERENCE (Task 5: Swap)
// =============================================================================
void modifyValue(int x) {
    x = x + 100; // Operates on a local copy
}

void modifyReference(int& y) {
    y = y + 100; // Operates directly on caller's variable
}

// Task 5: Swap using references
void swapNumbers(int& x, int& y) {
    int temp = x;
    x = y;
    y = temp;
}

void demoParameterPassing() {
    cout << "\n=== 5. Value vs Reference & Swap ===" << endl;

    int a = 10, b = 10;
    modifyValue(a);
    modifyReference(b);
    cout << "modifyValue(10)     -> " << a << " (Unchanged - Pass by Value)" << endl;
    cout << "modifyReference(10) -> " << b << " (Modified  - Pass by Reference)" << endl;

    int x = 12, y = 45;
    cout << "Before swap: x = " << x << ", y = " << y << endl;
    swapNumbers(x, y);
    cout << "After swap:  x = " << x << ", y = " << y << endl;
}

// =============================================================================
// 6. INTEGRATED PROBLEM (isEven & processNumbers)
// =============================================================================
bool isEven(int n) {
    return (n % 2 == 0);
}

void processNumbers(int limit, int& runningSum) {
    for (int i = 1; i <= limit; ++i) {
        if (isEven(i)) {
            runningSum += i;
        }
    }
}

int main() {
    demoSequence();
    demoSelection(85);
    demoRepetition();
    demoFunctions();
    demoParameterPassing();

    cout << "\n=== 6. Integrated Helper & Accumulator ===" << endl;
    int totalSum = 0;
    processNumbers(4, totalSum);
    cout << "Final Total Sum of evens up to 4 = " << totalSum << endl;

    return 0;
}
