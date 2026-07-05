###############################################################################
# TOPIC: String Formatting - Old-Style (%) and New-Style (str.format)
#
# 1. DEFINITION & INTRODUCTION:
#    - Python has evolved several mechanisms for string interpolation (inserting values
#      into strings). The two classic styles are:
#        1. Old-Style Formatting (printf-style `%` operator): Inherited from C's `printf`.
#        2. New-Style Formatting (`str.format()` method): Introduced in Python 2.6,
#           offering a more robust, extensible formatting engine.
#
# 2. OLD-STYLE (%) FORMATTING:
#    - Uses the `%` operator with format specifiers (e.g., `%s` for string, `%d` for integer,
#      `%f` for float).
#    - Drawbacks: Verbose, error-prone when passing tuples vs single values, does not
#      support dictionary lookups cleanly without explicit mappings.
#
# 3. NEW-STYLE (str.format) FORMATTING:
#    - Uses curly braces `{}` as placeholders.
#    - Supports:
#        - Positional Arguments: `"{0} is {1}".format("Python", "cool")`
#        - Keyword Arguments: `"{name} is {adjective}".format(name="Python", adjective="cool")`
#        - Dictionary/Attribute Access: Placeholders can access keys or properties directly
#          (e.g., `"{user.name}"`).
#
# 4. FORMAT SPECIFICATION MINI-LANGUAGE:
#    Both methods support formatting modifiers, but `str.format()` uses an advanced syntax
#    `{[index_or_key]:[fill][align][sign][#][0][width][group_sep][.precision][type]}`:
#    - Align: `<` (left), `>` (right), `^` (centered).
#    - Width: Total characters in the formatted field.
#    - Precision: Maximum characters for strings or decimal spots for floats (e.g., `.2f`).
#    - Group separator: `,` or `_` for thousands separators (e.g., `1,000,000`).
#
# 5. BEST PRACTICES:
#    - While f-strings (introduced in Python 3.6) are generally preferred for inline
#      formatting, `str.format()` remains highly useful for defining templates stored in
#      configuration files or database records where variables are evaluated later.
#    - Avoid old-style `%` formatting in new code bases.
#
# 6. INTERVIEW QUESTIONS:
#    - Q: What does `"{:^10}".format("hi")` do?
#      A: Centers the string "hi" inside a field of width 10 characters, padding it with spaces:
#         `"    hi    "`.
#    - Q: How can you write a percentage sign in `%` vs `.format` formatting?
#      A: In `%` formatting, double it: `%%`. In `.format()`, write it as normal inside the string
#         or use the `%` type code: `"{:.1%}".format(0.5)` -> `"50.0%"`.
#
# 7. EXERCISES & SOLUTIONS:
#    - Coding challenge: Format a tabular report containing student names (left-aligned),
#      scores (right-aligned float with 2 decimals), and IDs (centered) using `str.format()`.
#
###############################################################################

# 1. Old-Style (%) Formatting
name = "Alice"
age = 30
salary = 12500.755

print("--- Old-Style (%) Formatting ---")
# Basic interpolation
print("Hello %s, you are %d years old." % (name, age))

# Floating-point precision (Truncates to 2 decimal places)
print("Salary: %.2f" % salary)  # Expected: 12500.76

# Dictionary mapping format
mapping_data = {"user": "Bob", "code": 404}
print("Error % (code)d: % (user)s not found" % mapping_data)

# 2. New-Style (str.format) Formatting
print("\n--- New-Style (str.format) Formatting ---")
# Positional arguments
print("{0} belongs to {1}".format("Data", "us"))

# Named keyword arguments
print("Coordinates: Lat={lat}, Lon={lon}".format(lat="37.77N", lon="122.41W"))

# Accessing attributes and list indices inside placeholders
complex_list = ["Alpha", "Beta", "Gamma"]
print("First element: {0[0]} | Second element: {0[1]}".format(complex_list))

# 3. Format Specification Mini-Language
print("\n--- Format Specification Mini-Language ---")
# Center alignment with fill character
# '{:^10}' Centers the string, '*' is fill character, total width is 10.
print(f"Centered: |{'{:*^10}'.format('Centered')}|") 

# Left and Right Alignment
print("Left Aligned:  |{: <10}|".format("left"))
print("Right Aligned: |{: >10}|".format("right"))

# Numeric Formatting with Comma Separators and Precision
# ',' adds thousands separator, '.2f' rounds float to 2 decimals
print("Formatted Money: ${:,.2f}".format(1000000.899))  # Expected: $1,000,000.90

# Binary and Hexadecimal formatting using format types
# 'b' prints binary, 'x' prints hex
print("Number 255: Binary={:b}, Hex={:x}".format(255, 255))
