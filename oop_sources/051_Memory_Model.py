###############################################################################
# TOPIC: Python Memory Model - Stack vs Heap allocations, reference counting, and cyclic GC
#
# 1. DEFINITION & SCOPES:
#    - Stack: Stores active execution frames. Holds local variable name pointers,
#      which are references referencing addresses on the private heap.
#    - Heap: CPython's private heap memory block where all objects (integers, strings, custom class
#      instances) and their attributes are allocated.
#
# 2. REFERENCE COUNTING MECHANISM:
#    - Every Python object structure maintains a reference count `ob_refcnt`.
#    - When you assign an object reference to a variable, write it to a list, or pass it to a
#      function, the count increases.
#    - When a variable goes out of scope, is reassigned, or deleted, the count decreases.
#    - When `ob_refcnt` hits exactly **zero**, CPython immediately deallocates the object, returning
#      its memory block back to the heap allocator (PyMalloc or system heap).
#
# 3. CYCLIC GARBAGE COLLECTION:
#    - Reference counting cannot reclaim objects trapped in **reference cycles** (e.g. A references B,
#      and B references A, but neither has active external references from the stack).
#    - CPython solves this using a **Cyclic Garbage Collector** running in the background.
#    - Generational GC: It organizes container objects (lists, dicts, custom objects) into three
#      generations (Gen 0, 1, 2) based on survival history.
#    - Sweeping: It runs periodically, detecting cycles by temporarily decrementing internal counts
#      and identifying groups that have no external connections, then executing finalizers.
#
# 4. MEASURING MEMORY AND OBJECT SIZES:
#    - `sys.getsizeof(object)`: Returns the memory footprint size (in bytes) of the object structure
#      itself (including C headers), but does not recursively add the sizes of nested objects referenced
#      inside container arrays.
#
# 5. INTERVIEW QUESTIONS:
#    - Q: What happens to memory cleanup when reference count hits 0?
#      A: CPython immediately frees the object's memory. This is deterministic and instantaneous.
#    - Q: Why does Python need a cyclic garbage collector if it has reference counting?
#      A: Reference counting cannot detect self-referencing loops (cycles) where objects point to
#         each other but are unreachable from the active stack namespace.
#
# 6. EXERCISES & SOLUTIONS:
#    - Coding challenge: Inspect reference counts using `sys.getrefcount`, track object sizes
#      using `sys.getsizeof`, and verify container sizes.
#
###############################################################################

import sys  # Standard module containing getrefcount and getsizeof
import gc  # Standard module controlling the cyclic garbage collector

# 1. Reference Counting Verification
print("--- Reference Count Tracing ---")
a = [1, 2, 3]  # Heap list instantiated
# sys.getrefcount(obj) returns count. Note: it includes temporary reference inside getrefcount!
# So count shown is always actual count + 1.
print(f"Ref count of 'a' (expected 2 due to temp): {sys.getrefcount(a)}")

b = a  # Assign second variable reference
print(f"Ref count of 'a' after b = a (expected 3): {sys.getrefcount(a)}")

c = [a]  # Add inside container list
print(f"Ref count of 'a' after inside list (expected 4): {sys.getrefcount(a)}")

# Releasing references
print("\nReleasing references...")
del c
del b
print(f"Ref count after deletes (expected 2): {sys.getrefcount(a)}")

# 2. sys.getsizeof vs Deep Size
print("\n--- Object Memory footprints ---")
empty_dict = {}
populated_dict = {i: i for i in range(100)}

print(f"Empty dict size:      {sys.getsizeof(empty_dict)} bytes")
print(f"Populated dict size:  {sys.getsizeof(populated_dict)} bytes")

# Notice size of class instances
class Node:
    def __init__(self, val):
        self.val = val

n = Node(10)
print(f"Custom Node size (only struct headers, not dict): {sys.getsizeof(n)} bytes")
print(f"Node dictionary size (stores attributes):         {sys.getsizeof(n.__dict__)} bytes")

# 3. Interacting with Cyclic Garbage Collector
# Print GC thresholds (thresholds for triggering collection sweeps across Gen 0, 1, 2)
print("\n--- Garbage Collector Thresholds ---")
print(f"GC generational thresholds: {gc.get_threshold()}")

# We can manually enable/disable GC sweeps
gc.disable()
print("GC background sweeps disabled.")
# Perform cycles creations ...
gc.enable()
print("GC background sweeps re-enabled.")
