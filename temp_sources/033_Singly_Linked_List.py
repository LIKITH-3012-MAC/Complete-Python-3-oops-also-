# %% [markdown]
# # Topic: Singly Linked Lists - Node references, pointer updates, and Floyd's loop detection algorithm
# 
# ## 1. DEFINITION & MEMORY LAYOUT
# - **Singly Linked List**: A linear data structure where elements are not stored in contiguous memory. Instead:
#   - Each element is contained in a **Node** object.
#   - Each Node contains:
#     1. **Data**: The value stored in the node.
#     2. **Next**: A pointer (reference) pointing to the next Node object in the sequence.
#   - The list begins at a **Head** node reference, and ends at a node pointing to `None`.
# 
# ## 2. COMPLEXITY ANALYSIS
# - **Prepend (insert at head)**: **$O(1)$ time** (just point new node to head, and update head).
# - **Append (insert at tail)**: **$O(N)$ time** (requires traversing from head to the last node, unless a Tail pointer is kept which allows $O(1)$).
# - **Deletion**: **$O(N)$ time** (requires searching for the target node and updating the predecessor's next pointer).
# - **Access / Search**: **$O(N)$ time** (requires linear traversal, no random access index math).
# 
# ## 3. LOOP DETECTION: FLOYD'S CYCLE FINDING ALGORITHM
# - **The Problem**: A corrupted linked list where a node points back to a predecessor, creating an infinite loop.
# - **The Algorithm (Tortoise and Hare)**:
#   - Initialize two pointers at the head: `slow` and `fast`.
#   - Move `slow` by 1 node at a time; move `fast` by 2 nodes at a time.
#   - If there is a cycle, the `fast` pointer will eventually wrap around and meet the `slow` pointer (`slow == fast`). If `fast` reaches `None`, there is no cycle.
#   - **Time Complexity**: $O(N)$.
#   - **Space Complexity**: $O(1)$ auxiliary space.
# 
# ---

# %%
# 1. Node Class Implementation
class Node:
    """A single node inside a Singly Linked List."""
    def __init__(self, data):
        self.data = data
        self.next = None  # Reference pointer to next node

# 2. Singly Linked List Implementation
class SinglyLinkedList:
    def __init__(self):
        self.head = None

    def prepend(self, data):
        """O(1) Prepend: Insert at head."""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def append(self, data):
        """O(N) Append: Traverse to end and insert."""
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        
        # Traverse to last node
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def delete(self, key):
        """O(N) Delete: Find key, update pointers."""
        current = self.head
        
        # Case 1: Head contains key
        if current and current.data == key:
            self.head = current.next
            return
        
        # Case 2: Search for key, tracking predecessor
        prev = None
        while current and current.data != key:
            prev = current
            current = current.next
            
        if current is None:
            return  # Key not found
            
        # Unlink node
        prev.next = current.next

    def reverse(self):
        """O(N) Reverse: Swaps pointers in-place."""
        prev = None
        current = self.head
        while current:
            next_node = current.next  # Save next node
            current.next = prev       # Reverse pointer direction
            prev = current            # Shift prev
            current = next_node       # Shift current
        self.head = prev

    def has_cycle(self):
        """O(N) Loop Detection: Floyd's Tortoise and Hare algorithm."""
        slow = self.head
        fast = self.head
        while fast and fast.next:
            slow = slow.next          # Move 1 step
            fast = fast.next.next     # Move 2 steps
            if slow == fast:
                return True           # Meeting point proves cycle existence!
        return False

    def display(self):
        elements = []
        current = self.head
        # Max limit to prevent infinite loops in cycles display
        count = 0
        while current and count < 20:
            elements.append(str(current.data))
            current = current.next
            count += 1
        return " -> ".join(elements) + " -> None"

print("--- Singly Linked List Operations ---")
sll = SinglyLinkedList()
sll.prepend(10)
sll.prepend(20)
sll.append(30)
sll.append(40)
print(f"List after prepend/append: {sll.display()}")  # Expected: 20 -> 10 -> 30 -> 40 -> None

# Delete key 30
sll.delete(30)
print(f"List after deleting 30:   {sll.display()}")  # Expected: 20 -> 10 -> 40 -> None

# Reverse list
sll.reverse()
print(f"List after reversal:      {sll.display()}")  # Expected: 40 -> 10 -> 20 -> None

# %%
# 3. Floyd's Cycle Detection Demo
print("\n--- Cycle Detection (Floyd's Algorithm) ---")
cycle_list = SinglyLinkedList()
cycle_list.append(1)
cycle_list.append(2)
cycle_list.append(3)
cycle_list.append(4)

print(f"Has cycle initially? {cycle_list.has_cycle()}")  # Expected: False

# Introduce a loop corrupting the list (node 4 points back to node 2)
head = cycle_list.head
node_2 = head.next
node_4 = node_2.next.next
node_4.next = node_2  # Creating cycle loop!

print(f"Has cycle after corruption? {cycle_list.has_cycle()}")  # Expected: True
