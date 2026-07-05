###############################################################################
# TOPIC: Multiple Inheritance - Diamond Problem, MRO resolution, and super()
#
# 1. DEFINITION & INTRODUCTION:
#    - Multiple Inheritance: A class inherits attributes and methods from more than one
#      immediate parent class.
#      Syntax: `class ChildClass(ParentA, ParentB):`
#
# 2. THE DIAMOND PROBLEM:
#    - A classic problem in multiple inheritance occurs when subclass D inherits from B and C,
#      and both B and C inherit from a common base class A (forming a diamond shape).
#    - If B and C override a method from A, which method should D inherit?
#    - In many languages (like C++), this leads to compilation ambiguity or duplicate base copies.
#    - Python's Solution: The C3 Linearization Algorithm. This algorithm generates a strict,
#      ambiguity-free lookup list for resolving methods (Method Resolution Order).
#
# 3. COOPERATIVE MULTIPLE INHERITANCE (super() Delegation):
#    - To initialize all parent classes correctly, parent constructors must delegate cooperatively
#      using `super().__init__(*args, **kwargs)`.
#    - In multiple inheritance, `super()` does NOT mean "call the parent class".
#      Instead, it means "call the **next class in the MRO list**".
#    - Therefore, calling `super()` inside a class (e.g. B) might actually invoke the initializer
#      of its sibling class (e.g. C) if C comes after B in the MRO!
#    - This cooperative chain requires all classes in the hierarchy to use `super()` and pass on
#      unused arguments using `**kwargs` to prevent runtime crashes.
#
# 4. BEST PRACTICES:
#    - Avoid multiple inheritance unless absolutely necessary, or limit its use to stateless
#      **Mixin** classes (covered later).
#    - Ensure all classes in the multiple inheritance chain call `super().__init__()` with
#      flexible keyword argument parameters (`**kwargs`).
#
# 5. INTERVIEW QUESTIONS:
#    - Q: What does `super()` resolve to in multiple inheritance?
#      A: It resolves to the next class in the current Method Resolution Order (MRO) list,
#         which might be a sibling class rather than a parent class.
#    - Q: How does Python resolve the Diamond Problem?
#      A: By compiling a strict Method Resolution Order (MRO) using the C3 Linearization
#         algorithm, ensuring no class is searched before its subclasses and no parent is
#         searched before child classes.
#
# 6. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a Diamond hierarchy (A, B, C, D) showing how `super().__init__()`
#      traces through all classes in the compiled MRO order.
#
###############################################################################

# 1. Cooperative Multiple Inheritance Setup
# We construct a Diamond hierarchy:
#     Base
#    /    \
#   A      B
#    \    /
#    Derived

class Base:
    def __init__(self, **kwargs):
        print(" -> Base.__init__ entered")
        super().__init__()  # Terminates cooperative chain (calls object.__init__)
        print(" -> Base.__init__ exited")

class LevelA(Base):
    def __init__(self, val_a, **kwargs):
        print(" -> LevelA.__init__ entered")
        # Passes remaining kwargs to the next class in the MRO list
        super().__init__(**kwargs)
        self.val_a = val_a
        print(" -> LevelA.__init__ exited")

class LevelB(Base):
    def __init__(self, val_b, **kwargs):
        print(" -> LevelB.__init__ entered")
        # Passes remaining kwargs to the next class in the MRO
        super().__init__(**kwargs)
        self.val_b = val_b
        print(" -> LevelB.__init__ exited")

class Derived(LevelA, LevelB):
    def __init__(self, val_a, val_b):
        print(" -> Derived.__init__ entered")
        # super() calls LevelA.__init__
        super().__init__(val_a=val_a, val_b=val_b)
        print(" -> Derived.__init__ exited")

# 2. Inspect MRO and Execute Cooperative initialization
print("--- Method Resolution Order ---")
for idx, cls in enumerate(Derived.__mro__):
    print(f"[{idx}] Class: {cls.__name__}")
# Expected MRO list:
# 0: Derived
# 1: LevelA
# 2: LevelB
# 3: Base
# 4: object

print("\n--- Cooperative Initialization trace ---")
# Instantiate Derived
# LevelA.__init__ will execute super(), which resolves to LevelB (its sibling!),
# which in turn calls Base, which terminates.
d_obj = Derived(val_a="Alpha", val_b="Beta")

print("\n--- Attribute Verification ---")
print(f"d_obj.val_a: {d_obj.val_a}")  # Expected: 'Alpha'
print(f"d_obj.val_b: {d_obj.val_b}")  # Expected: 'Beta'
