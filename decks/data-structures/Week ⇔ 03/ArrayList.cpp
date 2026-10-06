// =============================================================================
// Course: Data Structures with C++
// Session 03: Arrays with Object-Oriented Programming (OOP)
// Instructor: Eng. Muhammad Ali Abdul Kareem — Sinai University
// =============================================================================

#include <iostream>

using namespace std;

class ArrayList {
private:
    int* data;       // Dynamic heap storage
    int size;        // Number of elements currently stored
    int capacity;    // Total allocated slots

public:
    // Constructor
    ArrayList(int cap = 4) {
        capacity = cap;
        size = 0;
        data = new int[capacity];
    }

    // Destructor (frees heap memory)
    ~ArrayList() {
        delete[] data;
    }

    // Display all elements
    void display() const {
        if (size == 0) {
            cout << "[Empty list]" << endl;
            return;
        }
        for (int i = 0; i < size; i++) {
            cout << "Index " << i << " = " << data[i] << endl;
        }
    }

    // Insert value at a specific position (shifts right)
    bool insertAt(int pos, int value) {
        if (size == capacity || pos < 0 || pos > size) {
            return false;
        }
        for (int i = size; i > pos; i--) {
            data[i] = data[i - 1]; // Shift right
        }
        data[pos] = value;
        size++;
        return true;
    }

    // Delete value at a specific position (shifts left)
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

    // Search for a value and return its index (-1 if not found)
    int searchByValue(int target) const {
        for (int i = 0; i < size; i++) {
            if (data[i] == target) {
                return i;
            }
        }
        return -1;
    }

    // Update value at a specific position
    bool updateAt(int pos, int value) {
        if (pos < 0 || pos >= size) {
            return false;
        }
        data[pos] = value;
        return true;
    }

    // Double the array capacity when full
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

    // Add value to the end of the array
    void push(int value) {
        if (size == capacity) {
            grow();
        }
        data[size++] = value;
    }

    // =========================================================
    // STUDENT TASKS
    // =========================================================

    // Task 1: Find the index of the maximum value
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

    // Task 2: Reverse array in-place using two pointers
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

int main() {
    cout << "=== ArrayList Class Demonstration ===" << endl;

    // 1. Create list and push elements
    ArrayList list(4);
    list.push(10);
    list.push(20);
    list.push(30);
    list.push(40);

    cout << "\nInitial List (size = " << list.getSize() << ", capacity = " << list.getCapacity() << "):" << endl;
    list.display();

    // 2. Insert element at index 2
    cout << "\nInserting 99 at index 2:" << endl;
    list.insertAt(2, 99);
    list.display();

    // 3. Delete element at index 1
    cout << "\nDeleting element at index 1:" << endl;
    list.deleteAt(1);
    list.display();

    // 4. Update element at index 0
    cout << "\nUpdating index 0 to 50:" << endl;
    list.updateAt(0, 50);
    list.display();

    // 5. Search for a value
    int target = 99;
    cout << "\nSearching for " << target << ": found at index " << list.searchByValue(target) << endl;

    // 6. Task 1: findMax()
    int maxIdx = list.findMax();
    cout << "\n[Task 1] Max element index: " << maxIdx << endl;

    // 7. Task 2: reverse()
    cout << "\n[Task 2] Reversing the array in-place:" << endl;
    list.reverse();
    list.display();

    // 8. Dynamic growth demonstration
    cout << "\nPushing elements to trigger dynamic grow():" << endl;
    list.push(100);
    list.push(200);
    cout << "New size = " << list.getSize() << ", new capacity = " << list.getCapacity() << endl;
    list.display();

    return 0;
}
