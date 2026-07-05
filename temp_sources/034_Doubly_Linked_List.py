# %% [markdown]
# # Topic: Doubly Linked Lists - Bidirectional traversals, prev/next node references, and sentinel boundaries
# 
# ## 1. DEFINITION & POINTER ACTIONS
# - **Doubly Linked List (DLL)**: A linear data structure where each node maintains two pointer references:
#   1. **Next**: Points to the successor node in the list.
#   2. **Prev**: Points to the predecessor node in the list.
# - **Bidirectional Traversals**: Pointers allow traversing the list in both forward direction (head to tail) and backward direction (tail to head).
# 
# ## 2. SENTINEL NODES
# - **Sentinel Nodes**: Dummy header and trailer nodes that do not contain user data.
#   - **Head Sentinel**: Points to the first data node. Prev points to `None`.
#   - **Tail Sentinel**: Points to the last data node. Next points to `None`.
# - **Benefit**: Eliminates boundary checks for empty lists or single-element insertions/deletions, as every data node is guaranteed to be flanked by a predecessor and a successor.
# 
# ## 3. COMPLEXITY ANALYSIS
# - **Insertion**:
#   - **$O(1)$ time**: If the reference to the adjacent node is already known (just update 4 pointer arrows: 2 for the new node, 1 for predecessor, 1 for successor).
#   - **$O(N)$ time**: If we must search for the insertion position.
# - **Deletion**:
#   - **$O(1)$ time**: If we have the node reference (simply link predecessor directly to successor, bypassing target).
#   - **$O(N)$ time**: If we must search for the target value.
# 
# ---

# %%
# 1. DLL Node Class
class DLLNode:
    """A node inside a Doubly Linked List containing prev and next references."""
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

# 2. DLL implementation with Sentinel Nodes
class DoublyLinkedList:
    def __init__(self):
        # Instantiate Sentinels
        self.header = DLLNode(None)
        self.trailer = DLLNode(None)
        self.header.next = self.trailer
        self.trailer.prev = self.header
        self.size = 0

    def __len__(self):
        return self.size

    def insert_between(self, data, predecessor, successor):
        """O(1) Insertion helper between two existing nodes."""
        new_node = DLLNode(data)
        new_node.prev = predecessor
        new_node.next = successor
        predecessor.next = new_node
        successor.prev = new_node
        self.size += 1
        return new_node

    def append(self, data):
        """O(1) Append: Insert right before the trailer sentinel."""
        self.insert_between(data, self.trailer.prev, self.trailer)

    def prepend(self, data):
        """O(1) Prepend: Insert right after the header sentinel."""
        self.insert_between(data, self.header, self.header.next)

    def delete_node(self, node):
        """O(1) Deletion: Unlinks node directly, bypassing search."""
        predecessor = node.prev
        successor = node.next
        predecessor.next = successor
        successor.prev = predecessor
        self.size -= 1
        return node.data

    def delete_by_value(self, value):
        """O(N) Deletion: Search for value and unlink."""
        current = self.header.next
        while current is not self.trailer:
            if current.data == value:
                self.delete_node(current)
                return True
            current = current.next
        return False

    def display_forward(self):
        elements = []
        current = self.header.next
        while current is not self.trailer:
            elements.append(str(current.data))
            current = current.next
        return "Header <-> " + " <-> ".join(elements) + " <-> Trailer"

    def display_backward(self):
        elements = []
        current = self.trailer.prev
        while current is not self.header:
            elements.append(str(current.data))
            current = current.prev
        return "Trailer <-> " + " <-> ".join(elements) + " <-> Header"

print("--- Doubly Linked List Operations ---")
dll = DoublyLinkedList()
dll.append(10)
dll.append(20)
dll.prepend(5)
print(f"Forward path:  {dll.display_forward()}")  # Expected: 5 <-> 10 <-> 20
print(f"Backward path: {dll.display_backward()}") # Expected: 20 <-> 10 <-> 5

# Delete by value 10
dll.delete_by_value(10)
print(f"After deleting 10 (Forward): {dll.display_forward()}")  # Expected: 5 <-> 20
print(f"List length: {len(dll)}")  # Expected: 2
