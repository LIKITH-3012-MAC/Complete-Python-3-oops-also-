###############################################################################
# TOPIC: Core Data Types - Booleans (bool) and Truthiness
#
# 1. DEFINITION & INTRODUCTION:
#    - Python's `bool` type represents logical truth values, having exactly two
#      constant singleton objects: `True` and `False`.
#
# 2. SUBCLASS OF INTEGER:
#    - Historically, Python did not have a dedicated boolean type, using 1 and 0.
#      When `bool` was introduced, it was implemented as a direct subclass of `int`
#      to maintain backward compatibility.
#    - Because `bool` inherits from `int`:
#        - `True` has an integer value of 1.
#        - `False` has an integer value of 0.
#        - You can perform arithmetic operations directly on booleans (e.g., `True + True` is 2).
#
# 3. TRUTH VALUE TESTING (TRUTHINESS):
#    - Every Python object has an implicit truthiness value and can be evaluated in boolean
#      contexts (like `if` statements).
#    - Built-in Falsey values:
#        - Constants: `None`, `False`
#        - Numeric zero: `0`, `0.0`, `0j`, `Decimal(0)`, `Fraction(0, 1)`
#        - Empty sequences/collections: `""`, `[]`, `()`, `{}`, `set()`, `range(0)`
#    - All other objects evaluate to `True` by default.
#
# 4. CUSTOM OBJECT TRUTH VALUE RESOLUTION:
#    - When Python tests the truth value of a custom object instance, it checks:
#        1. Does the object implement the `__bool__()` magic method? If so, Python calls it
#           and expects it to return `True` or `False`.
#        2. If `__bool__()` is not defined, Python checks for `__len__()`. If `__len__()` returns
#           0, the object is considered `False`; otherwise, it is `True`.
#        3. If neither method is implemented, the object is always considered `True`.
#
# 5. SHORT-CIRCUIT EVALUATION:
#    - Logical operators `and` and `or` perform short-circuit evaluation:
#        - `expr1 or expr2`: If `expr1` is truthy, it is returned immediately without
#          evaluating `expr2`. If `expr1` is falsey, `expr2` is evaluated and returned.
#        - `expr1 and expr2`: If `expr1` is falsey, it is returned immediately without
#          evaluating `expr2`. If `expr1` is truthy, `expr2` is evaluated and returned.
#    - Note: `and` and `or` do not always return boolean values; they return the object
#      that terminated the evaluation!
#
# 6. TIME COMPLEXITY:
#    - Boolean evaluations are extremely fast O(1) checks.
#
# 7. BEST PRACTICES:
#    - Do not compare booleans using `==` (e.g., write `if x:` instead of `if x == True:`).
#    - Be careful when relying on truthiness for function arguments (e.g. `if not limit:`
#      can trigger if limit is `0`, which might be a valid integer input instead of None/unset).
#
# 8. INTERVIEW QUESTIONS:
#    - Q: What is the output of `issubclass(bool, int)`?
#      A: `True`. The `bool` class is a subclass of the `int` class.
#    - Q: What is returned by the expression `[] or "hello"`?
#      A: `"hello"`. The left expression `[]` is falsey, so short-circuiting proceeds
#         to evaluate and return the second expression `"hello"`.
#
# 9. EXERCISES & SOLUTIONS:
#    - Coding challenge: Create a custom container class that changes its truthiness based
#      on the presence of internal elements, implementing both `__bool__` and `__len__`.
#
###############################################################################

# 1. Subclass Relationship and Arithmetic
print("--- Boolean Class & Integer Properties ---")
print(f"Is bool a subclass of int? {issubclass(bool, int)}")  # Expected: True
print(f"True == 1: {True == 1} | False == 0: {False == 0}")  # Expected: True | True

# Arithmetic operations on booleans
sum_bool = True + True + False
print(f"True + True + False = {sum_bool}")  # Expected: 2

# 2. Short-circuit Evaluation (Returns the evaluating object)
print("\n--- Short-circuit Evaluations ---")
res1 = "first" or "second"
print(f"'first' or 'second' = {repr(res1)}")  # Expected: 'first' (short-circuits immediately)

res2 = [] or "fallback_string"
print(f"[] or 'fallback_string' = {repr(res2)}")  # Expected: 'fallback_string'

res3 = 0 and "not_evaluated"
print(f"0 and 'not_evaluated' = {repr(res3)}")  # Expected: 0

res4 = [10] and "evaluated_next"
print(f"[10] and 'evaluated_next' = {repr(res4)}")  # Expected: 'evaluated_next'

# 3. Custom Object Truthiness Resolution
class StatefulContainer:
    def __init__(self):
        self.items = []
        
    def add_item(self, item):
        self.items.append(item)
        
    def __bool__(self):
        # Explicit truthiness check: True if we have items, False otherwise
        print(" -> Custom __bool__ called!")
        return len(self.items) > 0

class LengthOnlyContainer:
    def __init__(self, size):
        self.size = size
        
    def __len__(self):
        # Fallback truthiness: checked if __bool__ is absent
        print(" -> Custom __len__ called!")
        return self.size

# Instantiate objects
container_a = StatefulContainer()
container_b = LengthOnlyContainer(0)
container_c = LengthOnlyContainer(5)

print("\n--- Testing Custom Object Truthiness ---")
print("Testing container_a (StatefulContainer):")
if container_a:
    print("container_a is True")
else:
    print("container_a is False")  # Expected path (empty items list)

container_a.add_item("Python")
if container_a:
    print("container_a with item is True")  # Expected path

print("\nTesting container_b (LengthOnlyContainer - size 0):")
print(f"Truth value: {bool(container_b)}")  # Expected: False

print("\nTesting container_c (LengthOnlyContainer - size 5):")
print(f"Truth value: {bool(container_c)}")  # Expected: True
