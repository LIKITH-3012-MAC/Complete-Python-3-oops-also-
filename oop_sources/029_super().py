###############################################################################
# TOPIC: super() - dynamic MRO proxies, explicit parameters, and execution bounds
#
# 1. DEFINITION & INTRODUCTION:
#    - `super()`: A built-in function that returns a proxy object delegating method calls
#      to a parent or sibling class in the Method Resolution Order (MRO).
#    - Key utility: Crucial for cooperative multiple inheritance and single inheritance overrides.
#
# 2. HOW `super()` WORKS UNDER THE HOOD:
#    - Signature: `super([type [, object-or-type]])`
#    - Modern Python 3 Zero-Argument Syntax:
#        - Inside an instance method, calling `super()` is bytecode-equivalent to:
#          `super(__class__, self)`
#        - Python's compiler automatically inserts the closure variable `__class__` (representing
#          the class where the method is defined) and the first argument `self` (the instance).
#    - The Dynamic Proxy Object:
#        - `super()` returns a descriptor-based proxy object.
#        - When you call a method on this proxy (e.g. `super().method()`), the proxy searches the
#          MRO list of the **instance (`self`)**, starting *after* the class `__class__`.
#        - Crucial Rule: The search order is determined by the instance's MRO, NOT the parent
#          definition order of the current file! This is why sibling methods can be invoked.
#
# 3. EXPLICIT PARAMETER CALLS:
#    - You can call `super(ClassName, instance)` explicitly. This instructs Python: "Search the MRO
#      of `instance` starting immediately after `ClassName`."
#    - Highly useful for bypassing intermediate overrides in complex class hierarchies.
#
# 4. INTERVIEW QUESTIONS:
#    - Q: What does calling `super()` without arguments actually do in Python 3?
#      A: It dynamically retrieves the class it was called from (`__class__`) and the active
#         instance (`self`), returning a proxy that delegates calls to classes further down the MRO.
#    - Q: Why might `super().work()` call a sibling class method instead of a parent class method?
#      A: Because `super()` resolves methods according to the MRO of the calling instance. In multiple
#         inheritance, a sibling class can follow the current class in the instance's MRO sequence.
#
# 5. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a class hierarchy where a subclass method calls a grandparent's
#      method directly, bypassing the parent class's override, using explicit parameters in `super()`.
#
###############################################################################

# 1. Grandparent, Parent, Child Hierarchy
class Grandparent:
    def greet(self):
        print("Hello from Grandparent!")

class Parent(Grandparent):
    def greet(self):
        print("Hello from Parent!")

class Child(Parent):
    def greet(self):
        # Standard zero-argument super() calls immediate parent (Parent)
        print("--- Standard super() call ---")
        super().greet()  # Expected: calls Parent.greet()
        
    def greet_grandparent(self):
        # Explicit parameter super(Type, self)
        # We tell Python: search the MRO of self, starting AFTER class 'Parent'.
        # Since the MRO of Child is (Child, Parent, Grandparent, object),
        # searching after Parent resolves directly to Grandparent!
        print("\n--- Explicit super(Parent, self) call ---")
        super(Parent, self).greet()  # Expected: calls Grandparent.greet()

child_obj = Child()
child_obj.greet()
child_obj.greet_grandparent()

# 2. Dynamic binding proof
# We will show how super() binds to the MRO of the instance (not the class of the source code file).
class SiblingA:
    def run(self):
        print("Entering SiblingA")
        # In SiblingA, super() looks for the next class in self's MRO.
        # If we instantiated SiblingA directly, its MRO is (SiblingA, object), so super() finishes.
        # But if instantiated as part of HybridChild, the MRO has SiblingB after SiblingA!
        super().run()
        print("Exiting SiblingA")

class SiblingB:
    def run(self):
        print("Entering SiblingB (sibling)")
        # SiblingB has no parent other than object, but cooperates
        # super().run() would fail on object, so we catch or verify.
        # But here we show it gets resolved.
        print("Exiting SiblingB")

class HybridChild(SiblingA, SiblingB):
    def run(self):
        print("Entering HybridChild")
        super().run()  # Calls SiblingA.run()
        print("Exiting HybridChild")

print("\n--- Sibling Resolution Trace ---")
child_hybrid = HybridChild()
print(f"HybridChild MRO: {[c.__name__ for c in HybridChild.__mro__]}")
# MRO: HybridChild -> SiblingA -> SiblingB -> object

# Execute run
# Notice how SiblingA's super().run() successfully calls SiblingB.run()!
# This proves super() searches the instance's MRO, not SiblingA's parents.
child_hybrid.run()
