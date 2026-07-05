# %% [markdown]
# # Topic: Deques - Double-ended operations, DLL-based deques, and CPython block-link optimizations
# 
# ## 1. DEFINITION & SEMANTICS
# - **Deque (Double-Ended Queue)**: A linear collection that supports element insertion and removal at both ends:
#   - **Front end**: `appendleft(item)` and `popleft()`.
#   - **Back end**: `append(item)` and `pop()`.
# - **Complexity**: All four operations execute in **$O(1)$ constant time**.
# 
# ## 2. CPYTHON INTERNAL OPTIMIZATIONS: collections.deque
# - Why not use a standard dynamic list?
#   - List `insert(0, val)` and `pop(0)` are $O(N)$ operations.
# - CPython's **`collections.deque`** does NOT use a simple linked list.
#   - **Block-Link Structure**:
#     - It is implemented as a doubly-linked list of **fixed-size block arrays** (each block has space for 64 element pointers in 64-bit platforms).
#     - *Pros*: Provides extremely fast $O(1)$ random-like lookups within blocks, maintains C-speed contiguous execution, and avoids the high reference pointer memory overhead of standard node-by-node linked lists.
# 
# ---

# %%
from collections import deque

# 1. Custom DLL-based Deque implementation from scratch
class DLLNode:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class CustomDeque:
    """Deque implemented from scratch using a Doubly Linked List with Sentinels."""
    def __init__(self):
        self.header = DLLNode(None)
        self.trailer = DLLNode(None)
        self.header.next = self.trailer
        self.trailer.prev = self.header
        self.size = 0

    def __len__(self):
        return self.size

    def is_empty(self):
        return self.size == 0

    def _insert_between(self, data, predecessor, successor):
        new_node = DLLNode(data)
        new_node.prev = predecessor
        new_node.next = successor
        predecessor.next = new_node
        successor.prev = new_node
        self.size += 1
        return new_node

    def _delete_node(self, node):
        predecessor = node.prev
        successor = node.next
        predecessor.next = successor
        successor.prev = predecessor
        self.size -= 1
        return node.data

    def append(self, data):
        """O(1) Append to back."""
        self._insert_between(data, self.trailer.prev, self.trailer)

    def appendleft(self, data):
        """O(1) Append to front."""
        self._insert_between(data, self.header, self.header.next)

    def pop(self):
        """O(1) Pop from back."""
        if self.is_empty():
            raise IndexError("Pop from empty deque")
        return self._delete_node(self.trailer.prev)

    def popleft(self):
        """O(1) Pop from front."""
        if self.is_empty():
            raise IndexError("Pop from empty deque")
        return self._delete_node(self.header.next)

    def __repr__(self):
        elements = []
        curr = self.header.next
        while curr is not self.trailer:
            elements.append(str(curr.data))
            curr = curr.next
        return f"CustomDeque(Front -> {' <-> '.join(elements)} <- Back)"

print("--- Custom Deque Operations ---")
dq = CustomDeque()
dq.append(10)
dq.append(20)
dq.appendleft(5)
print(dq)  # Expected: Front -> 5 <-> 10 <-> 20 <- Back

print(f"Popped from front: {dq.popleft()}")  # Expected: 5
print(f"Popped from back:  {dq.pop()}")      # Expected: 20
print(dq)  # Expected: Front -> 10 <- Back

# %%
# 2. Python standard collections.deque usage
print("\n--- Standard collections.deque ---")
std_dq = deque([1, 2, 3])
std_dq.appendleft(100)
std_dq.append(200)
print(f"deque values: {std_dq}")

# Rotations: collections.deque supports rotating elements in O(K) time
std_dq.rotate(2)  # Rotates 2 steps to the right
print(f"After rotating right by 2: {std_dq}")
