// Data Structures — Session 04: Arrays, the OOP way
#include <iostream>
using namespace std;

class ArrayList {
private:
    int* data;      // hidden storage
    int size;       // used slots
    int capacity;   // total slots
    void grow();
public:
    ArrayList(int cap);
    ArrayList(const ArrayList& other);   // deep copy
    ~ArrayList();
    void fillFromUser(int n);
    static int readInt();
    void display() const;
    bool insertAt(int pos, int value);
    bool deleteAt(int pos);
    int  searchByValue(int target) const;
    bool updateAt(int pos, int value);
    void push(int value);
    int  findMax() const;     // Student Task 1
    void reverse();           // Student Task 2
};

ArrayList::ArrayList(int cap) {
    capacity = cap;
    size = 0;
    data = new int[capacity];   // allocate
}

ArrayList::ArrayList(const ArrayList& other) {
    capacity = other.capacity;
    size = other.size;
    data = new int[capacity];      // own block
    for (int i = 0; i < size; i++)
        data[i] = other.data[i];   // copy values
}
// + operator= + destructor = Rule of Three

ArrayList::~ArrayList() {
    delete[] data;              // free memory
}

int ArrayList::readInt() {
    int x;
    cin >> x;                    // try to read a number
    while (cin.fail()) {         // typed letters?
        cin.clear();             // step 1: clear error
        cin.ignore(1000, '\n');  // step 2: drop letters
        cout << "Invalid, try again: ";
        cin >> x;                // step 3: ask again
    }
    return x;                    // x is a real number
}

void ArrayList::fillFromUser(int n) {
    if (n < 0 || n > capacity - size) {
        cout << "Invalid n" << endl;
        return;                  // change nothing
    }
    for (int i = 0; i < n; i++) {
        cout << "Enter element " << i + 1 << ": ";
        data[size] = readInt();
        size++;
    }
}

void ArrayList::display() const {
    for (int i = 0; i < size; i++) {
        cout << "Index " << i
             << " = " << data[i] << endl;
    }
}

bool ArrayList::insertAt(int pos, int value) {
    if (size == capacity || pos < 0 || pos > size)
        return false;
    for (int i = size; i > pos; i--)
        data[i] = data[i - 1];   // shift right
    data[pos] = value;
    size++;
    return true;
}

bool ArrayList::deleteAt(int pos) {
    if (pos < 0 || pos >= size)
        return false;
    for (int i = pos; i < size - 1; i++)
        data[i] = data[i + 1];   // shift left
    size--;
    return true;
}

int ArrayList::searchByValue(int target) const {
    for (int i = 0; i < size; i++) {
        if (data[i] == target)
            return i;       // found
    }
    return -1;              // not found
}

bool ArrayList::updateAt(int pos, int value) {
    if (pos < 0 || pos >= size)
        return false;
    data[pos] = value;      // direct access: O(1)
    return true;
}

void ArrayList::push(int value) {
    if (size == capacity)
        grow();                  // full: double it
    data[size++] = value;
}

void ArrayList::grow() {
    int newCap = capacity * 2;
    int* bigger = new int[newCap];
    for (int i = 0; i < size; i++)
        bigger[i] = data[i];     // copy
    delete[] data;               // free old block
    data = bigger;
    capacity = newCap;
}

int ArrayList::findMax() const {
    if (size == 0) return -1;      // empty guard
    int best = 0;
    for (int i = 1; i < size; i++) {
        if (data[i] > data[best])
            best = i;
    }
    return best;
}

void ArrayList::reverse() {
    for (int i = 0, j = size - 1; i < j; i++, j--) {
        int tmp = data[i];
        data[i] = data[j];
        data[j] = tmp;
    }
}

// 2D arrays in one flat block
class Matrix {
    int* data;
    int rows, cols;
public:
    Matrix(int r, int c) : rows(r), cols(c) {
        data = new int[r * c];     // ONE flat block
    }
    int& at(int r, int c) {
        return data[r * cols + c]; // row-major
    }
    ~Matrix() { delete[] data; }
};

int main() {
    int n;
    cout << "How many elements? ";
    n = ArrayList::readInt();
    ArrayList list(n + 2);   // spare capacity
    list.fillFromUser(n);
    list.display();
    list.deleteAt(1);
    cout << "-- after deleteAt(1) --" << endl;
    list.display();
    return 0;   // ~ArrayList() runs here
}
