###############################################################################
# TOPIC: Destructors (__del__), Reference Counting trigger, and PEP 442 Finalization
#
# 1. DEFINITION & INTRODUCTION:
#    - Destructor: The magic method `__del__(self)` called when an object is about to be
#      destroyed.
#    - Trigger: Executed when the object's reference count reaches exactly zero.
#
# 2. NON-DETERMINISTIC BEHAVIOR & PITFALLS:
#    - Python developers should NOT rely on `__del__` for critical resource management
#      (like closing files, database connections, or socket release), because `__del__`
#      execution is non-deterministic.
#    - Why it is unreliable:
#        1. Delayed GC: If an object is part of a reference cycle, it will not be destroyed
#           by reference counting. It remains in memory until the cyclic GC sweeps, which
#           happens at arbitrary runtime intervals.
#        2. Interpreter Shutdown: Objects remaining at program termination are garbage collected
#           in an arbitrary order during interpreter teardown. At that stage, global variables
#           or modules referenced inside `__del__` might have already been set to `None`,
#           causing exceptions inside the destructor.
#
# 3. PEP 442 - SAFE OBJECT FINALIZATION:
#    - In Python versions prior to 3.4, if objects forming a reference cycle implemented a
#      `__del__` method, CPython's GC would refuse to collect them. This was because the
#      interpreter did not know which object's destructor to call first without potentially
#      passing a half-destroyed sibling reference.
#    - These un-collectable objects were placed in a global list `gc.garbage` and leaked.
#    - Python 3.4 introduced PEP 442, which allows the cyclic GC to safely finalize and tear down
#      objects with `__del__` in cycles, making destructor cycles collectable.
#
# 4. BEST PRACTICES:
#    - Use context managers (`with` statements) or explicit `close()` methods to manage external
#      system resources.
#    - Keep `__del__` methods as simple as possible, or avoid defining them altogether.
#
# 5. INTERVIEW QUESTIONS:
#    - Q: When is `__del__` called?
#      A: It is called when the reference count of an object reaches 0. This can happen due to
#         explicit deletion (`del`), reassigning the variable name, or leaving a scope.
#    - Q: Why is it bad practice to close database connections inside `__del__`?
#      A: Because its execution is non-deterministic. The connection could remain open in memory
#         for a long time if the object is captured in a reference cycle, leaking database resources.
#
# 6. EXERCISES & SOLUTIONS:
#    - Coding challenge: Create an object, show how deleting variables triggers `__del__`,
#      form a reference cycle, and demonstrate how `__del__` is delayed until manual GC run.
#
###############################################################################

import gc  # Standard library to control the garbage collector
import sys  # Standard library to track reference counts

class ResourceTracker:
    def __init__(self, resource_name):
        self.name = resource_name
        print(f" -> Resource '{self.name}' initialized.")
        
    def __del__(self):
        # Destructor prints message when deleted
        print(f" -> Resource '{self.name}' DESTROYED (destructor run).")

# 1. Deterministic destruction (Reference count hits 0)
print("--- Case A: Immediate reference count zeroing ---")
res1 = ResourceTracker("First")
# Increase reference count
res2 = res1
print(f"Ref count of res1 (via sys.getrefcount): {sys.getrefcount(res1)}")

print("Deleting res1 reference...")
del res1  # reference count drops but remains 1 (held by res2)
print("Res1 deleted. Checking if destructor ran (it should not have yet).")

print("Deleting res2 reference...")
del res2  # reference count hits 0, triggers __del__ immediately
print("Res2 deleted.")

# 2. Delayed destruction due to Reference Cycle
print("\n--- Case B: Reference Cycle delay ---")
class CyclicResource:
    def __init__(self, name):
        self.name = name
        self.partner = None
        print(f" -> CyclicResource '{self.name}' initialized.")
        
    def __del__(self):
        print(f" -> CyclicResource '{self.name}' DESTROYED.")

node_a = CyclicResource("NodeA")
node_b = CyclicResource("NodeB")

# Create the reference cycle
node_a.partner = node_b
node_b.partner = node_a

# Delete external pointers
print("Deleting external pointers to cycle nodes...")
del node_a
del node_b
print("External references deleted. Destructors have not run due to reference cycle!")

# Trigger cyclic garbage collection manually to force finalization (PEP 442)
print("Triggering manual cyclic garbage collection...")
gc.collect()  # Collects cycle and executes destructors
print("GC complete.")
