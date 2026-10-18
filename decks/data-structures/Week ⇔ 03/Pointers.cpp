// Data Structures — Session 03: Pointers & Memory
#include <iostream>
using namespace std;

int main() {
    // ---- Pointer Basics: value vs address ----
    int x = 10;
    int* p = &x;      // p holds the ADDRESS of x

    cout << x << endl;    // 10
    cout << *p << endl;   // 10  (value at that address)
    cout << p << endl;    // an address, e.g. 0x1000

    // ---- Memory Basics: Stack vs Heap ----
    int size = 0;                 // local variable (stack)
    int capacity = 5;             // local variable (stack)
    int* data = new int[5];       // array on the heap
    // new returns the address of the first element; data keeps it

    // ---- Why is data a Pointer? ----
    // Fixed: size frozen at compile time
    int fixedData[5];

    // Dynamic: size chosen at runtime
    int* dynamicData;
    dynamicData = new int[capacity];

    // ---- new[] and delete[] belong together ----
    // new    -> delete
    // new[]  -> delete[]
    delete[] dynamicData;
    delete[] data;

    return 0;
}
