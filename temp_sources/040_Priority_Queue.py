# %% [markdown]
# # Topic: Priority Queues - Priority ordering, sorted vs unsorted list implementations, and runtime trade-offs
# 
# ## 1. DEFINITION & SEMANTICS
# - **Priority Queue**: An abstract data type similar to a regular queue or stack, but where each element has an associated **priority key**.
# - **De-queuing Rule**: Elements with higher priority (or lower key value in a Min-Priority Queue) are popped before elements with lower priority.
# - **Operations**:
#   - **`insert(item, priority)`**: Adds an element with a priority key.
#   - **`remove_min()` / `pop()`**: Removes and returns the element with the highest priority (minimum key).
# 
# ## 2. LIST IMPLEMENTATION TRADE-OFFS (From Scratch)
# 1. **Unsorted List Implementation**:
#    - **`insert`**: **$O(1)$ time** (just append to list).
#    - **`remove_min`**: **$O(N)$ time** (requires searching the entire list to find the element with the minimum key, and popping it).
# 2. **Sorted List Implementation**:
#    - **`insert`**: **$O(N)$ time** (requires finding the correct sorted position and shifting elements to insert).
#    - **`remove_min`**: **$O(1)$ time** (simply pop the last element from the list since it's already sorted).
# 3. **Binary Heap (Most Optimal)**:
#    - Offers **$O(\log N)$** for both insertion and removal (covered in the Heaps module).
# 
# ---

# %%
# 1. Unsorted List-based Priority Queue
class UnsortedPriorityQueue:
    def __init__(self):
        self._data = []  # Contains tuples of (priority, value)

    def __len__(self):
        return len(self._data)

    def is_empty(self):
        return len(self._data) == 0

    def insert(self, value, priority):
        """O(1) Insertion: just append to list."""
        self._data.append((priority, value))

    def remove_min(self):
        """O(N) Deletion: scan list for min priority."""
        if self.is_empty():
            raise IndexError("Remove from empty priority queue")
        
        # Find index of min priority item
        min_idx = 0
        for i in range(1, len(self._data)):
            if self._data[i][0] < self._data[min_idx][0]:
                min_idx = i
                
        # Pop and return value
        priority, value = self._data.pop(min_idx)
        return value

    def __repr__(self):
        return f"UnsortedPQ({self._data})"

# 2. Sorted List-based Priority Queue
class SortedPriorityQueue:
    def __init__(self):
        self._data = []

    def __len__(self):
        return len(self._data)

    def is_empty(self):
        return len(self._data) == 0

    def insert(self, value, priority):
        """O(N) Insertion: insert in sorted position (descending order)."""
        new_item = (priority, value)
        if self.is_empty():
            self._data.append(new_item)
            return

        # Find position to insert (keeping list sorted descending)
        insert_idx = 0
        while insert_idx < len(self._data) and self._data[insert_idx][0] > priority:
            insert_idx += 1
            
        self._data.insert(insert_idx, new_item)

    def remove_min(self):
        """O(1) Deletion: Pop from the end of the sorted list."""
        if self.is_empty():
            raise IndexError("Remove from empty priority queue")
        priority, value = self._data.pop()
        return value

    def __repr__(self):
        return f"SortedPQ({self._data})"

print("--- Unsorted Priority Queue (O(1) insert, O(N) pop) ---")
upq = UnsortedPriorityQueue()
upq.insert("Process A", 3)
upq.insert("Process B", 1)  # High priority (min key)
upq.insert("Process C", 2)
print(upq)
print(f"Removed min: {upq.remove_min()}")  # Expected: "Process B"

print("\n--- Sorted Priority Queue (O(N) insert, O(1) pop) ---")
spq = SortedPriorityQueue()
spq.insert("Process A", 3)
spq.insert("Process B", 1)  # High priority (min key)
spq.insert("Process C", 2)
print(spq)
print(f"Removed min: {spq.remove_min()}")  # Expected: "Process B"
