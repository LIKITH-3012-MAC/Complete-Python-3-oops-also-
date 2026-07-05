###############################################################################
# TOPIC: Comparison and Logical Operators
#
# 1. DEFINITION & INTRODUCTION:
#    - Comparison Operators: Compare values and return booleans.
#      Operators include: `<`, `<=`, `>`, `>=`, `==`, `!=`.
#    - Logical Operators: Combine boolean contexts.
#      Operators include: `and`, `or`, `not`.
#
# 2. CHAINED COMPARISONS (CPython Internals):
#    - Python supports chaining comparison operators (e.g., `a < b <= c`).
#    - In many languages, `a < b < c` is evaluated as `(a < b) < c`. In Python, this evaluates
#      to `(a < b) and (b < c)`.
#    - Single Evaluation Rule: A key feature of Python's chained comparisons is that the
#      middle expression (`b`) is evaluated *exactly once*.
#      For instance, if `b` is a function call like `get_val()`, it is only executed once,
#      preventing side effects and performance loss.
#      Example: `a < get_val() < c` only invokes `get_val()` once.
#
# 3. LOGICAL OPERATORS & SHORT-CIRCUITING:
#    - Logical operators do not perform boolean casting automatically on their returned value.
#      They return the value of the operand that terminated evaluation (as covered in the Bool topic).
#    - Operator Precedence: `not` has highest precedence, followed by `and`, then `or`.
#
# 4. OBJECT COMPARISONS:
#    - Standard comparisons use value equality (`==`). Custom objects implement comparisons
#      via "rich comparison" magic methods: `__lt__`, `__le__`, `__gt__`, `__ge__`, `__eq__`, `__ne__`.
#
# 5. BEST PRACTICES:
#    - Leverage chained comparisons for clean numeric range checks (e.g., `18 <= age < 65`)
#      instead of writing verbose `18 <= age and age < 65` statements.
#
# 6. COMMON PITFALLS:
#    - Relying on order of evaluation when mixing logical operators without parentheses.
#      Write explicit parenthesized conditions to ensure correctness (e.g., `(a or b) and c`
#      instead of `a or b and c`).
#
# 7. INTERVIEW QUESTIONS:
#    - Q: Explain chained comparisons and how they prevent duplicate evaluation.
#      A: `a < b < c` is evaluated as `a < b and b < c`, but Python caches the result of the
#         evaluation of the middle expression `b` internally on the stack, ensuring it is only
#         evaluated once.
#    - Q: What does `not "" or [1]` evaluate to?
#      A: `[1]`. `not ""` is evaluated first (since `not` has higher precedence than `or`),
#         which becomes `True`. Then `True or [1]` short-circuits and returns `True`.
#
# 8. EXERCISES & SOLUTIONS:
#    - Coding challenge: Create a class with a method that prints a message when evaluated,
#      and prove that in a chained comparison the method is only called once.
#
###############################################################################

# 1. Standard Comparison Operators
print("--- Standard Comparisons ---")
print(f"5 < 10: {5 < 10}")  # True
print(f"5 != 10: {5 != 10}")  # True
print(f"5 == '5': {5 == '5'}")  # False (Strict type values, no implicit coercion)

# 2. Chained Comparisons Demonstration
# Check if a value falls within a range
x = 15
is_in_range = 10 < x < 20
print(f"\nIs 15 in range (10, 20)? {is_in_range}")  # Expected: True

# 3. Single Evaluation Proof
# We will define a function that logs its invocation to verify how many times it gets called
# in a chained comparison.
evaluation_count = 0

def get_middle_value():
    global evaluation_count
    evaluation_count += 1
    print(" -> get_middle_value() invoked!")
    return 15

# Chained check: 10 < get_middle_value() < 20
# If python evaluated this as two distinct operations:
# (10 < get_middle_value()) and (get_middle_value() < 20), the function would be called twice.
print("\nEvaluating chained comparison: 10 < get_middle_value() < 20")
result = 10 < get_middle_value() < 20
print(f"Chained comparison result: {result}")
print(f"Total function calls: {evaluation_count}")  # Expected: 1 (Proven single evaluation)

# 4. Logical Operators Precedence and Evaluation
print("\n--- Logical Operator Precedence ---")
# Precedence: 'not' > 'and' > 'or'
# Expression: True or False and False
# Evaluates as: True or (False and False) -> True or False -> True
res_precedence = True or False and False
print(f"True or False and False = {res_precedence}")  # Expected: True

# Compare with: (True or False) and False -> True and False -> False
res_grouped = (True or False) and False
print(f"(True or False) and False = {res_grouped}")  # Expected: False

# 5. String Comparisons (Lexicographical ordering)
# Strings are compared character by character using Unicode values (code points).
print(f"\n'apple' < 'banana': {'apple' < 'banana'}")  # Expected: True ('a' has lower code point than 'b')
print(f"'Apple' < 'apple': {'Apple' < 'apple'}")  # Expected: True (Uppercase letters come before lowercase in Unicode)
