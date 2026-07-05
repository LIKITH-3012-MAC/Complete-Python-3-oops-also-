###############################################################################
# TOPIC: Lists - Implementation Internals, dynamic Arrays, and Allocation
#
# 1. DEFINITION & INTRODUCTION:
#    - Python's `list` is a mutable, ordered sequence of heterogeneous objects.
#
# 2. CPYTHON INTERNAL STRUCTURE:
#    - Under the hood in CPython, a list is represented by the `PyListObject` C struct:
#      ```c
#      typedef struct {
#          PyObject_VAR_HEAD
#          PyObject **ob_item;
#          Py_ssize_t allocated;
#      } PyListObject;
#      ```
#    - Pointers array: `ob_item` is a pointer to a dynamically allocated array of pointers
#      pointing to `PyObject` structs.
#    - A list does not contain the actual object payloads inline. Instead, it contains
#      the memory addresses of the objects. This design allows lists to store mixed
#      types (integers, strings, custom objects) within a single contiguous array of pointers.
#
# 3. AMORTIZED O(1) APPEND & OVER-ALLOCATION STRATEGY:
#    - When you append an element to a list, Python must place its pointer in the next
#      empty slot. If the underlying C array is full, Python must allocate a new, larger array
#      and copy all existing pointers to it.
#    - To avoid resizing on every single `append()` (which would run in O(N) time), Python uses an
#      over-allocation strategy.
#    - When the list runs out of space, CPython allocates extra capacity according to a formula:
#      `new_allocated = (size_t)newsize + (newsize >> 3) + (newsize < 9 ? 3 : 6);`
#      This grows the capacity roughly by ~12% to 25% larger than the requested size.
#    - Because resizes happen exponentially less frequently as the list grows, the cost of
#      array allocation and copying is spread across many operations, resulting in an
#      amortized time complexity of O(1) for list `append()`.
#
# 4. TIME COMPLEXITY:
#    - Access by index: O(1) (simple array offset math).
#    - Append: Amortized O(1).
#    - Insert/Pop at arbitrary index: O(N) (requires shifting remaining pointers in memory).
#    - Search (`in`): O(N) (linear scan).
#
# 5. CYCLIC GC TRACKING:
#    - Lists are container objects. Because a list can contain references to other containers
#      (or even reference itself), they are automatically tracked by the cyclic Garbage Collector
#      and undergo periodic Gen 0/1/2 collection sweeps.
#
# 6. INTERVIEW QUESTIONS:
#    - Q: How does Python list memory allocation work under the hood?
#      A: It is implemented as a dynamic array of pointers (`PyObject*`). When capacity is
#         reached, Python allocates a new array using an over-allocation algorithm (growth factor),
#         copies the pointers, and releases the old array. This ensures amortized O(1) appends.
#    - Q: Why is `insert(0, item)` slow on lists?
#      A: Inserting an item at index 0 requires shifting all existing N pointers in the contiguous
#         array to the right by one position, running in O(N) time. Use `collections.deque`
#         if you need fast O(1) insertions at both ends.
#
# 7. EXERCISES & SOLUTIONS:
#    - Coding challenge: Write a script that monitors a list's structural size growth
#      using `sys.getsizeof()` as you append elements one by one, showing the exact moments
#      when memory reallocations occur.
#
###############################################################################

import sys  # Standard library to check the memory size of objects in bytes

# 1. Monitoring List Over-Allocation & Resizing Steps
# We will create an empty list and monitor how its byte size changes as elements are appended.
monitored_list = []
previous_size = sys.getsizeof(monitored_list)

print("--- List Memory Growth Trace ---")
print(f"Empty list overhead: {previous_size} bytes")

reallocation_points = []

# Append 40 elements and track when the size increases
for i in range(40):
    monitored_list.append(i)
    current_size = sys.getsizeof(monitored_list)
    
    # If the size changed, it indicates Python resized/allocated a new array of pointers
    if current_size != previous_size:
        print(f"Resized at len {len(monitored_list):<2}: size expanded from {previous_size:<3} to {current_size:<3} bytes")
        reallocation_points.append(len(monitored_list))
        previous_size = current_size

# The allocations show gaps: e.g. size remains constant for a few appends, indicating
# that Python is writing pointers into the pre-allocated over-allocation slots.

# 2. Heterogeneous Reference Array Demonstration
# Lists store pointers, not objects. We can store completely different objects in the same list.
mixed_list = [42, "string", [1.1, 2.2]]
print("\n--- Mixed Pointer Array ---")
for idx, element in enumerate(mixed_list):
    print(f"Index {idx} element: {repr(element):<12} | Address: {id(element)} | Type: {type(element)}")

# 3. List Shallow Copy Mechanics
# Slicing a list or calling list.copy() copies the pointer array, not the underlying objects!
list_orig = [[1, 2], 3]
list_copy = list_orig.copy()

print("\n--- Shallow Copy Demonstration ---")
print(f"Original: {list_orig} | Copy: {list_copy}")
print(f"Are list objects the same?  {list_orig is list_copy}")  # Expected: False (Different pointer array)
print(f"Are inner elements the same? {list_orig[0] is list_copy[0]}")  # Expected: True (Shared reference to nested list)

# Modifying the shared nested list affects both list references
list_orig[0].append(99)
print(f"Original after update: {list_orig}")
print(f"Copy after update:     {list_copy}")  # Also changed!
