###############################################################################
# TOPIC: Hierarchical Inheritance - Shared interfaces, child specializations, and polymorphism
#
# 1. DEFINITION & INTRODUCTION:
#    - Hierarchical Inheritance: Multiple child subclasses inherit directly from a single
#      parent base class.
#      Hierarchy Shape:
#             Parent
#            /   |   \
#         Child1 Child2 Child3
#
# 2. CORE CHARACTERISTICS:
#    - Shared Base: All subclasses share the same parent attributes and methods.
#    - Diverse Specializations: Each subclass defines its own specialized behaviors or extensions
#      unique to its type.
#    - Polymorphism: Standard implementation model where parent references can point to any child
#      instance, executing child-overridden methods dynamically at runtime.
#
# 3. BEST PRACTICES:
#    - Use hierarchical inheritance to define a standard set of attributes or method signatures
#      (interfaces) in the parent class that all child classes are guaranteed to support.
#
# 4. INTERVIEW QUESTIONS:
#    - Q: Give a real-world example of hierarchical inheritance.
#      A: A base class `Shape` containing a `color` attribute, and subclasses `Circle`, `Square`,
#         and `Triangle` each overriding a `calculate_area()` method.
#    - Q: Do siblings in a hierarchical inheritance tree share namespaces?
#      A: No. Each subclass has its own distinct namespace dictionary, sharing only what is
#         defined in the parent class namespace.
#
# 5. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a base `Shape` class, and derived `Circle` and `Rectangle`
#      subclasses. Demonstrate polymorphic calculation of areas of diverse shapes in a loop.
#
###############################################################################

import math  # standard library module to compute pi

# 1. Parent Base Class
class Shape:
    def __init__(self, color):
        self.color = color
        
    def get_description(self):
        return f"A {self.color} shape."
        
    def calculate_area(self):
        # Base method, to be overridden by subclasses
        raise NotImplementedError("Subclasses must override calculate_area()!")

# 2. Child Class 1 (Circle)
class Circle(Shape):
    def __init__(self, color, radius):
        super().__init__(color)
        self.radius = radius
        
    def calculate_area(self):
        # Circle area formula: pi * r^2
        return math.pi * (self.radius ** 2)
        
    def get_description(self):
        return f"A {self.color} Circle with radius {self.radius}."

# 3. Child Class 2 (Rectangle)
class Rectangle(Shape):
    def __init__(self, color, width, height):
        super().__init__(color)
        self.width = width
        self.height = height
        
    def calculate_area(self):
        # Rectangle area formula: width * height
        return self.width * self.height
        
    def get_description(self):
        return f"A {self.color} Rectangle with dimensions {self.width}x{self.height}."

# 4. Testing Hierarchical Inheritance & Polymorphism
shapes_list = [
    Circle("Red", 5.0),
    Rectangle("Blue", 4.0, 6.0),
    Circle("Green", 2.5)
]

print("--- Polymorphic Shape Evaluation ---")
for shape in shapes_list:
    # Executing parent and overridden methods polymorphically
    print(shape.get_description())
    print(f"  Calculated Area: {shape.calculate_area():.2f}")
    
# 5. Verify inheritance relations
print("\n--- Subclass Check ---")
print(f"Is Circle subclass of Shape? {issubclass(Circle, Shape)}")  # Expected: True
print(f"Is Rectangle subclass of Shape? {issubclass(Rectangle, Shape)}")  # Expected: True
print(f"Is Circle subclass of Rectangle? {issubclass(Circle, Rectangle)}")  # Expected: False
