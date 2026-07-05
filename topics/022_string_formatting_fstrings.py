###############################################################################
# TOPIC: Formatted String Literals (f-strings)
#
# 1. DEFINITION & INTRODUCTION:
#    - Formatted string literals (f-strings) are string literals prefixed with 'f' or 'F'.
#      They contain replacement fields marked by curly braces `{}` containing expressions.
#      Introduced in Python 3.6 (PEP 498).
#
# 2. COMPILER MECHANICS & PERFORMANCE:
#    - f-strings are NOT evaluated as dynamic template strings at runtime.
#    - Instead, during compilation, the CPython parser splits the f-string into its
#      literal components and expressions, compiling them directly into optimized bytecode
#      concatenation operations (comparable to calling `''.join([str(x), ...])` or utilizing
#      `FORMAT_VALUE` opcodes).
#    - This makes f-strings significantly faster than `%` formatting or calling `str.format()`,
#      as it avoids the overhead of function call lookups at runtime.
#
# 3. EXPRESSION EVALUATION:
#    - Inside curly braces `{}` in an f-string, you can write any valid Python expression,
#      including arithmetic, dictionary lookups, function calls, and object method invocations.
#
# 4. CONVERSIONS:
#    You can coerce how a value is converted inside the brace using:
#    - `!s`: Invokes `str()` on the value.
#    - `!r`: Invokes `repr()` on the value.
#    - `!a`: Invokes `ascii()` on the value.
#
# 5. DEBUGGING FORMAT (`=` Operator):
#    - Introduced in Python 3.8, adding `=` after an expression (e.g., `f"{variable=}"`)
#      tells Python to print both the variable name (expression text) and its evaluated value,
#      highly useful for print-debugging.
#
# 6. TIME & SPACE COMPLEXITY:
#    - Evaluation of expression: Same as executing the expression natively.
#    - Concatenation: O(N) where N is the total length of the resulting string.
#
# 7. BEST PRACTICES:
#    - Use f-strings for all inline string interpolations due to superior readability
#      and execution performance.
#    - Avoid writing extremely complex logical expressions inside f-string braces.
#      Evaluate complex logic first in separate statements, then interpolate the variable.
#
# 8. INTERVIEW QUESTIONS:
#    - Q: Why are f-strings faster than `str.format()`?
#      A: `str.format()` is a method call lookup on string objects requiring runtime method
#         dispatch. F-strings are parsed at compile-time and compiled directly into low-level
#         `FORMAT_VALUE` and `BUILD_STRING` bytecodes.
#    - Q: What does `f"{val!r}"` do?
#      A: It forces the interpolation to use the representation string `repr(val)` instead of
#         the standard string `str(val)`.
#
# 9. EXERCISES & SOLUTIONS:
#    - Coding challenge: Benchmark the performance of `%` vs `.format()` vs `f-strings`
#      using the standard `timeit` module to verify the speed difference.
#
###############################################################################

import timeit  # standard library module to benchmark code execution speeds

# 1. Basic interpolation & Expressions
user_name = "Charlie"
items_in_cart = 5
price_per_item = 19.99

print("--- f-string Expression Evaluation ---")
# Evaluate math and call string methods inside the f-string
summary = f"User {user_name.upper()} has {items_in_cart} items. Total: ${items_in_cart * price_per_item:.2f}"
print(summary)

# 2. Conversion Specifiers (!s, !r, !a)
special_string = "pythón"  # Contains unicode character 'ó'
print("\n--- Conversions (!s, !r, !a) ---")
print(f"Default str: {special_string}")
print(f"Force str:   {special_string!s}")
print(f"Force repr:  {special_string!r}")   # Includes enclosing quotes
print(f"Force ascii: {special_string!a}")   # Escapes non-ASCII characters to '\xf3'

# 3. Debugging Support (= Operator)
# Useful feature introduced in Python 3.8
debug_x = 42
debug_y = 100
print("\n--- Debugging Support ---")
print(f"{debug_x=}")  # Expected output: debug_x=42
print(f"Calculated expression: {debug_x + debug_y = }")  # Expected: debug_x + debug_y = 142

# 4. Performance Benchmarks
# We will compare the speed of Old-style %, str.format(), and f-strings using timeit.
setup_code = "name = 'Charlie'; age = 30"
percent_test = "'Hello %s, you are %d' % (name, age)"
format_test = "'Hello {}, you are {}'.format(name, age)"
fstring_test = "f'Hello {name}, you are {age}'"

iterations = 1000000
time_percent = timeit.timeit(percent_test, setup=setup_code, number=iterations)
time_format = timeit.timeit(format_test, setup=setup_code, number=iterations)
time_fstring = timeit.timeit(fstring_test, setup=setup_code, number=iterations)

print("\n--- Performance Benchmark (1 Million Runs) ---")
print(f"Old % Operator:    {time_percent:.4f} seconds")
print(f"str.format() API:  {time_format:.4f} seconds")
print(f"fstring Literal:   {time_fstring:.4f} seconds")
print(f"f-string is {time_format / time_fstring:.1f}x faster than str.format()!")
