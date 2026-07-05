###############################################################################
# TOPIC: Inheritance Introduction - IS-A relationships, syntax, and type validation
#
# 1. DEFINITION & INTRODUCTION:
#    - Inheritance: An OOP mechanism allowing a new class (derived/child class) to inherit
#      attributes and methods from an existing class (base/parent class).
#    - Relationship: Models an **IS-A** relationship.
#      Example: A `Dog` IS-A `Animal`. A `Car` IS-A `Vehicle`.
#    - Syntax: `class ChildClass(ParentClass):`
#
# 2. KEY BENEFITS:
#    - Code Reuse: Subclasses inherit parent methods automatically, preventing duplicate code.
#    - Extensibility: Subclasses can add new attributes or override inherited methods to define
#      specialized behaviors.
#
# 3. INTERPRETER VALIDATION UTILITIES:
#    Python provides built-in functions to verify inheritance chains at runtime:
#    - `isinstance(object, classinfo)`: Returns `True` if `object` is an instance of `classinfo`
#      or a subclass thereof.
#    - `issubclass(class, classinfo)`: Returns `True` if `class` is a subclass of `classinfo`.
#
# 4. METHOD RESOLUTION ORDER (MRO) PREVIEW:
#    - When you call a method on an instance, Python searches the instance's dictionary, then
#      the subclass dictionary, and then proceeds up the parent inheritance tree.
#    - This search path is defined by the Method Resolution Order (MRO), accessible via
#      `ClassName.__mro__`.
#
# 5. BEST PRACTICES:
#    - Ensure the inheritance relationship is a logical "IS-A" mapping. If the relationship
#      is "HAS-A" (e.g. `Car` has an `Engine`), use **Composition** instead of inheritance.
#
# 6. INTERVIEW QUESTIONS:
#    - Q: What does `isinstance(obj, Parent)` return if `obj` is an instance of a subclass of `Parent`?
#      A: `True`. The subclass is a specialization of the parent, so it counts as an instance.
#    - Q: How does Python support code reuse through inheritance?
#      A: By automatically resolving unresolved attribute/method lookups on child instances
#         by searching parent classes upward through the Method Resolution Order (MRO).
#
# 7. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a base `Animal` class, a derived `Mammal` class, and
#      verify their subclass relationships using `issubclass` and `isinstance`.
#
###############################################################################

# 1. Base Class (Parent)
class Animal:
    def __init__(self, name):
        self.name = name
        
    def eat(self):
        print(f" -> {self.name} is eating food.")

# 2. Derived Class (Child)
# Inherits from Animal
class Mammal(Animal):
    def walk(self):
        print(f" -> {self.name} is walking on land.")

print("--- Testing Basic Inheritance ---")
# Instantiate child class
mammal_obj = Mammal("Simba")

# Call inherited method from parent class (Animal)
mammal_obj.eat()  # Expected: "Simba is eating food."

# Call specialized method defined only in subclass
mammal_obj.walk()  # Expected: "Simba is walking on land."

# 3. Runtime Verification (isinstance & issubclass)
print("\n--- Subclass Verification ---")
print(f"Is mammal_obj an instance of Mammal? {isinstance(mammal_obj, Mammal)}")  # Expected: True
print(f"Is mammal_obj an instance of Animal? {isinstance(mammal_obj, Animal)}")  # Expected: True (due to inheritance)
print(f"Is mammal_obj an instance of object? {isinstance(mammal_obj, object)}")  # Expected: True (all classes inherit object)

print(f"\nIs Mammal subclass of Animal? {issubclass(Mammal, Animal)}")  # Expected: True
print(f"Is Animal subclass of Mammal? {issubclass(Animal, Mammal)}")  # Expected: False

# 4. Method Resolution Order (MRO) Inspection
# __mro__ is a tuple showing the search order Python takes to locate methods
print("\n--- Method Resolution Order ---")
print(f"Mammal.__mro__: {Mammal.__mro__}")
# Expected: (Mammal, Animal, object)
