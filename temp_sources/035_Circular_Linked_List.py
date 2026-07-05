# %% [markdown]
# # Topic: Circular Linked Lists - Loop boundary traversals, tail-to-head wraps, and round-robin task schedulers
# 
# ## 1. DEFINITION & POINTER STRUCTURE
# - **Circular Linked List (CLL)**: A linked list variation where the last node (tail) points back to the first node (head) instead of pointing to `None`.
# - **Variations**:
#   - **Singly Circular**: Last node's `next` pointer references the head node.
#   - **Doubly Circular**: Last node's `next` references head, and head's `prev` references the last node.
# 
# ## 2. LOOP TRAVERSAL BOUNDARIES
# - **Termination Warning**: Since there is no terminal `None` pointer, standard linear loops (`while current:`) will run infinitely.
# - **Correct Termination**: Iterations must keep track of the starting node (usually `head`). The traversal finishes when `current.next` matches the `head` reference again.
# 
# ## 3. REAL-WORLD APPLICATIONS
# 1. **Round-Robin Scheduling**: Operating systems share CPU time among processes by placing them in a circular queue, cycling through them continuously.
# 2. **Multiplayer Turn Systems**: Game engines route turns from player to player circularly.
# 3. **Media Playlists**: Continuous audio loops.
# 
# ---

# %%
# 1. Singly Circular Linked List Implementation
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class CircularLinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        """O(N) Append: Traverse to tail and link back to head."""
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            new_node.next = self.head  # Points to itself
            return

        current = self.head
        # Traverse until current.next points back to head (the tail)
        while current.next is not self.head:
            current = current.next
        
        current.next = new_node
        new_node.next = self.head  # Wrap tail back to head

    def display(self):
        if self.head is None:
            return "Empty Circular List"
        
        elements = []
        current = self.head
        while True:
            elements.append(str(current.data))
            current = current.next
            # Break loop when we wrap back to the head
            if current is self.head:
                break
        return " -> ".join(elements) + " -> (Back to Head)"

print("--- Circular Linked List Operations ---")
cll = CircularLinkedList()
cll.append("Task A")
cll.append("Task B")
cll.append("Task C")
print(cll.display())  # Expected: Task A -> Task B -> Task C -> (Back to Head)

# %%
# 2. Round-Robin Scheduler Simulation using Circular List
def run_round_robin(cll_scheduler, time_quantum):
    """Simulates CPU process scheduling by allocating fixed times to circular tasks."""
    if cll_scheduler.head is None:
        return

    print(f"\n--- OS Round-Robin Simulation (Quantum={time_quantum}s) ---")
    current = cll_scheduler.head
    
    # Run loop for 6 steps to simulate circular CPU scheduling cycles
    for cycle in range(1, 7):
        print(f"Cycle {cycle}: CPU allocated to {current.data}...")
        current = current.next  # Move to next task automatically in circle

run_round_robin(cll, time_quantum=2)
# Expected: cycles through Task A, B, C, then wraps back to Task A, B, C!
