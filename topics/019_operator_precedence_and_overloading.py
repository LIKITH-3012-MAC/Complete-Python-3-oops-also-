###############################################################################
# TOPIC: Operator Precedence, Associativity, and Operator Overloading
#
# 1. DEFINITION & INTRODUCTION:
#    - Operator Precedence: Determines the grouping of terms in an expression and
#      decides how an expression is parsed when multiple operators are present.
#    - Associativity: Determines the order of execution when operators of the same
#      precedence level appear together.
#    - Operator Overloading: Allows custom classes to define their response to Python's
#      built-in operators (like `+`, `-`, `*`) by implementing specific magic (dunder) methods.
#
# 2. OPERATOR PRECEDENCE TABLE (Highest to Lowest):
#    1. `(expressions...)`, `[expressions...]`, `{key: value...}`: Parentheses/brackets/braces
#    2. `subscription[index]`, `slicing[i:j]`, `call(args...)`, `attribute.name`
#    3. `**`: Exponentiation (Right-to-left associativity!)
#    4. `+x`, `-x`, `~x`: Unary positive, negative, bitwise NOT
#    5. `*`, `/`, `//`, `%`: Multiplicative operators
#    6. `+`, `-`: Additive operators
#    7. `<<`, `>>`: Bitwise shift operators
#    8. `&`: Bitwise AND
#    9. `^`: Bitwise XOR
#    10. `|`: Bitwise OR
#    11. In, not in, is, is not, <, <=, >, >=, ==, !=: Comparison, membership, identity
#    12. `not x`: Logical NOT
#    13. `and`: Logical AND
#    14. `or`: Logical OR
#    15. `if - else`: Conditional expression
#    16. `lambda`: Lambda expression
#    17. `:=`: Assignment expression (walrus)
#
# 3. ASSOCIATIVITY RULES:
#    - Left-to-Right Associativity: Most operators evaluate from left to right.
#      Example: `10 - 5 - 2` evaluates as `(10 - 5) - 2` -> `3`.
#    - Right-to-Left Associativity: Exponentiation `**` evaluates right-to-left.
#      Example: `2 ** 3 ** 2` is parsed as `2 ** (3 ** 2)` -> `2 ** 9` -> `512`.
#      Writing `(2 ** 3) ** 2` would evaluate as `8 ** 2` -> `64`.
#
# 4. OPERATOR OVERLOADING METHODS:
#    For any operator `op`, custom classes can define three types of magic methods:
#    - Binary Operators: `__add__(self, other)` for `self + other`.
#    - Reflected (Reverse) Operators: `__radd__(self, other)` for `other + self`. Called
#      when the left operand does not support the operation and returning `NotImplemented`.
#    - In-place Operators: `__iadd__(self, other)` for `self += other`. Enables in-place mutation.
#
# 5. BEST PRACTICES:
#    - Overload operators only when the mathematical analogy makes intuitive sense.
#      Do not overload `+` to mean "delete element".
#    - When implementing binary operators, return `NotImplemented` if the other operand's
#      type is unknown, enabling cooperative dispatch.
#
# 6. INTERVIEW QUESTIONS:
#    - Q: What does `2 ** 3 ** 2` evaluate to in Python?
#      A: `512`. The exponentiation operator is right-associative, so it resolves the
#         rightmost exponent first: `2 ** (3 ** 2) = 2 ** 9 = 512`.
#    - Q: How does Python determine whether to call `__add__` or `__radd__`?
#      A: It calls `__add__` on the left operand first. If that returns `NotImplemented`
#         (or if the left operand doesn't implement `__add__`), it checks the right operand
#         and calls `__radd__` on it.
#
# 7. EXERCISES & SOLUTIONS:
#    - Coding challenge: Create a `Vector2D` class that overloads addition, subtraction,
#      scalar multiplication, and in-place addition, displaying changes to object identity.
#
###############################################################################

# 1. Associativity Proof (Right-Associative Exponentiation)
res_right_assoc = 2 ** 3 ** 2  # 2 ** (3 ** 2) -> 2 ** 9
res_left_assoc = (2 ** 3) ** 2  # (2 ** 3) ** 2 -> 8 ** 2

print("--- Associativity Demonstration ---")
print(f"2 ** 3 ** 2 = {res_right_assoc}")  # Expected: 512
print(f"(2 ** 3) ** 2 = {res_left_assoc}")  # Expected: 64

# Left-associative subtraction
sub_assoc = 10 - 5 - 2  # (10 - 5) - 2
print(f"10 - 5 - 2 = {sub_assoc}")  # Expected: 3

# 2. Vector2D Class with Operator Overloading
class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __repr__(self):
        return f"Vector2D({self.x}, {self.y})"
        
    # Standard addition operator (+)
    def __add__(self, other):
        if not isinstance(other, Vector2D):
            return NotImplemented
        return Vector2D(self.x + other.x, self.y + other.y)
        
    # Reflected addition (called if: non-Vector2D + Vector2D)
    def __radd__(self, other):
        # Addition is commutative, so we can just reuse __add__
        return self.__add__(other)
        
    # In-place addition (+=)
    def __iadd__(self, other):
        if not isinstance(other, Vector2D):
            return NotImplemented
        print(" -> In-place addition (__iadd__) invoked!")
        self.x += other.x
        self.y += other.y
        return self  # MUST return self to update variable binding
        
    # Multiplication (*)
    def __mul__(self, scalar):
        # Multiplies vector by a scalar value (float/int)
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        return Vector2D(self.x * scalar, self.y * scalar)
        
    # Reflected multiplication (scalar * vector)
    def __rmul__(self, scalar):
        return self.__mul__(scalar)

# Test the overloaded operations
v1 = Vector2D(1, 2)
v2 = Vector2D(3, 4)

print("\n--- Operator Overloading Output ---")
print(f"v1: {v1} | v2: {v2}")

# Binary Add
v3 = v1 + v2
print(f"Addition (v1 + v2): {v3}")  # Expected: Vector2D(4, 6)

# Scalar Multiplication
v4 = v1 * 3
print(f"Multiplication (v1 * 3): {v4}")  # Expected: Vector2D(3, 6)

# Reflected Scalar Multiplication (3 * v1)
v5 = 3 * v1
print(f"Reflected Multiplication (3 * v1): {v5}")  # Expected: Vector2D(3, 6)

# In-place Add (+=)
# Check if the memory address changes
original_v1_id = id(v1)
v1 += v2
print(f"v1 after += v2: {v1}")  # Expected: Vector2D(4, 6)
print(f"Is v1 the same object in memory? {id(v1) == original_v1_id}")  # Expected: True (In-place mutated)
