###############################################################################
# TOPIC: Operators - Arithmetic, Assignment, and the Walrus Operator (:=)
#
# 1. DEFINITION & INTRODUCTION:
#    - Arithmetic Operators: Standard mathematical operations (`+`, `-`, `*`, `/`,
#      `//`, `%`, `**`).
#    - Assignment Operators: Bind names to objects (`=`). Augmented assignment
#      operators (`+=`, `-=`, `*=`, etc.) combine an operation and assignment.
#    - Walrus Operator (`:=`): Officially known as "Assignment Expressions" (PEP 572,
#      introduced in Python 3.8). It allows assigning values to variables as part
#      of an expression, returning the assigned value.
#
# 2. THE WALRUS OPERATOR (:=) - HISTORY & SCOPING:
#    - Introduced in Python 3.8 to reduce code redundancy and improve loop/conditional
#      readability.
#    - Prior to Python 3.8, an assignment was strictly a *statement*, which did not return
#      a value and could not be nested inside conditionals.
#    - Scoping: A variable assigned using `:=` inside a conditional or loop inherits
#      the enclosing function or module scope, remaining accessible after the block ends.
#      However, variables assigned using `:=` inside list comprehensions are scoped
#      locally to the comprehension to prevent polluting the outer scope (except when
#      declared inside a generator expression's filter/conditional block, which can leak).
#
# 3. AUGMENTED ASSIGNMENTS IN-PLACE BEHAVIOR:
#    - When executing `x += y`, CPython checks:
#        1. Does `x` implement the in-place addition magic method `__iadd__`?
#        2. If so, it modifies `x` in-place (mutable types like list do this, keeping the same `id`).
#        3. If not, it falls back to standard `x = x + y`, which creates a new object and
#           rebinds `x` (immutable types like int, str, tuple do this).
#
# 4. BEST PRACTICES:
#    - Use the walrus operator when it improves readability (e.g., retrieving a regex match
#      or reading from a stream inside a loop header). Do not abuse it to write dense,
#      unreadable one-liners.
#    - Use augmented assignments to write clearer code and leverage in-place optimizations
#      for mutable structures.
#
# 5. INTERVIEW QUESTIONS:
#    - Q: What is the difference between `x = x + y` and `x += y` for a list?
#      A: `x = x + y` creates a brand new list object and rebinds the name `x`.
#         `x += y` calls `__iadd__`, extending the original list in-place and keeping the same `id`.
#    - Q: Where can you NOT use the walrus operator?
#      A: You cannot use it as a standalone statement without parentheses if it conflicts with
#         regular assignment grammar (e.g., `x := 10` is invalid; it must be `(x := 10)` or used
#         in an expression context like `if (x := 10) > 5:`).
#
# 6. EXERCISES & SOLUTIONS:
#    - Coding challenge: Write a loop that reads user inputs using the walrus operator,
#      terminating when a sentinel value is received, and print the values.
#
###############################################################################

# 1. Arithmetic Operators Demonstration
val_x = 7
val_y = 3

print("--- Arithmetic Operators ---")
print(f"Addition (7 + 3) = {val_x + val_y}")
print(f"Subtraction (7 - 3) = {val_x - val_y}")
print(f"Multiplication (7 * 3) = {val_x * val_y}")
print(f"True Division (7 / 3) = {val_x / val_y}")
print(f"Floor Division (7 // 3) = {val_x // val_y}")
print(f"Modulo (7 % 3) = {val_x % val_y}")
print(f"Exponentiation (7 ** 3) = {val_x ** val_y}")

# 2. Augmented Assignment & In-Place Mutation
# Mutable type (List)
list_ref = [1, 2]
original_list_id = id(list_ref)
# += calls __iadd__ and mutates the list in-place
list_ref += [3, 4]
print(f"\nList += in-place mutation? {id(list_ref) == original_list_id}")  # Expected: True

# Immutable type (Integer)
int_ref = 10
original_int_id = id(int_ref)
# += falls back to __add__ and creates a new object
int_ref += 5
print(f"Integer += in-place mutation? {id(int_ref) == original_int_id}")  # Expected: False

# 3. Walrus Operator (:=) Demonstration
# Traditional way:
# chunk = stream.read()
# while chunk:
#     process(chunk)
#     chunk = stream.read()

# Using the walrus operator:
# while chunk := stream.read():
#     process(chunk)

print("\n--- Walrus Operator Demonstration ---")
# Simulate reading inputs and filtering them
data_inputs = ["apple", "banana", "cherry", "quit", "extra"]
processed_data = []

# Iterating using the walrus operator inside a while loop condition
idx = -1
# (item := data_inputs[idx]) assigns the value and evaluates to that value.
# The loop exits when we hit 'quit'.
while (item := data_inputs[(idx := idx + 1)]) != "quit":
    print(f"Processing input item: {item}")
    processed_data.append(item)
    
print(f"Processed List: {processed_data}")
# Notice that 'item' and 'idx' are still accessible in the enclosing namespace!
print(f"Post-loop values: item='{item}', idx={idx}")  # Leaked to outer scope

# 4. Scoping of Walrus Operator in Comprehensions
# Inside a list comprehension, the walrus operator restricts the assigned variable
# to the comprehension's local scope to avoid polluting outer namespaces.
outer_val = "original"
squares = [y for x in range(5) if (y := x**2) > 5]
print(f"\nSquares above 5: {squares}")
# Attempting to access 'y' from list comprehension scope:
# In python 3.x, comprehensions have their own scope, so 'y' does not overwrite or leak.
print(f"Outer value check: {outer_val}")
