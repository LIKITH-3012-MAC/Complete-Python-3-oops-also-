###############################################################################
# TOPIC: Operator Overloading - Mathematical, comparison, and indexer magic methods
#
# 1. DEFINITION & INTRODUCTION:
#    - Operator Overloading: Customizing the behavior of Python's built-in operators
#      (like `+`, `*`, `<`, `==`, `[]`) when applied to custom class instances.
#    - Achieved by implementing corresponding magic (dunder) methods in the class.
#
# 2. OVERLOADABLE OPERATORS CATEGORIES:
#    - Mathematical Operators:
#        - Addition: `__add__(self, other)`
#        - Subtraction: `__sub__(self, other)`
#        - Multiplication: `__mul__(self, other)`
#    - Comparison Operators (Rich Comparisons):
#        - Less than: `__lt__(self, other)`
#        - Less or equal: `__le__(self, other)`
#        - Greater than: `__gt__(self, other)`
#        - Greater or equal: `__ge__(self, other)`
#        - Equal to: `__eq__(self, other)`
#        - Not equal to: `__ne__(self, other)`
#    - Indexing and Slicing:
#        - Read index: `__getitem__(self, key)`
#        - Write index: `__setitem__(self, key, value)`
#        - Delete index: `__delitem__(self, key)`
#
# 3. REFLECTED AND IN-PLACE OPERATORS:
#    - Reflected/Reverse: `__radd__(self, other)` is called when left-hand operand does not
#      support addition with the class type.
#    - In-place: `__iadd__(self, other)` is called for `self += other`, allowing modification.
#
# 4. BEST PRACTICES:
#    - Ensure overloading makes logical sense. Do not overload `+` to perform subtraction.
#    - Return `NotImplemented` from comparison/math methods when operand types are incompatible,
#      enabling cooperative operator dispatch.
#
# 5. INTERVIEW QUESTIONS:
#    - Q: How does Python evaluate `a == b` for a custom class?
#      A: It calls `a.__eq__(b)`. If `__eq__` is not defined, it defaults to comparing their object
#         identities in memory (`id(a) == id(b)`).
#    - Q: What magic method must be implemented to support bracket slicing like `obj[1:5]`?
#      A: `__getitem__(self, key)`. The `key` parameter receives a standard `slice` object.
#
# 6. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a `SmartList` wrapper class that overloads indexing, addition
#      (merging lists), and rich equality comparison.
#
###############################################################################

class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __repr__(self):
        return f"Point2D({self.x}, {self.y})"
        
    # Overload addition (+)
    def __add__(self, other):
        if not isinstance(other, Point2D):
            return NotImplemented
        return Point2D(self.x + other.x, self.y + other.y)
        
    # Overload equal comparison (==)
    def __eq__(self, other):
        if not isinstance(other, Point2D):
            return False
        return self.x == other.x and self.y == other.y
        
    # Overload less-than comparison (<)
    def __lt__(self, other):
        if not isinstance(other, Point2D):
            return NotImplemented
        # Compare distance from origin
        dist_self = (self.x**2 + self.y**2) ** 0.5
        dist_other = (other.x**2 + other.y**2) ** 0.5
        return dist_self < dist_other

# Test Point2D Operator Overloading
p1 = Point2D(3, 4)  # Distance = 5
p2 = Point2D(5, 12) # Distance = 13
p3 = Point2D(3, 4)

print("--- Testing Math Overloading (+) ---")
print(f"p1 + p2: {p1 + p2}")  # Expected: Point2D(8, 16)

print("\n--- Testing Comparison Overloading (==, <) ---")
print(f"p1 == p3: {p1 == p3}")  # Expected: True (Values match)
print(f"p1 == p2: {p1 == p2}")  # Expected: False
print(f"p1 < p2:  {p1 < p2}")   # Expected: True (5 < 13)

# 2. Indexer/Slice Overloading (__getitem__)
# We will create a class wrapping a list to show custom item indexing
class CustomContainer:
    def __init__(self, items):
        self._items = items
        
    def __getitem__(self, key):
        # Inspect if key is an integer or slice object
        if isinstance(key, slice):
            print(f" -> Slice detected! range: {key.start} to {key.stop}")
            return self._items[key]
        elif isinstance(key, int):
            print(f" -> Index integer lookup: {key}")
            return self._items[key]
        else:
            raise TypeError("Invalid index key type.")

container = CustomContainer(["Alpha", "Beta", "Gamma", "Delta"])

print("\n--- Testing Custom Indexing (Bracket Overloading) ---")
print(f"Index 1: {container[1]}")        # Expected: "Beta"
print(f"Slice [1:3]: {container[1:3]}")  # Expected: ["Beta", "Gamma"]
