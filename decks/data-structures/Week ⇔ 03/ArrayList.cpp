// =============================================================================
// Course: Data Structures with C++
// Session 03: Arrays with Object-Oriented Programming (OOP)
// Instructor: Eng. Muhammad Ali Abdul Kareem — Sinai University
// =============================================================================

#include <iostream>
#include <limits>

using namespace std;

class ArrayList {
private:
    int* data;       // Pointer to dynamic heap memory
    int size;        // Current number of elements stored
    int capacity;    // Total allocated slots available

public:
    // ---------------------------------------------------------
    // 1. Constructor & Destructor (Memory Lifecycle Management)
    // ---------------------------------------------------------
    ArrayList(int cap = 4) {
        if (cap <= 0) cap = 4;
        capacity = cap;
        size = 0;
        data = new int[capacity];
    }

    ~ArrayList() {
        delete[] data;
        data = nullptr;
    }

    // ---------------------------------------------------------
    // 2. Rule of Three: Deep Copy Constructor & Copy Assignment
    // ---------------------------------------------------------
    ArrayList(const ArrayList& other) {
        capacity = other.capacity;
        size = other.size;
        data = new int[capacity];
        for (int i = 0; i < size; i++) {
            data[i] = other.data[i];
        }
    }

    ArrayList& operator=(const ArrayList& other) {
        if (this == &other) return *this;
        delete[] data;
        capacity = other.capacity;
        size = other.size;
        data = new int[capacity];
        for (int i = 0; i < size; i++) {
            data[i] = other.data[i];
        }
        return *this;
    }

    // ---------------------------------------------------------
    // 3. Helper: Safe Numeric Input
    // ---------------------------------------------------------
    static int readInt() {
        int val;
        while (true) {
            if (cin >> val) return val;
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            cout << "Invalid input. Please enter a valid integer: ";
        }
    }

    // ---------------------------------------------------------
    // 4. Core Array Operations
    // ---------------------------------------------------------
    void fillFromUser(int n) {
        if (n <= 0 || n > capacity - size) return;
        for (int i = 0; i < n; i++) {
            cout << "Enter element " << (size + 1) << ": ";
            data[size++] = readInt();
        }
    }

    void display() const {
        if (size == 0) {
            cout << "[Empty ArrayList]" << endl;
            return;
        }
        for (int i = 0; i < size; i++) {
            cout << "Index " << i << " = " << data[i] << endl;
        }
    }

    bool insertAt(int pos, int value) {
        if (pos < 0 || pos > size || size == capacity) {
            return false;
        }
        for (int i = size; i > pos; i--) {
            data[i] = data[i - 1]; // Shift right
        }
        data[pos] = value;
        size++;
        return true;
    }

    bool deleteAt(int pos) {
        if (pos < 0 || pos >= size) {
            return false;
        }
        for (int i = pos; i < size - 1; i++) {
            data[i] = data[i + 1]; // Shift left
        }
        size--;
        return true;
    }

    int searchByValue(int target) const {
        for (int i = 0; i < size; i++) {
            if (data[i] == target) return i; // Found at index i
        }
        return -1; // Not found
    }

    bool updateAt(int pos, int value) {
        if (pos < 0 || pos >= size) {
            return false;
        }
        data[pos] = value; // O(1) direct write
        return true;
    }

    // ---------------------------------------------------------
    // 5. Dynamic Growth (Doubling Strategy)
    // ---------------------------------------------------------
    void grow() {
        int newCap = capacity * 2;
        int* bigger = new int[newCap];
        for (int i = 0; i < size; i++) {
            bigger[i] = data[i];
        }
        delete[] data;
        data = bigger;
        capacity = newCap;
    }

    void push(int value) {
        if (size == capacity) {
            grow();
        }
        data[size++] = value;
    }

    // ---------------------------------------------------------
    // 6. Student Hands-on Tasks
    // ---------------------------------------------------------
    // Task 1: findMax() - returns the index of the maximum value
    int findMax() const {
        if (size == 0) return -1;
        int best = 0;
        for (int i = 1; i < size; i++) {
            if (data[i] > data[best]) {
                best = i;
            }
        }
        return best;
    }

    // Task 2: reverse() - in-place two-pointer swap: O(n) time, O(1) space
    void reverse() {
        for (int i = 0, j = size - 1; i < j; i++, j--) {
            int tmp = data[i];
            data[i] = data[j];
            data[j] = tmp;
        }
    }

    // Getters
    int getSize() const { return size; }
    int getCapacity() const { return capacity; }
};

// ---------------------------------------------------------
// 7. Demonstration Driver Program
// ---------------------------------------------------------
int main() {
    cout << "===========================================" << endl;
    cout << "  Constella Data Structures — Session 03   " << endl;
    cout << "  ArrayList Class with OOP in C++          " << endl;
    cout << "===========================================" << endl;

    cout << "How many elements would you like to enter initially? ";
    int n = ArrayList::readInt();

    ArrayList list(n + 4); // Extra capacity for insertions
    list.fillFromUser(n);

    cout << "\n--- Current Elements ---" << endl;
    list.display();

    cout << "\n[Demo] Inserting 99 at index 1..." << endl;
    list.insertAt(1, 99);
    list.display();

    cout << "\n[Demo] Maximum element is at index: " << list.findMax() << endl;

    cout << "\n[Demo] Reversing ArrayList in place..." << endl;
    list.reverse();
    list.display();

    cout << "\n[Demo] Deleting element at index 0..." << endl;
    list.deleteAt(0);
    list.display();

    return 0; // ~ArrayList() destructor frees memory here
}
