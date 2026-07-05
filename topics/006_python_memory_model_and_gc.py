###############################################################################
# TOPIC: Python Memory Model, Allocation, and Garbage Collection
#
# 1. DEFINITION & INTRODUCTION:
#    - CPython manages all object memory automatically. It abstracts memory management
#      using a system that combines a private heap, reference counting, and a
#      generational cyclic garbage collector.
#
# 2. INTERNAL MEMORY ARCHITECTURE (PyMalloc):
#    - Python bypasses the standard OS `malloc` for small objects (<= 512 bytes) using
#      an internal allocator called PyMalloc.
#    - Structure of PyMalloc:
#        1. Arenas: Large contiguous chunks of memory (256 KB) requested from the OS.
#        2. Pools: Arenas are divided into Pools of 4 KB. Each pool contains blocks
#           of equal sizes.
#        3. Blocks: Small memory segments (ranging from 8 bytes up to 512 bytes)
#           allocated to actual Python objects.
#    - Large objects (> 512 bytes) are routed directly to the system allocator.
#
# 3. REFERENCE COUNTING SYSTEM:
#    - The primary memory management mechanism. Every object struct (`PyObject`)
#      holds a field `ob_refcnt`.
#    - When a variable points to an object, its reference count incremented by 1.
#    - When a reference goes out of scope or is deleted (`del`), `ob_refcnt` decreases.
#    - Once `ob_refcnt` hits 0, CPython immediately calls the type's deallocator
#      function (`tp_dealloc`) to free the block.
#
# 4. CYCLIC GARBAGE COLLECTOR:
#    - Reference counting cannot detect cyclic references (e.g., node A references
#      node B, and node B references node A, but neither is accessible from globals).
#    - Python uses a cyclic garbage collector (`gc` module) to find and collect these.
#    - Generational GC: Python categorizes container objects (lists, dicts, custom objects)
#      into three generations based on survival age:
#        - Generation 0: Newly created containers.
#        - Generation 1: Containers that survived Gen 0 collection.
#        - Generation 2: Long-lived containers.
#    - The collector uses a threshold system: when allocations in Gen 0 exceed the
#      threshold relative to deallocations, a collection is triggered.
#    - Cycle-Finding Algorithm: The collector temporarily copies reference counts,
#      subtracts counts corresponding to internal references within the container graph,
#      and any objects whose count becomes 0 are isolated as unreachable.
#
# 5. TIME & SPACE COMPLEXITY:
#    - Reference counting is O(1) time complexity for additions/deletions.
#    - Cyclic GC is O(N + M) where N is the number of objects in the generation being
#      collected, and M is the number of active links (references) between them.
#
# 6. GIL & THREAD SAFETY:
#    - Since reference counts are updated during almost all operations, CPython uses
#      the GIL to prevent race conditions when two threads modify the same object's
#      `ob_refcnt`.
#
# 7. BEST PRACTICES:
#    - Avoid cyclic references where possible. Use the `weakref` module for parent/child
#      relationships or cache setups.
#    - Avoid manual calls to `gc.collect()` unless you have just freed a large volume
#      of objects in a long-running daemon.
#
# 8. COMMON PITFALLS & PITFALLS:
#    - Overreliance on `__del__` (destructors). In Python versions before 3.4, cyclic
#      references containing objects with `__del__` methods could not be safely GC'd,
#      causing memory leaks. (Fixed by PEP 442, but still considered bad practice to use
#      `__del__` for resource cleanup. Use context managers instead).
#
# 9. INTERVIEW QUESTIONS:
#    - Q: How does reference counting differ from garbage collection?
#      A: Reference counting is deterministic and instantaneous (frees memory when count
#         reaches 0). Cyclic GC is non-deterministic, running periodically to find cyclic
#         graphs of references that cannot be freed by reference counting alone.
#    - Q: Why is `sys.getrefcount(obj)` always 1 higher than expected?
#      A: Calling `getrefcount(obj)` passes the object as an argument to the function,
#         which creates a temporary local reference inside the function call stack.
#
# 10. EXERCISES & SOLUTIONS:
#     - Coding challenge: Create a cyclic reference, verify that standard `del` fails
#       to free the memory, and use the `gc` module to force collect it, verifying the
#       number of collected objects.
#
###############################################################################

import sys  # Standard module for system parameters and object reference inspection
import gc  # Standard module to inspect and control the cyclic garbage collector
import weakref  # Module to create weak references (references that do not increment ref count)

# 1. Inspect Reference Counting Mechanics
# We create a simple list object.
x_list = [1, 2, 3]

# The initial reference count is checked using sys.getrefcount().
# Note: sys.getrefcount(x_list) receives x_list as an argument, incrementing count by 1.
ref_count_1 = sys.getrefcount(x_list)
print(f"Ref count for x_list (includes getrefcount parameter): {ref_count_1}")  # Expected: 2 (x_list, argument)

# Create a new reference pointing to the same list object
y_list = x_list
ref_count_2 = sys.getrefcount(x_list)
print(f"Ref count after y_list = x_list: {ref_count_2}")  # Expected: 3 (x_list, y_list, argument)

# Remove one reference
del y_list
ref_count_3 = sys.getrefcount(x_list)
print(f"Ref count after deleting y_list: {ref_count_3}")  # Expected: 2 (x_list, argument)

# 2. Demonstrate Cyclic References and the Garbage Collector
# Disable garbage collection temporarily to inspect cyclic behavior manually
gc.disable()
print(f"\nGC status: Enabled={gc.isenabled()}")

# Define a Node class that can form reference cycles
class Node:
    def __init__(self, name):
        self.name = name
        self.partner = None

# Create two nodes
node_a = Node("Alpha")
node_b = Node("Beta")

# Form a cycle
node_a.partner = node_b
node_b.partner = node_a

# Delete external references to the nodes.
# Their reference counts will drop by 1, but will remain at 1 because they point to each other.
# Reference counting cannot free this memory because ref counts do not hit 0.
del node_a
del node_b

# Verify the garbage collector can find the cycle
# gc.collect() triggers a manual collection sweep across all generations.
# It returns the number of unreachable objects found and cleared.
print("Triggering manual garbage collection run...")
unreachable_count = gc.collect()
print(f"GC successfully collected cycle objects: {unreachable_count}")  # Expected: >0 (collects the nodes and their __dict__)

# Re-enable GC
gc.enable()

# 3. Weak References Demonstration
# Weak references allow referencing objects without incrementing their reference count,
# preventing reference cycles.
class LargeData:
    def __init__(self, data):
        self.data = data

data_obj = LargeData("Very large string dataset")
# Create a weak reference to the object
weak_ref = weakref.ref(data_obj)

print(f"\nWeak reference points to: {weak_ref()}")  # Returns the object if alive
print(f"Ref count of data_obj: {sys.getrefcount(data_obj)}")  # Weak reference did not increment this

# Delete the strong reference
del data_obj

# The object is immediately collected as there are no strong references remaining
print(f"Weak reference points to (after strong reference deletion): {weak_ref()}")  # Returns None
