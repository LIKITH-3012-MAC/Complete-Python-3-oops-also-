###############################################################################
# TOPIC: Protocols - Structural Typing, PEP 544, and runtime checkable interfaces
#
# 1. DEFINITION & INTRODUCTION:
#    - Protocol (introduced in Python 3.8 via PEP 544): Enables **Structural Typing**
#      (also known as Static Duck Typing).
#    - Declared by subclassing `typing.Protocol`.
#
# 2. NOMINAL VS STRUCTURAL SUBTYPING:
#    - Nominal Subtyping (Abstract Base Classes - ABC): Type compatibility is determined by
#      explicit class inheritance names (e.g. `class Dog(Animal):`).
#    - Structural Subtyping (Protocol): Type compatibility is determined by the class structure
#      (i.e. what methods and fields it defines), regardless of explicit inheritance links.
#
# 3. STATIC TYPE CHECKING & RUNTIME CHECKS:
#    - Static Type Checkers (like MyPy or Pyright) use Protocols to verify that arguments passed
#      to typed parameters implement all required methods.
#    - Runtime Checks: By default, you cannot run `isinstance(obj, MyProtocol)` (raises TypeError).
#    - To enable runtime checks, decorate the Protocol class with `@typing.runtime_checkable`.
#      This allows `isinstance()` and `issubclass()` checks to verify structure at runtime.
#
# 4. BEST PRACTICES:
#    - Use `Protocol` when you want to define a loose, structural contract (static duck typing)
#      that other classes can satisfy without creating tight, explicit inheritance dependencies.
#
# 5. INTERVIEW QUESTIONS:
#    - Q: What is the difference between Nominal Typing and Structural Typing?
#      A: Nominal typing checks class inheritance hierarchies (names); Structural typing checks
#         the existence of method/attribute structures (shapes).
#    - Q: How can you run `isinstance()` checks on a Protocol?
#      A: By decorating the Protocol class with `@typing.runtime_checkable`.
#
# 6. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a `Renderable` Protocol containing a `render` method,
#      decorate it as runtime checkable, implement unrelated classes that satisfy the protocol,
#      and execute runtime validations.
#
###############################################################################

from typing import Protocol, runtime_checkable  # standard typing module elements

# 1. Define Structural Protocol
# We decorate it as runtime checkable to support isinstance() checks during execution
@runtime_checkable
class Flyable(Protocol):
    # Protocols define signatures only (body is pass or Ellipsis)
    def fly(self) -> str:
        ...

# 2. Implement classes (No explicit inheritance of Flyable)
class Airplane:
    def fly(self) -> str:
        return "Airplane is cruising using jet engines."

class Bird:
    def fly(self) -> str:
        return "Bird is flapping its wings."

class Fish:
    def swim(self) -> str:
        return "Fish is swimming."

# 3. Client function annotated with Protocol
def execute_flight(flyer: Flyable):
    # Static type checkers verify that flyer has a .fly() method returning a string.
    print(f"[Flight Control]: {flyer.fly()}")

print("--- Testing Protocol Conformance (Static Duck Typing) ---")
plane = Airplane()
robin = Bird()

# Both work because they implement the required structural methods!
execute_flight(plane)
execute_flight(robin)

# 4. Runtime checks using isinstance()
# Supported because of @runtime_checkable decorator
print("\n--- Runtime Protocol checks ---")
print(f"Is plane an instance of Flyable? {isinstance(plane, Flyable)}")  # Expected: True
print(f"Is robin an instance of Flyable? {isinstance(robin, Flyable)}")  # Expected: True

fish = Fish()
print(f"Is fish an instance of Flyable?  {isinstance(fish, Flyable)}")   # Expected: False
print(f"Is Fish a subclass of Flyable?     {issubclass(Fish, Flyable)}")    # Expected: False
