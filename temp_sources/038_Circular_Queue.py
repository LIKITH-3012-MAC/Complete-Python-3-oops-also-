# %% [markdown]
# # Topic: Circular Queues - Ring buffer layouts, modulo pointer arithmetic, and overflow states
# 
# ## 1. DEFINITION & THE RING BUFFER CONCEPT
# - **Circular Queue (Ring Buffer)**: A linear queue implementation using a fixed-size array where the last position wraps around to the first position.
# - **Pointers**:
#   - **`head`**: Index of the front element in the queue.
#   - **`tail`**: Index of the next available slot for insertion.
#   - **`size`**: Current number of elements inside the queue.
# - **Modulo Pointer Wraps**:
#   - Enqueue offset index: `tail = (tail + 1) % capacity`
#   - Dequeue offset index: `head = (head + 1) % capacity`
# 
# ## 2. EDGE STATES: OVERFLOW & UNDERFLOW
# - **Queue Full (Overflow)**: Triggered when trying to enqueue and `size == capacity`.
# - **Queue Empty (Underflow)**: Triggered when trying to dequeue and `size == 0`.
# - **Benefit**: Absolute memory reuse. Memory allocations are done once at instantiation. Pointers wrap around infinitely, avoiding shifting costs or memory reallocations.
# 
# ## 3. REAL-WORLD APPLICATIONS
# - **Network Packet Buffering**: Circular buffers hold network stream packets (e.g. ring buffers inside sockets).
# - **Audio Streaming**: Audio APIs read and write streams circularly.
# 
# ---

# %%
# 1. Custom Circular Queue Implementation
class CircularQueue:
    def __init__(self, capacity):
        self.capacity = capacity
        self._data = [None] * capacity  # Allocate fixed array
        self.head = 0
        self.tail = 0
        self.size = 0

    def __len__(self):
        return self.size

    def is_empty(self):
        return self.size == 0

    def is_full(self):
        return self.size == self.capacity

    def enqueue(self, val):
        """O(1) Enqueue: inserts at tail, wraps around using modulo."""
        if self.is_full():
            raise OverflowError("Circular Queue is full (Queue Overflow)")
        
        self._data[self.tail] = val
        # Wrap pointer using modulo arithmetic
        self.tail = (self.tail + 1) % self.capacity
        self.size += 1

    def dequeue(self):
        """O(1) Dequeue: removes from head, wraps around using modulo."""
        if self.is_empty():
            raise IndexError("Dequeue from empty queue (Queue Underflow)")
        
        val = self._data[self.head]
        self._data[self.head] = None  # Clear slot reference
        # Wrap pointer using modulo arithmetic
        self.head = (self.head + 1) % self.capacity
        self.size -= 1
        return val

    def __repr__(self):
        return (f"CircularQueue(Size: {self.size}/{self.capacity} | "
                f"Head index: {self.head} | Tail index: {self.tail} | "
                f"Buffer: {self._data})")

print("--- Circular Queue Execution ---")
cq = CircularQueue(4)
cq.enqueue(10)
cq.enqueue(20)
cq.enqueue(30)
print(cq)  # Expected size: 3/4. Buffer: [10, 20, 30, None]

# Dequeue 2 elements
print(f"Dequeued: {cq.dequeue()}")  # Expected: 10
print(f"Dequeued: {cq.dequeue()}")  # Expected: 20
print(cq)  # Expected: Head index has wrapped to 2. Buffer: [None, None, 30, None]

# Enqueue 2 new elements - tail wraps around to index 0 and 1!
cq.enqueue(40)
cq.enqueue(50)
print(cq)  # Expected: Tail wrapped back to 0. Buffer: [50, None, 30, 40] (in modulo sequence)

try:
    # Try to overflow the queue (capacity is 4)
    cq.enqueue(60)
    cq.enqueue(70)
except OverflowError as e:
    print(f"Caught expected OverflowError: {e}")
