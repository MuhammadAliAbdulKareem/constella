// =============================================================================
// Course: Data Structures with C++
// Session 05: Sorting & Searching inside the ArrayList Class
// Instructor: Eng. Muhammad Ali Abdul Kareem — Sinai University
// =============================================================================
// Description:
//   In this session, we transition from standalone procedural sorting functions
//   to object-oriented sorting algorithms embedded directly inside the ArrayList.
//   By encapsulating the sorting logic inside the class:
//     1. The object protects its internal state (data pointer, size, capacity).
//     2. Bounds are strictly controlled using 'size' rather than 'capacity'
//        (avoiding dangerous garbage-value comparisons).
//     3. Algorithms share safe internal helper methods like swapAt() and grow().
//
// Algorithms Implemented:
//   - Bubble Sort (with early-exit optimization): Best O(n), Worst O(n^2), Stable
//   - Selection Sort (minimum writes/swaps): Best/Worst O(n^2), Unstable
//   - Insertion Sort (adaptive shift-and-insert): Best O(n), Worst O(n^2), Stable
//   - Ordered Insertion (insertSorted): O(n)
//   - Binary Search (logarithmic lookup on sorted data): O(log n)
//   - Student Task 1: isSorted() verification method: O(n)
//   - Student Task 2: bubbleSortPasses() pass counter with early exit: O(n) - O(n^2)
// =============================================================================

#include <iostream>

using namespace std;

// =============================================================================
// ArrayList Class Definition
// =============================================================================
class ArrayList {
private:
    int* data;      // Pointer to dynamic array allocated on the heap
    int size;       // Number of actual elements currently stored
    int capacity;   // Total available slots allocated in memory

    // Private Helper Methods (Internal mechanics hidden from outside code)
    int  readInt();                 // Robust keyboard input validation
    void swapAt(int i, int j);      // Centralized single-point element exchange
    void grow();                    // Dynamic capacity doubling when array is full

public:
    // Lifecycle Management (Rule of Three)
    ArrayList(int cap = 10);
    ArrayList(const ArrayList& other);             // Deep copy constructor
    ArrayList& operator=(const ArrayList& other);  // Deep copy assignment operator
    ~ArrayList();                                  // Destructor (frees heap memory)

    // --- Core Operations (from Session 03) ---
    void fillFromUser(int n);
    void display() const;
    bool insertAt(int pos, int value);
    bool deleteAt(int pos);
    int  searchByValue(int target) const;
    bool updateAt(int pos, int value);
    void push(int value);

    // --- Sorting & Searching Methods (Session 05) ---
    void bubbleSort();
    void selectionSort();
    void insertionSort();
    bool insertSorted(int value);
    int  binarySearch(int target) const;

    // --- Student Practice Tasks ---
    bool isSorted() const;          // Task 1: Check if elements are in non-decreasing order
    int  bubbleSortPasses();        // Task 2: Count sorting passes until sorted
};

// =============================================================================
// 1. LIFECYCLE MANAGEMENT (Constructors, Destructor, Rule of Three)
// =============================================================================

// Constructor: Allocates initial heap memory
ArrayList::ArrayList(int cap) {
    capacity = (cap > 0) ? cap : 10;
    size = 0;
    data = new int[capacity];
}

// Copy Constructor: Creates an independent deep copy of another ArrayList
ArrayList::ArrayList(const ArrayList& other) {
    capacity = other.capacity;
    size = other.size;
    data = new int[capacity];
    for (int i = 0; i < size; i++) {
        data[i] = other.data[i];
    }
}

// Copy Assignment Operator: Cleans up old buffer, then performs deep copy
ArrayList& ArrayList::operator=(const ArrayList& other) {
    if (this == &other) return *this; // Self-assignment check

    delete[] data;                    // 1. Free existing memory
    capacity = other.capacity;
    size = other.size;
    data = new int[capacity];         // 2. Allocate new buffer
    for (int i = 0; i < size; i++) {   // 3. Copy elements
        data[i] = other.data[i];
    }
    return *this;
}

// Destructor: Returns heap memory back to the operating system
ArrayList::~ArrayList() {
    delete[] data;
    data = nullptr;
}

// =============================================================================
// 2. PRIVATE HELPER METHODS
// =============================================================================

// Safe Integer Reader: Validates user input and rejects invalid non-numeric inputs
int ArrayList::readInt() {
    int x;
    cin >> x;
    while (cin.fail()) {
        cin.clear();            // Step 1: Clear the error state flags on cin
        cin.ignore(1000, '\n'); // Step 2: Discard erroneous input up to newline
        cout << "Invalid input. Please enter an integer: ";
        cin >> x;
    }
    return x;
}

// Centralized Swapper: Swaps values at index i and j safely
void ArrayList::swapAt(int i, int j) {
    int tmp = data[i];
    data[i] = data[j];
    data[j] = tmp;
}

// Dynamic Resizer: Doubles capacity when storage becomes full
void ArrayList::grow() {
    int newCap = (capacity == 0) ? 2 : capacity * 2;
    int* bigger = new int[newCap];
    for (int i = 0; i < size; i++) {
        bigger[i] = data[i];
    }
    delete[] data;
    data = bigger;
    capacity = newCap;
}

// =============================================================================
// 3. CORE ARRAYLIST OPERATIONS
// =============================================================================

// Fill array with n items read securely from the keyboard
void ArrayList::fillFromUser(int n) {
    if (n < 0 || n > capacity - size) {
        cout << "Error: n must be between 0 and remaining capacity (" << (capacity - size) << ")." << endl;
        return;
    }
    for (int i = 0; i < n; i++) {
        cout << "Enter element [" << size << "]: ";
        data[size] = readInt();
        size++;
    }
}

// Print elements in the array with their corresponding indices
void ArrayList::display() const {
    if (size == 0) {
        cout << "[Empty list]" << endl;
        return;
    }
    for (int i = 0; i < size; i++) {
        cout << "Index " << i << " = " << data[i] << endl;
    }
}

// Insert value at arbitrary index (shifts existing elements right)
bool ArrayList::insertAt(int pos, int value) {
    if (pos < 0 || pos > size) return false;
    if (size == capacity) grow();

    for (int i = size; i > pos; i--) {
        data[i] = data[i - 1];
    }
    data[pos] = value;
    size++;
    return true;
}

// Delete value at arbitrary index (shifts remaining elements left)
bool ArrayList::deleteAt(int pos) {
    if (pos < 0 || pos >= size) return false;

    for (int i = pos; i < size - 1; i++) {
        data[i] = data[i + 1];
    }
    size--;
    return true;
}

// Linear search by value: Returns index if found, -1 otherwise. O(n)
int ArrayList::searchByValue(int target) const {
    for (int i = 0; i < size; i++) {
        if (data[i] == target) return i;
    }
    return -1;
}

// Direct element update by index: O(1)
bool ArrayList::updateAt(int pos, int value) {
    if (pos < 0 || pos >= size) return false;
    data[pos] = value;
    return true;
}

// Append value at end of array: Amortized O(1)
void ArrayList::push(int value) {
    if (size == capacity) grow();
    data[size++] = value;
}

// =============================================================================
// 4. ELEMENTARY SORTING ALGORITHMS (SESSION 05)
// =============================================================================

// -----------------------------------------------------------------------------
// Bubble Sort
// -----------------------------------------------------------------------------
// Intuition:
//   Repeatedly steps through the array, compares adjacent elements, and swaps
//   them if they are out of order. After pass i, the largest unsorted element
//   "bubbles up" to its permanent position at index (size - 1 - i).
//
// Optimizations:
//   1. Inner loop bound: (size - 1 - i) avoids re-checking already sorted tail.
//   2. Early exit flag: If an entire pass completes with 0 swaps, array is
//      already sorted, terminating the algorithm early.
//
// Complexity:
//   - Best Case:    O(n)   (when list is already sorted, stops after 1 pass)
//   - Average Case: O(n^2)
//   - Worst Case:   O(n^2) (reverse sorted)
//   - Space:        O(1)   (In-place)
//   - Stability:    STABLE (adjacent equals are never swapped)
// -----------------------------------------------------------------------------
void ArrayList::bubbleSort() {
    for (int i = 0; i < size - 1; i++) {
        bool swapped = false;
        for (int j = 0; j < size - 1 - i; j++) {
            if (data[j] > data[j + 1]) {
                swapAt(j, j + 1);
                swapped = true;
            }
        }
        if (!swapped) break; // Early termination: already sorted
    }
}

// -----------------------------------------------------------------------------
// Selection Sort
// -----------------------------------------------------------------------------
// Intuition:
//   Divides the list into a sorted prefix and an unsorted suffix.
//   In each pass i, it scans the unsorted suffix to find the index of the minimum
//   element, then performs at most ONE swap to put it at index i.
//
// Key Feature:
//   Makes at most (size - 1) swaps total, regardless of input distribution.
//   Ideal for systems where flash memory or write operations are costly.
//
// Complexity:
//   - Best Case:    O(n^2) (must always scan for minimum)
//   - Average Case: O(n^2)
//   - Worst Case:   O(n^2)
//   - Space:        O(1)   (In-place)
//   - Stability:    UNSTABLE (a long-distance swap can jump over an equal key)
// -----------------------------------------------------------------------------
void ArrayList::selectionSort() {
    for (int i = 0; i < size - 1; i++) {
        int minIndex = i;
        for (int j = i + 1; j < size; j++) {
            if (data[j] < data[minIndex]) {
                minIndex = j;
            }
        }
        if (minIndex != i) {
            swapAt(i, minIndex);
        }
    }
}

// -----------------------------------------------------------------------------
// Insertion Sort
// -----------------------------------------------------------------------------
// Intuition:
//   Builds the sorted array one element at a time, analogous to sorting cards
//   in your hand. Takes element data[i] as 'key', shifts all elements in the
//   sorted prefix that are greater than 'key' one position to the right,
//   and places 'key' into the vacated slot.
//
// Key Feature:
//   Highly efficient for small datasets and partially sorted data.
//
// Complexity:
//   - Best Case:    O(n)   (already sorted: while-loop test fails immediately)
//   - Average Case: O(n^2)
//   - Worst Case:   O(n^2) (reverse sorted: full shifts every time)
//   - Space:        O(1)   (In-place)
//   - Stability:    STABLE (strictly greater elements shift; equals remain ordered)
// -----------------------------------------------------------------------------
void ArrayList::insertionSort() {
    for (int i = 1; i < size; i++) {
        int key = data[i];
        int j = i - 1;
        while (j >= 0 && data[j] > key) {
            data[j + 1] = data[j]; // Shift element right
            j--;
        }
        data[j + 1] = key;         // Drop key into vacated slot
    }
}

// =============================================================================
// 5. ORDERED INSERTION & FAST SEARCHING
// =============================================================================

// -----------------------------------------------------------------------------
// insertSorted()
// -----------------------------------------------------------------------------
// Inserts a new value into an already sorted ArrayList while preserving sorted order.
// Shifts larger elements right from the back, then inserts the value.
// Complexity: O(n) shifts. Returns false if capacity is reached.
// -----------------------------------------------------------------------------
bool ArrayList::insertSorted(int value) {
    if (size == capacity) return false; // Rejection when full (bounded per syllabus)

    int j = size - 1;
    while (j >= 0 && data[j] > value) {
        data[j + 1] = data[j];          // Shift right
        j--;
    }
    data[j + 1] = value;
    size++;
    return true;
}

// -----------------------------------------------------------------------------
// Binary Search
// -----------------------------------------------------------------------------
// Precondition: The array MUST be sorted beforehand.
// Algorithm:
//   Repeatedly divides the search interval in half.
//   Compares target with middle element:
//     - If equal: target found at mid.
//     - If target > data[mid]: search upper half (lo = mid + 1).
//     - If target < data[mid]: search lower half (hi = mid - 1).
//
// Complexity:
//   - Best Case:  O(1)
//   - Average:    O(log n)
//   - Worst Case: O(log n)
//   - Space:      O(1)
// -----------------------------------------------------------------------------
int ArrayList::binarySearch(int target) const {
    int lo = 0;
    int hi = size - 1;

    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2; // Safe midpoint calculation
        if (data[mid] == target) return mid;
        if (data[mid] < target)  lo = mid + 1;
        else                     hi = mid - 1;
    }
    return -1; // Not found
}

// =============================================================================
// 6. STUDENT PRACTICE TASKS
// =============================================================================

// -----------------------------------------------------------------------------
// Student Task 1: isSorted()
// -----------------------------------------------------------------------------
// Problem:
//   Verify whether the elements are sorted in non-decreasing order.
//
// Solution Strategy:
//   - A list with 0 or 1 element is inherently sorted (returns true).
//   - Iterate while (i + 1 < size) to safely inspect adjacent pairs.
//   - Early exit: Return false as soon as data[i] > data[i + 1].
//   - Trap to avoid: Looping with (i < size) causes data[i + 1] to read garbage.
// Complexity: O(n) time, O(1) space.
// -----------------------------------------------------------------------------
bool ArrayList::isSorted() const {
    for (int i = 0; i + 1 < size; i++) {
        if (data[i] > data[i + 1]) {
            return false; // Inversion found
        }
    }
    return true; // No inversions: sorted
}

// -----------------------------------------------------------------------------
// Student Task 2: bubbleSortPasses()
// -----------------------------------------------------------------------------
// Problem:
//   Sort the array using Bubble Sort and return the EXACT number of passes executed.
//
// Solution Strategy:
//   - Maintain a 'passes' counter incremented at the start of each outer pass.
//   - Use a 'swapped' flag to detect early completion.
//   - Trap to avoid: A pre-sorted array still requires 1 verification pass (returns 1).
// Complexity: Best O(n) (1 pass), Worst O(n^2) (size - 1 passes).
// -----------------------------------------------------------------------------
int ArrayList::bubbleSortPasses() {
    int passes = 0;
    for (int i = 0; i < size - 1; i++) {
        passes++;
        bool swapped = false;
        for (int j = 0; j < size - 1 - i; j++) {
            if (data[j] > data[j + 1]) {
                swapAt(j, j + 1);
                swapped = true;
            }
        }
        if (!swapped) break; // Finished early
    }
    return passes;
}

// =============================================================================
// 7. DEMONSTRATION & TEST SUITE
// =============================================================================
int main() {
    cout << "=========================================================" << endl;
    cout << "   Data Structures (C++) - Session 05: Sorting ArrayList " << endl;
    cout << "   Instructor: Eng. Muhammad Ali Abdul Kareem            " << endl;
    cout << "=========================================================\n" << endl;

    // 1. Initialize ArrayList with initial capacity of 10
    ArrayList list(10);

    // 2. Populate sample data: 5, 3, 8, 4, 2
    cout << "--- 1. Initial Data Insertion ---" << endl;
    list.push(5);
    list.push(3);
    list.push(8);
    list.push(4);
    list.push(2);
    list.display();

    // 3. Test Student Task 1: isSorted()
    cout << "\n--- 2. Checking if List is Sorted ---" << endl;
    cout << "list.isSorted() -> " << (list.isSorted() ? "true (SORTED)" : "false (UNSORTED)") << endl;

    // 4. Test Student Task 2: bubbleSortPasses() on a copy or directly
    ArrayList listCopy = list; // Tests deep copy constructor
    cout << "\n--- 3. Testing bubbleSortPasses() ---" << endl;
    int passes = listCopy.bubbleSortPasses();
    cout << "Passes taken to sort [5, 3, 8, 4, 2]: " << passes << endl;

    // 5. Test Insertion Sort on the main list
    cout << "\n--- 4. Running insertionSort() on list ---" << endl;
    list.insertionSort();
    list.display();
    cout << "list.isSorted() after insertionSort() -> " << (list.isSorted() ? "true" : "false") << endl;

    // 6. Test insertSorted()
    cout << "\n--- 5. Testing insertSorted(6) ---" << endl;
    list.insertSorted(6);
    list.display();

    // 7. Test Binary Search
    cout << "\n--- 6. Testing binarySearch() on Sorted Array ---" << endl;
    int target1 = 6;
    int target2 = 50;
    cout << "binarySearch(" << target1 << ") -> index " << list.binarySearch(target1) << endl;
    cout << "binarySearch(" << target2 << ") -> index " << list.binarySearch(target2) << " (not found)" << endl;

    cout << "\n=========================================================" << endl;
    cout << "   All operations completed successfully!                " << endl;
    cout << "=========================================================" << endl;

    return 0; // ~ArrayList() automatically frees heap memory here
}
