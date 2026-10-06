// =============================================================================
// Course: Data Structures with C++
// Session: 02 - Time Complexity, Big-O Notation & Growth Rates
// Instructor: Eng. Muhammad Ali Abdul Kareem — Sinai University
// =============================================================================

#include <iostream>
#include <cmath>

using namespace std;

// =============================================================================
// 1. BIG-O COMPLEXITY CLASSES
// =============================================================================

// O(1) - Constant Time: single operation regardless of n
void constantTime(int n) {
    int result = n * n;
    cout << "O(1) Constant Time Result: " << result << endl;
}

// O(log N) - Logarithmic Time: loop variable doubles each iteration
void logTime(int n) {
    int steps = 0;
    for (int i = 1; i < n; i *= 2) {
        steps++;
    }
    cout << "O(log N) Total Steps for n = " << n << ": " << steps << endl;
}

// O(N^0.25) & O(N^(1/3)) - Sub-linear Root Time
void fourthRootTime(int n) {
    int limit = pow(n, 0.25);
    for (int i = 0; i < limit; i++) { }
}

void cubeRootTime(int n) {
    int limit = cbrt(n);
    for (int i = 0; i < limit; i++) { }
}

// O(sqrt(N)) - Square Root Time
void squareRootTime(int n) {
    int limit = sqrt(n);
    cout << "O(sqrt N) Iterations for n = " << n << " (limit = " << limit << "): ";
    for (int i = 0; i < limit; i++) {
        cout << i << " ";
    }
    cout << endl;
}

// O(N) - Linear Time: loop runs proportional to n
void linearTime(int n) {
    cout << "O(N) Linear Time (sample checkpoints for n = " << n << "): ";
    int step = (n / 10 == 0) ? 1 : (n / 10);
    for (int i = 0; i < n; i++) {
        if (i % step == 0) {
            cout << i << " ";
        }
    }
    cout << endl;
}

// O(N log N) - Linearithmic Time: outer loop N, inner loop doubles (log N)
void nLogNTime(int n) {
    int count = 0;
    for (int i = 0; i < n; i++) {
        for (int j = 1; j < n; j *= 2) {
            count++;
        }
    }
    cout << "O(N log N) Operation Count for n = " << n << ": " << count << endl;
}

// O(N^2) - Quadratic Time: nested loops
void quadraticTime(int n) {
    int count = 0;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            count++;
        }
    }
    cout << "O(N^2) Operation Count for n = " << n << ": " << count << endl;
}

// =============================================================================
// 2. STUDENT TASK 6: FILTER & SUM MULTIPLES
// =============================================================================

// Helper function: Checks if a value is divisible by 3 (Selection)
bool isDivisibleByThree(int val) {
    return (val % 3 == 0);
}

// Accumulator function: Filters and accumulates multiples (O(N) Time, O(1) Space)
void filterAndSum(int n, int& matchedCount, long long& sumResult) {
    for (int i = 1; i <= n; ++i) {
        if (isDivisibleByThree(i)) {
            matchedCount++;
            sumResult += i;
        }
    }
}

// =============================================================================
// 3. DRIVER PROGRAM
// =============================================================================
int main() {
    int n = 100;
    cout << "=== Time Complexity Demonstrations (n = " << n << ") ===" << endl;

    constantTime(n);
    logTime(n);
    fourthRootTime(n);
    cubeRootTime(n);
    squareRootTime(n);
    linearTime(n);
    nLogNTime(n);
    quadraticTime(20); // Small n for O(N^2) demo

    cout << "\n=== Student Task 6: Filter & Sum Multiples of 3 ===" << endl;
    int limit = 30;
    int totalMatches = 0;
    long long totalSum = 0;

    filterAndSum(limit, totalMatches, totalSum);

    cout << "Limit n:        " << limit << endl;
    cout << "Matched Count:  " << totalMatches << " (numbers divisible by 3)" << endl;
    cout << "Sum of Matches: " << totalSum << endl;

    return 0;
}
