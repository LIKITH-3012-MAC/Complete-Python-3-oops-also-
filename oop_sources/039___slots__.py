###############################################################################
# TOPIC: __slots__ - Dict bypass, memory optimization, and inheritance behaviors
#
# 1. DEFINITION & INTRODUCTION:
#    - By default, Python class instances store attributes inside a dynamic dictionary `__dict__`.
#      While flexible, dictionaries consume significant memory because they are sparse hash tables.
#    - `__slots__`: A class-level attribute (a tuple of string identifiers) that informs Python
#      to reserve space for only a fixed set of attributes, completely bypassing the creation
#      of `__dict__` and `__weakref__` for instances.
#
# 2. CPYTHON INTERNAL MECHANICS:
#    - When `__slots__` is declared in a class:
#        1. The metaclass `type` does not allocate space for `__dict__` in instance structures.
#        2. Instead, CPython allocates a fixed-size array of pointers directly in the object
#           struct.
#        3. It generates C-level descriptors (member descriptors) for each slot attribute.
#           Accessing `self.x` translates to a direct array offset lookup in C, bypassing
#           hash table evaluations.
#
# 3. PERFORMANCE & MEMORY BENEFITS:
#    - Memory: Drastic footprint reduction (up to 70% to 80% memory savings), highly critical
#      when instantiating millions of small objects (like nodes in a graph or coordinates).
#    - Speed: Attribute access runs roughly 15% to 25% faster due to direct C-array indexing.
#    - Constraint: Prevents dynamic attribute addition (monkey patching). Attempting to write
#      an attribute not declared in `__slots__` raises an `AttributeError`.
#
# 4. INHERITANCE RULES:
#    - Subclass slots inheritance: Subclasses do not inherit `__slots__` automatically.
#      If parent has `__slots__` and child defines no `__slots__`, the child class instance
#      **will get a `__dict__`**, losing the memory benefit!
#    - To keep the optimization, the child class must declare `__slots__ = ()` (empty tuple) or
#      declare its own additional slots.
#
# 5. INTERVIEW QUESTIONS:
#    - Q: How does `__slots__` reduce memory usage?
#      A: It prevents CPython from allocating a `__dict__` dictionary for every instance, storing
#         attributes in a fixed-size array of pointers accessed via descriptors.
#    - Q: What happens if a subclass does not declare `__slots__` when the parent did?
#      A: The subclass instances will allocate a `__dict__` dictionary, losing the memory savings
#         for subclass-defined attributes.
#
# 6. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a class with and without `__slots__`, instantiate 1 million
#      objects of each, and measure memory usage differences using `tracemalloc`.
#
###############################################################################

import sys  # Standard library to check object sizes
import tracemalloc  # standard library module to trace memory allocations

# 1. Class declarations
class StandardCoordinates:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class SlottedCoordinates:
    # Restrict attributes to x and y only
    __slots__ = ("x", "y")
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

# 2. Testing Constraints (No Monkey Patching)
std = StandardCoordinates(1, 2)
slot = SlottedCoordinates(1, 2)

print("--- Testing Slots Write Constraints ---")
# Standard instance supports monkey patching
std.z = 100
print(f"Standard dict: {std.__dict__}")

# Slotted instance blocks monkey patching
try:
    slot.z = 100
except AttributeError as e:
    print(f"Caught expected AttributeError on slotted write: {e}")

# Verify slots instance has no __dict__
print(f"Does Slotted instance have __dict__? {hasattr(slot, '__dict__')}")  # Expected: False

# 3. Memory Allocation Benchmark (tracemalloc)
def benchmark_memory():
    tracemalloc.start()
    
    # Measure Standard Class allocations
    snapshot1 = tracemalloc.take_snapshot()
    std_instances = [StandardCoordinates(i, i+1) for i in range(50000)]
    snapshot2 = tracemalloc.take_snapshot()
    
    # Measure memory difference
    stats = snapshot2.compare_to(snapshot1, "lineno")
    total_std_mem = sum(stat.size_diff for stat in stats)
    
    # Clear instances to reset memory trace
    del std_instances
    gc_collected = gc.collect() if "gc" in sys.modules else 0
    
    # Measure Slotted Class allocations
    snapshot3 = tracemalloc.take_snapshot()
    slot_instances = [SlottedCoordinates(i, i+1) for i in range(50000)]
    snapshot4 = tracemalloc.take_snapshot()
    
    stats_slot = snapshot4.compare_to(snapshot3, "lineno")
    total_slot_mem = sum(stat.size_diff for stat in stats_slot)
    
    print("\n--- Memory Allocation Benchmark (50,000 instances) ---")
    print(f"Standard Class memory usage: {total_std_mem / 1024:.2f} KB")
    print(f"Slotted Class memory usage:  {total_slot_mem / 1024:.2f} KB")
    print(f"Slots save roughly {100 - (total_slot_mem / total_std_mem * 100):.1f}% memory!")

benchmark_memory()
tracemalloc.stop()
