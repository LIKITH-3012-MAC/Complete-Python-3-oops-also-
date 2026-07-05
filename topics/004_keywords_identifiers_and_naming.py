###############################################################################
# TOPIC: Keywords, Identifiers, and PEP 8 Naming Conventions
#
# 1. DEFINITION & INTRODUCTION:
#    - Keywords are reserved words in Python that have predefined syntax meanings and
#      cannot be used as identifiers (variable names, function names, etc.).
#    - Identifiers are user-defined names representing variables, functions, classes,
#      modules, or other objects.
#
# 2. KEYWORD CLASSIFICATION:
#    Python keywords are divided into two main categories:
#    - Hard Keywords: Reserved words that always represent syntax structures (e.g.,
#      `def`, `class`, `if`, `while`, `import`). You cannot reassign these words.
#      Attempting to do so results in a `SyntaxError`.
#      Examples: `def = 5` is invalid.
#    - Soft Keywords: Contextual keywords introduced to keep backward compatibility.
#      They act as keywords in specific syntax contexts (e.g., pattern matching) but
#      can be used as normal variable names elsewhere.
#      Examples: `match`, `case`, and `_` (introduced in Python 3.10 for match-case).
#
# 3. IDENTIFIER RULES:
#    - Must start with a letter (A-Z, a-z) or an underscore `_`.
#    - Followed by zero or more letters, underscores, or digits (0-9).
#    - Cannot contain whitespace or special characters (like `@`, `$`, `%`).
#    - Case-sensitive: `myVar` and `myvar` are distinct identifiers.
#    - Can use Unicode letters (e.g., accented characters, non-Latin script).
#
# 4. HISTORY & MOTIVATION:
#    - Python added keywords as the language evolved (e.g., `async` and `await` became
#      hard keywords in Python 3.7 to support native coroutines).
#    - Naming conventions were standardized in PEP 8 (Python Enhancement Proposal 8)
#      to maintain code style consistency across the global open-source ecosystem.
#
# 5. PEP 8 NAMING CONVENTIONS:
#    - Variables & Functions: Snake_case (lowercase with underscores, e.g., `user_age`).
#    - Classes: PascalCase (capitalized words, e.g., `UserProfileManager`).
#    - Constants: UPPERCASE_SNAKE (all capital letters, e.g., `MAX_RETRIES`).
#    - Private Variables: Single leading underscore (`_variable`) indicates internal
#      implementation details.
#    - Strongly Private Variables: Double leading underscore (`__variable`) triggers
#      name mangling within class structures.
#    - Dunder names: Double leading and trailing underscores (`__init__`) are reserved
#      for system-defined magic methods.
#
# 6. INTERNAL IMPLEMENTATION & CPYTHON INTERNALS:
#    - During tokenization, the CPython lexer reads each token and checks it against a
#      perfect hash table of reserved words (generated using `gperf` or similar logic in
#      CPython source). If it matches, the lexer generates a keyword token (e.g., `NAME`
#      vs `DEF`), allowing the parser to construct the grammar tree correctly.
#
# 7. TIME & SPACE COMPLEXITY:
#    - Identifier validation (`str.isidentifier()`) runs in O(N) where N is the length
#      of the identifier.
#    - Lookup of variable names in namespaces (dictionaries) is O(1) average-case.
#
# 8. BEST PRACTICES:
#    - Never redefine built-in functions or types (e.g., do not name variables `list`,
#      `dict`, `str`, `int`, or `print`). Doing so overrides the name in the current scope.
#    - Use descriptive, meaningful names over single-character names (except for simple
#      loop counters like `i`, `j`).
#
# 9. COMMON PITFALLS:
#    - Overwriting built-ins:
#      ```python
#      list = [1, 2, 3] # Overwrites the built-in constructor
#      my_list = list("abc") # Throws TypeError: 'list' object is not callable
#      ```
#    - Confusing name mangling: Attempting to access `__private` attributes outside a
#      class directly instead of through mangled name `_ClassName__private`.
#
# 10. INTERVIEW QUESTIONS:
#     - Q: What are "soft keywords" in Python?
#       A: Keywords that behave as reserved words in certain contexts (like `match`
#          and `case` in match-case statements) but can be used as variable names
#          elsewhere without raising a SyntaxError.
#     - Q: What is name mangling?
#       A: Python automatically alters identifiers starting with double underscores
#          (e.g., `__my_var`) to `_ClassName__my_var` to prevent variable collision
#          in subclasses.
#
# 11. EXERCISES & SOLUTIONS:
#     - Write a script that checks if a list of string identifiers are valid Python
#       names and checks if they are keywords.
#
###############################################################################

import keyword  # Standard library module to inspect Python keyword status
import builtins  # Module containing all built-in types and functions

# 1. Inspect Python Keywords list
print("--- Python Keywords Statistics ---")
all_kw = keyword.kwlist
print(f"Total hard keywords: {len(all_kw)}")
print(f"Examples of hard keywords: {all_kw[:10]}")

# 2. Check for Soft Keywords
# keyword.softkwlist contains the contextual keywords
all_soft_kw = keyword.softkwlist
print(f"Total soft keywords: {len(all_soft_kw)}")
print(f"Soft keywords list: {all_soft_kw}")

# 3. Test Identifier Validity programmatically
# keyword.iskeyword() checks if a string is a reserved keyword
# string.isidentifier() checks if a string matches identifier syntax rules
test_names = ["user_name", "class", "2nd_user", "_private_data", "match", "résumé"]

print("\n--- Identifier Validation Test ---")
for name in test_names:
    is_valid = name.isidentifier()
    is_reserved = keyword.iskeyword(name)
    is_soft = name in keyword.softkwlist
    
    print(f"'{name}':")
    print(f"  Valid identifier syntax? {is_valid}")
    print(f"  Reserved hard keyword? {is_reserved}")
    print(f"  Contextual soft keyword? {is_soft}")

# 4. Demonstrate soft keyword usage as variable
# 'match' and 'case' are soft keywords, so they can be normal variable names.
match = "This is a string assigned to match variable"  # Valid variable binding
case = 42  # Valid variable binding
print(f"\nSoft keyword variables: match='{match}', case={case}")

# 5. Demonstrate the danger of overwriting built-ins
# We will temporarily print a message showing how a built-in can be shadowed.
# Shadowing 'sum' built-in function
original_sum = builtins.sum
sum = 100  # Shadowing 'sum' with an integer in local namespace

print(f"\nLocal shadow 'sum' variable value: {sum}")
try:
    # Attempting to use the shadowed 'sum' as a function
    sum([1, 2, 3])
except TypeError as e:
    print(f"Caught expected TypeError from shadowed sum: {e}")

# Restoring the built-in function to clean up the environment
sum = original_sum
print(f"Restored sum of [1, 2, 3]: {sum([1, 2, 3])}")
