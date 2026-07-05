###############################################################################
# TOPIC: Control Flow - Conditionals (if, elif, else) and Ternary Expression
#
# 1. DEFINITION & INTRODUCTION:
#    - Conditional statements control program execution branches based on truth value
#      evaluations of expressions.
#    - Python keywords: `if`, `elif` (else-if shortcut), `else`.
#
# 2. TERNARY CONDITIONAL EXPRESSION:
#    - Syntax: `value_if_true if condition else value_if_false`
#    - Unlike traditional statements, this is an *expression* that evaluates and returns
#      a value. It is equivalent to C-family `condition ? val1 : val2`.
#    - Ternary operators also perform short-circuiting; only the branch selected by the
#      condition is evaluated.
#
# 3. TRUTH VALUE EVALUATION RULES:
#    - Python conditional blocks implicitly cast expression results to boolean values.
#    - Therefore, any object can serve as a conditional check (relying on its truthiness,
#      resolving to `__bool__` or `__len__` as covered in the Boolean topic).
#
# 4. CONDITIONAL CLAUSE SHORT-CIRCUIT COMBINATIONS:
#    - When combining checks (e.g. `if condition_a and condition_b:`), order of conditions
#      is important. Place fast check operations or highly discriminative clauses on the left
#      to benefit from short-circuiting, bypassing execution of slow checks on the right.
#
# 5. BEST PRACTICES:
#    - Keep conditional nesting levels to a minimum to maintain readability. Use guard clauses
#      and early returns where applicable.
#    - Avoid redundant truth comparisons (e.g. write `if active:` instead of `if active == True:`).
#
# 6. INTERVIEW QUESTIONS:
#    - Q: How does the Python ternary expression differ from C-style?
#      A: In Python, it is written as `x if condition else y` (value first, condition middle),
#         whereas in C-style languages it uses the ternary syntax `condition ? x : y`.
#    - Q: Explain what a "guard clause" is.
#      A: A conditional statement at the beginning of a function that returns early or raises
#         an exception on failure criteria, preventing nested indentation for main logic.
#
# 7. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a nested category classifier using ternary expressions
#      to categorize age categories (child, teen, adult, senior) in a single line.
#
###############################################################################

# 1. Standard Conditional Block
age = 20

print("--- Standard Conditionals ---")
if age < 13:
    print("Category: Child")
elif age < 20:
    # Executes only if the first condition is False
    print("Category: Teen")
else:
    # Executes only if all previous conditions are False
    print("Category: Adult")

# 2. Ternary Conditional Expression
# Syntax: expression_true if condition else expression_false
status = "Active User" if age >= 18 else "Minor Account"
print(f"\nUser status (ternary): {status}")  # Expected: "Active User"

# 3. Short-circuiting in Conditional Clauses
# We will show how placing a safe check on the left prevents a TypeError on the right.
username = None

# If we checked: if len(username) > 0: -> raises TypeError (None has no len)
# But because of short-circuiting, the left-hand 'username is not None' evaluates to False,
# and Python skips the right-hand len check entirely!
print("\n--- Short-circuit conditional execution ---")
if username is not None and len(username) > 0:
    print(f"Logged in: {username}")
else:
    print("Anonymous user detected safely.")

# 4. Nested Ternary Expressions (Classifier Challenge)
# Categorize age into: "Child" (<13), "Teen" (<20), "Adult" (<65), or "Senior".
# While powerful, nested ternaries should be used sparingly as they can be hard to read.
age_test = 70
category = "Child" if age_test < 13 else ("Teen" if age_test < 20 else ("Adult" if age_test < 65 else "Senior"))
print(f"\nCategorized age {age_test} as: {category}")  # Expected: "Senior"
