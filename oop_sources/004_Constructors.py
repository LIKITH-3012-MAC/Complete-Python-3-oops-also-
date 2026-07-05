###############################################################################
# TOPIC: Constructors - Parameters, defaults, and Constructor Overloading alternatives
#
# 1. DEFINITION & INTRODUCTION:
#    - Python classes combine `__new__` and `__init__` to perform object construction.
#    - The initializer `__init__` defines the parameters required to construct an object.
#
# 2. CONSTRUCTOR OVERLOADING RESTRICTION:
#    - In languages like C++, Java, or C#, you can overload constructors by defining multiple
#      constructor functions with different parameter signatures.
#    - Python does NOT support this. Since Python namespace lookups resolve keys in a dictionary
#      (where a name can point to only one object), defining a second `__init__` method simply
#      shadows and overwrites the first one.
#
# 3. OVERLOADING ALTERNATIVES:
#    To achieve constructor overloading behaviors in Python, we use two main patterns:
#    - Method A: Variable parameter types or default values inside `__init__` combined with
#      type checks (`isinstance()`).
#    - Method B: Factory classmethods (Recommended). Define a primary constructor, and create
#      alternative classmethods (e.g. `from_string`, `from_json`) that parse inputs and call
#      the primary constructor, returning the initialized instance.
#
# 4. BEST PRACTICES:
#    - Use factory classmethods for distinct initialization workflows. It is cleaner and
#      more readable than writing complex, branch-heavy type checks inside a single `__init__`.
#    - Document the expected parameter formats in the class docstring.
#
# 5. INTERVIEW QUESTIONS:
#    - Q: Can you write two `__init__` methods in a single Python class?
#      A: You can, but Python will not overload them. The second definition will completely
#         shadow/overwrite the first one, rendering the first definition inaccessible.
#    - Q: What are factory methods and why are they used in Python OOP?
#      A: They are class methods (decorated with `@classmethod`) that act as alternative
#         constructors, parsing diverse data formats and returning an instantiated object.
#
# 6. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a `Point` class that can be initialized using coordinates
#      (x, y), or parsed from a comma-separated string, or from a dictionary, using factory methods.
#
###############################################################################

import json  # standard library module to parse serialized JSON data

class Point:
    def __init__(self, x, y):
        # The primary constructor accepts numeric coordinates
        self.x = x
        self.y = y
        
    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"
        
    # Alternative Constructor 1: Parse from string (e.g., "10,20")
    @classmethod
    def from_string(cls, coord_str):
        # Splits the string and converts items to float
        parts = coord_str.split(",")
        if len(parts) != 2:
            raise ValueError("String must be formatted as 'x,y'")
        x_val, y_val = float(parts[0]), float(parts[1])
        # Instantiates the class (cls) using the primary constructor
        return cls(x_val, y_val)
        
    # Alternative Constructor 2: Parse from dictionary (e.g. {"x": 10, "y": 20})
    @classmethod
    def from_dict(cls, coord_dict):
        # Extracts x and y keys
        return cls(coord_dict["x"], coord_dict["y"])
        
    # Alternative Constructor 3: Parse from JSON string
    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls(data["x"], data["y"])

print("--- Instantiating using primary constructor ---")
p1 = Point(5, 10)
print(f"Primary Point: {p1}")

print("\n--- Instantiating using Factory Methods ---")
# Call from_string classmethod
p2 = Point.from_string("15.5,30.0")
print(f"From String:   {p2}")

# Call from_dict classmethod
p3 = Point.from_dict({"x": 100, "y": 200})
print(f"From Dict:     {p3}")

# Call from_json classmethod
json_payload = '{"x": -50, "y": -75}'
p4 = Point.from_json(json_payload)
print(f"From JSON:     {p4}")

# Demonstrating why multiple __init__ methods fail:
class OverwriteTest:
    def __init__(self, name):
        self.name = name
        
    def __init__(self, name, age):  # Overwrites the 1-parameter __init__!
        self.name = name
        self.age = age

try:
    # Attempting to call the 1-parameter constructor (fails!)
    ot = OverwriteTest("Alice")
except TypeError as e:
    print(f"\nCaught expected TypeError (calling shadowed constructor): {e}")
