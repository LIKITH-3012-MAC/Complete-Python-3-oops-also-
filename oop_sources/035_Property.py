###############################################################################
# TOPIC: Property - @property decorator, read-only accessors, and descriptor engines
#
# 1. DEFINITION & INTRODUCTION:
#    - `@property`: A built-in decorator that allows wrapping a method and exposing it as if
#      it were a standard read-only attribute (e.g. `obj.name` instead of calling `obj.name()`).
#    - Motivation: Encapsulation. Allows developers to expose a public attribute interface while
#      maintaining the freedom to change the underlying implementation (e.g. calculating values
#      on-the-fly) without breaking client code that accesses it as a simple field.
#
# 2. UNDER-THE-HOOD DESCRIPTOR ENGINE:
#    - In Python, the `property` decorator is implemented as a class that conforms to the
#      **Descriptor Protocol**.
#    - When you decorate a method inside a class:
#      ```python
#      @property
#      def value(self): return self._value
#      ```
#      Python instantiates a `property` descriptor object and binds it to the class attribute
#      `value` inside the class `__dict__`.
#    - When you call `instance.value`, Python's lookup detects that the class attribute `value`
#      is a descriptor implementing the `__get__` method. It calls `value.__get__(instance, Class)`
#      internally, executing your getter function and returning the output.
#
# 3. BEST PRACTICES:
#    - Use properties to expose attributes that require light computations, data conversions
#      (e.g., combining first and last name), or lazy evaluation.
#    - Avoid placing slow, heavy-weight computations (like database queries or network requests)
#      inside properties; callers expect attribute reads to be near-instantaneous O(1) operations.
#
# 4. INTERVIEW QUESTIONS:
#    - Q: How does the `@property` decorator work under the hood?
#      A: It creates an instance of the built-in `property` descriptor class, which implements
#         the `__get__` magic method of the descriptor protocol, routing attribute access calls
#         to the decorated getter function.
#    - Q: What happens if you try to assign a value to a property that has no setter defined?
#      A: Python raises an `AttributeError: can't set attribute`.
#
# 5. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a `Circle` class that takes a radius in its constructor and
#      exposes the area as a read-only property, updating automatically if radius changes.
#
###############################################################################

import math  # standard library module to compute pi

class Circle:
    def __init__(self, radius):
        self.radius = radius
        
    # Read-only property: exposes calculation as an attribute
    @property
    def area(self):
        # Calculated dynamically on-the-fly
        print(" -> [Property Getter] Calculating circle area...")
        return math.pi * (self.radius ** 2)

c = Circle(5.0)
print("--- Accessing Property ---")
# Notice we do NOT use parenthesis like c.area(); we access it as a field.
print(f"Initial Radius: {c.radius}")
print(f"Area:           {c.area:.4f}")  # Expected: 78.5398

# Modify radius
c.radius = 10.0
# The property area updates automatically on next read!
print(f"\nNew Radius:     {c.radius}")
print(f"New Area:       {c.area:.4f}")  # Expected: 314.1593

# 2. Attempting to assign value to read-only property
try:
    c.area = 500.0  # Fails because no setter is configured
except AttributeError as e:
    print(f"\nCaught expected AttributeError (read-only write attempt): {e}")

# 3. Verifying the descriptor object in class dict
descriptor_obj = Circle.__dict__["area"]
print(f"\nType of Circle.area descriptor: {type(descriptor_obj)}")  # Expected: <class 'property'>
print(f"Does it implement __get__?    {hasattr(descriptor_obj, '__get__')}")  # Expected: True
