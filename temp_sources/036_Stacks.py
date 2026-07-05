# %% [markdown]
# # Topic: Stacks - LIFO semantics, array and linked-list implementations, and parenthesis validation
# 
# ## 1. DEFINITION & SEMANTICS
# - **Stack**: A linear data structure that adheres to the **LIFO (Last-In, First-Out)** execution order principle.
# - **Operations**:
#   - **`push(item)`**: Inserts an item onto the top of the stack.
#   - **`pop()`**: Removes and returns the item from the top of the stack. Raises an error if empty (Stack Underflow).
#   - **`peek()`**: Returns the top item without removing it.
# 
# ## 2. IMPLEMENTATION PARADIGMS
# 1. **Array-based Stack**:
#    - Uses a dynamic list as the underlying buffer container.
#    - *Pros*: Fast $O(1)$ amortized operations; memory-dense.
#    - *Cons*: Occasional $O(N)$ resizing copy overhead.
# 2. **Linked-List-based Stack**:
#    - Uses nodes where insertions and deletions happen at the head node.
#    - *Pros*: Strict $O(1)$ time execution for all operations; no resize overhead.
#    - *Cons*: Memory overhead from node reference pointers.
# 
# ## 3. COMMON APPLICATIONS
# - **Call Stack**: Managing execution contexts and activation frames in programming language PVMs.
# - **Undo/Redo Actions**: Storing editor states.
# - **Expression Parsing**: Evaluating postfix notations or matching balanced parentheses.
# 
# ---

# %%
# 1. Array-based Stack Implementation
class ArrayStack:
    def __init__(self):
        self._data = []

    def __len__(self):
        return len(self._data)

    def is_empty(self):
        return len(self._data) == 0

    def push(self, val):
        """O(1) Amortized Push."""
        self._data.append(val)

    def pop(self):
        """O(1) Amortized Pop."""
        if self.is_empty():
            raise IndexError("Pop from empty stack (Stack Underflow)")
        return self._data.pop()

    def peek(self):
        """O(1) Peek."""
        if self.is_empty():
            raise IndexError("Peek from empty stack")
        return self._data[-1]

    def __repr__(self):
        return f"ArrayStack(Top -> {self._data[::-1]})"

# 2. Linked-List-based Stack Implementation
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedStack:
    def __init__(self):
        self.head = None
        self.size = 0

    def __len__(self):
        return self.size

    def is_empty(self):
        return self.size == 0

    def push(self, val):
        """Strict O(1) Push: Prepend to head."""
        new_node = Node(val)
        new_node.next = self.head
        self.head = new_node
        self.size += 1

    def pop(self):
        """Strict O(1) Pop: Delete head."""
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        popped_val = self.head.data
        self.head = self.head.next
        self.size -= 1
        return popped_val

    def peek(self):
        """Strict O(1) Peek."""
        if self.is_empty():
            raise IndexError("Peek from empty stack")
        return self.head.data

    def __repr__(self):
        elements = []
        curr = self.head
        while curr:
            elements.append(str(curr.data))
            curr = curr.next
        return f"LinkedStack(Top -> {' -> '.join(elements)} -> Base)"

print("--- Array Stack Operations ---")
astack = ArrayStack()
astack.push(10)
astack.push(20)
print(f"Stack state: {astack}")
print(f"Popped value: {astack.pop()}")  # Expected: 20

print("\n--- Linked Stack Operations ---")
lstack = LinkedStack()
lstack.push(10)
lstack.push(20)
lstack.push(30)
print(f"Stack state: {lstack}")  # Expected: Top -> 30 -> 20 -> 10 -> Base

# %%
# 3. Stack Application: Balanced Parentheses Matching
def is_balanced(expression):
    """Validates if brackets '()', '[]', '{}' are matched correctly using a Stack."""
    stack = ArrayStack()
    mapping = {")": "(", "}": "{", "]": "["}
    
    for char in expression:
        if char in mapping.values():
            stack.push(char)
        elif char in mapping.keys():
            if stack.is_empty() or stack.pop() != mapping[char]:
                return False
    return stack.is_empty()

print("\n--- Parenthesis Matcher Verification ---")
print(f"Is '{'({[]})'}' balanced? {is_balanced('({[]})')}")  # Expected: True
print(f"Is '{'({[})'}' balanced?  {is_balanced('({[})')}")   # Expected: False
