/**
 * ============================================================================
 * Course: Data Structures with C++
 * Session: 02 - Time Complexity, Big-O Notation & Growth Rates
 * Instructor: Muhammad Ali Abdul Kareem
 * Faculty of IT and CS, Sinai University
 * ============================================================================
 * 
 * Topics Covered:
 *   1. Big-O Complexity Classes: O(1), O(log N), O(N), O(N log N), O(N^2).
 *   2. Trace Tables & Loop Counting: How loop bounds translate to operations.
 *   3. References (&) vs Value: Memory footprint and performance implications.
 *   4. Student Task 6 (Capstone): Filter & Accumulate Multiples with complexity breakdown.
 *   5. High-Resolution Benchmarking: std::chrono timing across orders of magnitude.
 * 
 * How to compile & run:
 *   g++ -std=c++17 -O2 Complexity_BigO.cpp -o session02
 *   ./session02      (Linux/macOS)
 *   session02.exe    (Windows)
 * ============================================================================
 */

#include <iostream>
#include <vector>
#include <iomanip>
#include <chrono>
#include <algorithm>
#include <numeric>
#include <limits>

using namespace std;
using namespace std::chrono;

// ============================================================================
// 1. HELPER & UI UTILITIES
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
        if (cin >> value) return value;
        cout << "  [Error] Invalid input. Please enter an integer.\n";
        cin.clear();
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
    }
}

// ============================================================================
// 2. BIG-O COMPLEXITY DEMONSTRATIONS
// ============================================================================

// 1) O(1) - Constant Time: Operations count does not depend on input size N
int getFirstElement(const vector<int>& arr) {
    if (arr.empty()) return -1;
    return arr[0]; // Exactly 1 memory lookup
}

// 2) O(log N) - Logarithmic Time: Input halved at every step (Binary Search)
int binarySearch(const vector<int>& sortedArr, int target, int& steps) {
    int left = 0;
    int right = static_cast<int>(sortedArr.size()) - 1;
    steps = 0;

    while (left <= right) {
        steps++;
        int mid = left + (right - left) / 2;
        if (sortedArr[mid] == target) return mid;
        if (sortedArr[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}

// 3) O(N) - Linear Time: Operations grow linearly with N
long long sumElements(const vector<int>& arr, int& steps) {
    long long total = 0;
    steps = 0;
    for (int x : arr) {
        steps++;
        total += x;
    }
    return total;
}

// 4) O(N^2) - Quadratic Time: Nested loops (comparing all pairs)
long long countPairsWithSum(const vector<int>& arr, int targetSum, long long& steps) {
    long long count = 0;
    steps = 0;
    int n = static_cast<int>(arr.size());
    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            steps++;
            if (arr[i] + arr[j] == targetSum) {
                count++;
            }
        }
    }
    return count;
}

// ============================================================================
// 3. STUDENT TASK 6 (CAPSTONE): FILTER & ACCUMULATE MULTIPLES
// ============================================================================
/**
 * Task Specification:
 *   Filter numbers in an array that are multiples of K, accumulate their sum,
 *   and count the number of matching elements.
 * 
 * Complexity Analysis:
 *   - Time Complexity: O(N) because we visit each element exactly once.
 *   - Space Complexity: O(1) auxiliary space (using accumulator variables).
 *   - Reference (&): Passing `const vector<int>&` avoids copying O(N) elements!
 */
struct Task6Result {
    long long sum;
    int count;
    int operations;
};

Task6Result filterAndAccumulate(const vector<int>& arr, int K) {
    Task6Result res = { 0, 0, 0 };
    if (K == 0) return res;

    for (int val : arr) {
        res.operations++;
        if (val % K == 0) {
            res.sum += val;
            res.count++;
        }
    }
    return res;
}

void demoTask6() {
    printHeader("Student Task 6: Filter & Accumulate Multiples");
    cout << "Testing array with K = 3:\n";

    vector<int> sample = { 3, 7, 9, 12, 14, 18, 20, 21, 25 };
    cout << "  Input Array: [ ";
    for (int v : sample) cout << v << " ";
    cout << "]\n";

    int K = 3;
    Task6Result res = filterAndAccumulate(sample, K);

    cout << "\nResults for Multiples of " << K << ":\n";
    cout << "  -> Count of multiples = " << res.count << " (3, 9, 12, 18, 21)\n";
    cout << "  -> Sum of multiples   = " << res.sum << "\n";
    cout << "  -> Loop iterations    = " << res.operations << " out of " << sample.size() << " elements\n";
    cout << "  -> Complexity         = O(N) time, O(1) extra space\n";
}

// ============================================================================
// 4. MEMORY & REFERENCES: PASS BY VALUE VS CONST REFERENCE
// ============================================================================
void passByValueDemo(vector<int> copyArr) {
    // A complete deep copy of copyArr was allocated on the heap!
    volatile size_t sz = copyArr.size();
    (void)sz;
}

void passByRefDemo(const vector<int>& refArr) {
    // Only an 8-byte pointer/reference was passed! Zero heap allocation!
    volatile size_t sz = refArr.size();
    (void)sz;
}

void demoReferences() {
    printHeader("Reference (&) vs Value Performance Demonstration");
    const int N = 2'000'000;
    cout << "Creating vector with " << N << " elements (~8 MB of memory)...\n";
    vector<int> largeVector(N, 42);

    // Timing Pass by Value (allocates and copies 8 MB)
    auto t0 = high_resolution_clock::now();
    passByValueDemo(largeVector);
    auto t1 = high_resolution_clock::now();
    double copyTime = duration<double, milli>(t1 - t0).count();

    // Timing Pass by Reference (0 copies)
    auto t2 = high_resolution_clock::now();
    passByRefDemo(largeVector);
    auto t3 = high_resolution_clock::now();
    double refTime = duration<double, milli>(t3 - t2).count();

    cout << "\nBenchmark Results:\n";
    cout << "  -> Pass by Value (Deep Copy): " << fixed << setprecision(3) << copyTime << " ms [Allocates new vector]\n";
    cout << "  -> Pass by const Reference:   " << fixed << setprecision(3) << refTime << " ms [Zero allocations! O(1) passing]\n";
    cout << "  -> Speedup: ~" << (copyTime / (refTime > 0.0001 ? refTime : 0.0001)) << "x faster using &\n";
}

// ============================================================================
// 5. HIGH-RESOLUTION BIG-O BENCHMARK SUITE
// ============================================================================
void runBenchmarkSuite() {
    printHeader("Live Big-O Growth Rates Benchmark");
    cout << "Measuring real CPU time as input size N scales:\n\n";

    vector<int> sizes = { 100, 1000, 5000, 10000, 20000 };

    cout << left << setw(10) << "N"
         << setw(16) << "BinarySearch"
         << setw(16) << "LinearSum"
         << setw(18) << "PairCount (N^2)"
         << "\n";
    cout << string(60, '-') << "\n";

    for (int n : sizes) {
        vector<int> data(n);
        iota(data.begin(), data.end(), 1); // 1, 2, 3, ... n

        // 1) Binary Search O(log N)
        int stepsBS = 0;
        auto t0 = high_resolution_clock::now();
        binarySearch(data, n - 1, stepsBS);
        auto t1 = high_resolution_clock::now();
        double bsTime = duration<double, micro>(t1 - t0).count();

        // 2) Linear Sum O(N)
        int stepsSum = 0;
        auto t2 = high_resolution_clock::now();
        sumElements(data, stepsSum);
        auto t3 = high_resolution_clock::now();
        double sumTime = duration<double, micro>(t3 - t2).count();

        // 3) Quadratic Pairs O(N^2)
        long long stepsPairs = 0;
        auto t4 = high_resolution_clock::now();
        countPairsWithSum(data, n, stepsPairs);
        auto t5 = high_resolution_clock::now();
        double pairTime = duration<double, micro>(t5 - t4).count();

        cout << left << setw(10) << n
             << setw(16) << (to_string(bsTime).substr(0, 5) + " us")
             << setw(16) << (to_string(sumTime).substr(0, 5) + " us")
             << setw(18) << (to_string(pairTime / 1000.0).substr(0, 6) + " ms")
             << "\n";
    }

    cout << "\nObservations:\n";
    cout << "  - Binary Search: Barely changes as N increases from 100 to 20,000.\n";
    cout << "  - Linear Sum: Scales smoothly and directly in proportion to N.\n";
    cout << "  - Quadratic Pairs: Quadruples whenever N is doubled! (Explodes at N=20,000).\n";
}

// ============================================================================
// 6. MAIN MENU
// ============================================================================
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cout << "================================================================\n";
    cout << "  CONSTELLA COURSE PORTAL - DATA STRUCTURES SESSION 02\n";
    cout << "  Time Complexity, Big-O Analysis & Performance in C++\n";
    cout << "================================================================\n";

    while (true) {
        cout << "\nChoose a demonstration to run:\n";
        cout << "  1. Student Task 6 (Capstone: Filter & Accumulate Multiples)\n";
        cout << "  2. Pass by Reference vs Value Benchmark (& vs Copy)\n";
        cout << "  3. Live Big-O Growth Rates Benchmark (O(log N), O(N), O(N^2))\n";
        cout << "  4. Run ALL Demonstrations\n";
        cout << "  0. Exit\n";

        int choice = readInt("\nEnter your choice (0-4): ");

        if (choice == 0) {
            cout << "\nGoodbye! Keep analyzing complexity before writing code.\n\n";
            break;
        }

        switch (choice) {
            case 1: demoTask6(); break;
            case 2: demoReferences(); break;
            case 3: runBenchmarkSuite(); break;
            case 4:
                demoTask6();
                demoReferences();
                runBenchmarkSuite();
                break;
            default:
                cout << "  [!] Unknown option. Please select 0 to 4.\n";
        }
    }

    return 0;
}
