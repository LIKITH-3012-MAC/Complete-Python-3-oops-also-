# %% [markdown]
# # Topic: Queues - FIFO semantics, optimized array list cursors, and linked list queues
# 
# ## 1. DEFINITION & SEMANTICS
# - **Queue**: A linear data structure that adheres to the **FIFO (First-In, First-Out)** execution order principle.
# - **Operations**:
#   - **`enqueue(item)`**: Inserts an item at the back of the queue (tail).
#   - **`dequeue()`**: Removes and returns the item from the front of the queue (head). Raises an error if empty (Queue Underflow).
#   - **`first()` / `peek()`**: Returns the front item without removing it.
# 
# ## 2. IMPLEMENTATION PARADIGMS & OPTIMIZATIONS
# 1. **Naive Array-based Queue**:
#    - Uses a list `pop(0)` for dequeue.
#    - **Fatal Flaw**: `pop(0)` is an **$O(N)$ operation** because it requires shifting all remaining elements one slot left in memory.
# 2. **Optimized Array-based Queue**:
#    - Instead of shifting elements, maintain a **Read Pointer Index** cursor pointing to the current front element.
#    - **`dequeue()`**: Reads the value at the cursor index, increments the cursor, and marks the old slot as None.
#    - **Complexity**: $O(1)$ constant execution time for both enqueue and dequeue.
# 3. **Linked-List-based Queue**:
#    - Uses a Singly Linked List maintaining **both** a `head` and a `tail` pointer reference.
#    - **`enqueue()`**: Appends directly at `tail.next = new_node; tail = new_node` ($O(1)$).
#    - **`dequeue()`**: Deletes and shifts the `head` pointer to `head.next` ($O(1)$).
# 
# ---

# %%
# 1. Optimized Array-based Queue (Read Pointer Cursor)
class ArrayQueue:
    def __init__(self):
        self._data = []
        self._front = 0  # Read pointer index cursor

    def __len__(self):
        return len(self._data) - self._front

    def is_empty(self):
        return len(self._data) == self._front

    def enqueue(self, val):
        """O(1) Enqueue."""
        self._data.append(val)

    def dequeue(self):
        """O(1) Dequeue (no shifting!)."""
        if self.is_empty():
            raise IndexError("Dequeue from empty queue (Queue Underflow)")
        val = self._data[self._front]
        self._data[self._front] = None  # Free memory reference
        self._front += 1
        return val

    def first(self):
        """O(1) Peek."""
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self._data[self._front]

    def __repr__(self):
        return f"ArrayQueue(Front -> {self._data[self._front:]} <- Back)"

# 2. Linked-List-based Queue (Head & Tail pointers)
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedQueue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def __len__(self):
        return self.size

    def is_empty(self):
        return self.size == 0

    def enqueue(self, val):
        """Strict O(1) Enqueue at tail."""
        new_node = Node(val)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def dequeue(self):
        """Strict O(1) Dequeue from head."""
        if self.is_empty():
            raise IndexError("Dequeue from empty queue")
        popped_val = self.head.data
        self.head = self.head.next
        self.size -= 1
        if self.is_empty():
            self.tail = None  # Reset tail if list is now empty
        return popped_val

    def __repr__(self):
        elements = []
        curr = self.head
        while curr:
            elements.append(str(curr.data))
            curr = curr.next
        return f"LinkedQueue(Front -> {' -> '.join(elements)} <- Back)"

print("--- Array Queue (Optimized Cursor) ---")
aq = ArrayQueue()
aq.enqueue("Job A")
aq.enqueue("Job B")
aq.enqueue("Job C")
print(aq)
print(f"Dequeued: {aq.dequeue()}")  # Expected: "Job A"
print(aq)  # Notice: "Job A" is deleted, front cursor updated

print("\n--- Linked Queue (Head/Tail pointers) ---")
lq = LinkedQueue()
lq.enqueue("Job A")
lq.enqueue("Job B")
lq.enqueue("Job C")
print(lq)
print(f"Dequeued: {lq.dequeue()}")  # Expected: "Job A"
print(lq)
