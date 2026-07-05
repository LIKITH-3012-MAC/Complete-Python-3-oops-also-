###############################################################################
# TOPIC: Object-Oriented Programming (OOP) Introduction
#
# 1. DEFINITION & INTRODUCTION:
#    - Object-Oriented Programming (OOP) is a programming paradigm based on the concept
#      of "objects", which contain data (attributes/properties) and code (methods).
#    - Python is a multi-paradigm language, supporting procedural, functional, and
#      object-oriented programming.
#    - The four core pillars of OOP are:
#        1. Encapsulation: Grouping state (data) and behavior (methods) together into a
#           single unit, restricting direct access to some of the object's components.
#        2. Abstraction: Hiding internal complexity and exposing only necessary interfaces.
#        3. Inheritance: Reusing and extending features of existing classes in new classes.
#        4. Polymorphism: Allowing different classes to respond to the same interface or method call
#           in their own specific way.
#
# 2. HISTORY & MOTIVATION:
#    - The concept of OOP originated in the 1960s with Simula-67 and was popularized by Smalltalk
#      in the 1970s.
#    - Guido van Rossum designed Python from the ground up to support classes and objects.
#    - Motivation: To manage growing software complexity by mapping program structures to real-world
#      entities, encouraging modularity, code reuse, and high-level structural modeling.
#
# 3. CPYTHON CLASS INTERNALS & TYPE SYSTEM:
#    - In Python, **everything is an object**, including numbers, strings, functions, and classes
#      themselves.
#    - CPython Object Struct (`PyObject`): Every object has a type pointer `ob_type`.
#    - Type of Type: The type of a class is `type` (metaclass).
#      Example: If you define class `MyClass`, the type of an instance of `MyClass` is `MyClass`,
#      and the type of `MyClass` is `type`.
#    - Dynamic Attributes: By default, objects store their instance attributes inside a dictionary
#      called `__dict__`. Class attributes are stored in the class's dictionary `__dict__` (proxied
#      by `mappingproxy` to prevent direct modification of class namespaces).
#
# 4. TIME & SPACE COMPLEXITY:
#    - Class definition: O(1) overhead during compilation.
#    - Attribute lookup: O(1) average-case (dictionary lookup).
#
# 5. BEST PRACTICES:
#    - Use OOP when you need to model stateful, long-lived entities with complex relationships.
#      Do not force OOP when a simple procedural function or module is cleaner.
#
# 6. INTERVIEW QUESTIONS:
#    - Q: What are the four pillars of OOP?
#      A: Encapsulation, Abstraction, Inheritance, and Polymorphism.
#    - Q: What is the type of a class in Python?
#      A: `type`. The `type` metaclass is the factory that constructs all Python classes.
#
# 7. EXERCISES & SOLUTIONS:
#    - MCQ: Which of the following statements is true?
#           a) Only user-defined classes are objects in Python.
#           b) Everything in Python, including functions and classes, is an object.
#       Answer: b.
#    - Coding challenge: Implement a simple class demonstrating the four pillars of OOP.
#
###############################################################################

# 1. Verify that Class is an Object (type system)
class SimpleClass:
    """A minimal class representing OOP concept foundations."""
    pass

# Instantiate class
instance = SimpleClass()

print("--- Type System Verification ---")
print(f"Type of instance: {type(instance)}")  # Expected: <class '__main__.SimpleClass'>
print(f"Type of SimpleClass (the class itself): {type(SimpleClass)}")  # Expected: <class 'type'>

# 2. Demonstrating the 4 Pillars of OOP in a Single Codebase
# Parent Class (Abstraction & Inheritance foundation)
class Vehicle:
    def __init__(self, make, model):
        self.make = make        # Instance attribute
        self.model = model      # Instance attribute
        self._speed = 0         # Encapsulated attribute (single underscore indicates protected)
        
    def start_engine(self):
        # Abstraction: Caller does not know internal engine steps, just triggers start
        self._ignite_spark()
        print(f"Engine of {self.make} {self.model} started.")
        
    def _ignite_spark(self):
        # Internal helper method
        pass
        
    def move(self):
        # Base implementation of Polymorphic method
        print("Vehicle is moving...")

# Child Class (Inheritance & Polymorphism)
class Car(Vehicle):
    def __init__(self, make, model, doors):
        # Inherit constructor from parent
        super().__init__(make, model)
        self.doors = doors
        
    def move(self):
        # Polymorphism: Overriding the parent's move method
        print(f"Car {self.make} is driving on roads at {self._speed} km/h.")
        
    def accelerate(self, increment):
        # Encapsulation: We control how _speed is modified
        if increment > 0:
            self._speed += increment
            print(f"Accelerated to {self._speed} km/h.")

# Test code
car_obj = Car("Toyota", "Camry", 4)
print("\n--- Testing OOP Pillars ---")
car_obj.start_engine()  # Abstraction: runs spark ignition internally
car_obj.accelerate(50)  # Encapsulation: alters protected _speed safely
car_obj.move()          # Polymorphism: executes Car.move overriding Vehicle.move
