# %% [markdown]
# # Topic: Static Arrays - Contiguous memory structures, insertion/deletion shifting, and C-style array layouts
# 
# ## 1. DEFINITION & CONTIGUOUS MEMORY
# - **Static Array**: A low-level collection of elements of the same type stored in **contiguous (adjacent) memory blocks**.
# - **Contiguous Memory**:
#   - Allows direct random access using index arithmetic:
#     $$\text{Address}(A[i]) = \text{BaseAddress} + i \times \text{ElementSize}$$
#   - This allows lookup by index to execute in **$O(1)$ constant time**.
# - **Fixed Size**: Static arrays have a fixed length determined at instantiation. They cannot grow or shrink dynamically.
# 
# ## 2. COMPLEXITY ANALYSIS
# - **Access**: $O(1)$ (Direct index calculation).
# - **Search**: $O(N)$ (Linear scan, unless sorted and binary searched $O(\log N)$).
# - **Insertion / Deletion**:
#   - **$O(N)$ time**: Inserting or deleting an element at index $i$ requires shifting all subsequent elements to the right or left to maintain contiguous layout.
#   - **$O(1)$ boundary cases**: Inserting or deleting at the very end of the array (if capacity permits) is $O(1)$.
# 
# ## 3. PYTHON STANDARD LIBRARY: array MODULE
# - Python's standard `list` is a dynamic array of pointers.
# - The **`array.array`** module (PEP 3118) provides dense, C-style primitive arrays containing homogeneous (single-type) elements.
#   - *Memory efficiency*: Highly optimized since it stores raw binary numbers directly, avoiding the pointer overhead and reference-counting boxing costs of standard Python objects in lists.
# 
# ---

# %%
import array
import sys

# 1. Implementing a Static Array from Scratch in Python
class StaticArray:
    """Simulates a fixed-size, low-level contiguous array."""
    def __init__(self, capacity):
        self._capacity = capacity
        # Allocate a fixed-size contiguous block pre-filled with None
        self._data = [None] * capacity
        self._size = 0

    def __len__(self):
        return self._size

    def __getitem__(self, index):
        """O(1) Random Access."""
        self._validate_index(index)
        return self._data[index]

    def __setitem__(self, index, value):
        """O(1) Value Assignment."""
        self._validate_index(index)
        self._data[index] = value

    def _validate_index(self, index):
        if not (0 <= index < self._capacity):
            raise IndexError("Array index out of bounds")

    def insert(self, index, value):
        """O(N) Insertion: shifts subsequent elements to the right."""
        if self._size >= self._capacity:
            raise OverflowError("Array is at full capacity")
        if not (0 <= index <= self._size):
            raise IndexError("Invalid insertion index")

        # Shift elements right: start from size and move down to index
        for i in range(self._size, index, -1):
            self._data[i] = self._data[i - 1]
        
        self._data[index] = value
        self._size += 1

    def delete(self, index):
        """O(N) Deletion: shifts subsequent elements to the left."""
        self._validate_index(index)
        # Shift elements left: move elements after index down
        for i in range(index, self._size - 1):
            self._data[i] = self._data[i + 1]
        
        self._data[self._size - 1] = None
        self._size -= 1

    def __repr__(self):
        return f"StaticArray(Size: {self._size}/{self._capacity} | Data: {self._data})"

print("--- Custom Static Array Execution ---")
arr = StaticArray(5)
arr.insert(0, 10)
arr.insert(1, 20)
arr.insert(2, 30)
print(f"After inserts: {arr}")  # Expected: [10, 20, 30, None, None]

# Insert in middle (index 1) - shifts 20 and 30 to the right
arr.insert(1, 99)
print(f"After middle insert (index 1): {arr}")  # Expected: [10, 99, 20, 30, None]

# Delete from index 2 - shifts 30 to the left
arr.delete(2)
print(f"After delete at index 2:        {arr}")  # Expected: [10, 99, 30, None, None]

# %%
# 2. CPython array module vs list memory footprint
print("\n--- Memory Footprint: list vs array.array ---")
limit = 10000

# Standard list of floats (stores pointer objects to float instances)
list_floats = [float(i) for i in range(limit)]

# Homogeneous C-style float array (stores dense 8-byte doubles directly)
array_floats = array.array('d', (float(i) for i in range(limit)))

print(f"List size in memory:  {sys.getsizeof(list_floats)} bytes")
print(f"Array size in memory: {sys.getsizeof(array_floats)} bytes")
# Expected: array.array consumes significantly less memory!
