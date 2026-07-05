###############################################################################
# TOPIC: repr() vs str(), ascii(), and Pretty Printing (pprint)
#
# 1. DEFINITION & INTRODUCTION:
#    - `str(obj)`: Creates a user-friendly, readable string representation of an object.
#      Aimed at end-users. Resolves to `__str__()`.
#    - `repr(obj)`: Creates an unambiguous, developer-friendly string representation of
#      an object. Aimed at developers for debugging. Ideally, `eval(repr(obj))` should reconstruct
#      the object. Resolves to `__repr__()`.
#    - `ascii(obj)`: Like `repr()`, but escapes any non-ASCII characters with `\x`, `\u`,
#      or `\U` escape sequences.
#    - `pprint`: A standard library module used to format complex nested data structures (lists,
#      dicts, sets) into highly readable, aligned multi-line layouts.
#
# 2. INTERNAL RESOLUTION RULES:
#    - When you call `print(obj)`, Python tries to resolve `obj.__str__()`. If missing, it
#      falls back to `obj.__repr__()`.
#    - If `obj.__repr__()` is also missing, Python uses the base class object representation
#      (`<__main__.ClassName object at 0x... >`).
#
# 3. THE `pprint` MODULE:
#    - Real-world nested datasets (like parsed JSON responses) are difficult to read when printed
#      as a single raw string.
#    - `pprint.pprint(data, stream=None, indent=1, width=80, depth=None, compact=False, sort_dicts=True)`:
#        - `indent`: Number of spaces for each indentation level.
#        - `width`: Maximum character width before wrapping.
#        - `depth`: Maximum nested levels to display; deeper levels are replaced with `...`.
#        - `sort_dicts`: If `True` (default), keys in dictionaries are printed sorted alphabetically.
#
# 4. TIME COMPLEXITY:
#    - `repr()` and `str()` evaluations depend on object structure size, running in O(N).
#    - `pprint` runs in O(N log N) due to recursive formatting and dict sorting.
#
# 5. BEST PRACTICES:
#    - Always define `__repr__` for custom classes. It pays off immensely during debugging and
#      logging.
#    - Use `pprint` when logging or displaying complex nested dictionaries in CLI tools.
#
# 6. INTERVIEW QUESTIONS:
#    - Q: What is the main design difference between `__str__` and `__repr__`?
#      A: `__str__` is for readability (informational representation for users); `__repr__` is
#         for unambiguity (accurate state representation for developers, often matching code syntax).
#    - Q: If `__str__` is not defined in a class, what happens when you call `str(instance)`?
#      A: Python falls back to calling `__repr__` of the class.
#
# 7. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a custom class with both `__str__` and `__repr__` methods,
#      demonstrating how they are invoked under different contexts (`str(x)`, `repr(x)`, list prints).
#
###############################################################################

import pprint  # Standard library module to pretty print complex data types
import datetime  # Import datetime to show built-in str vs repr differences

# 1. str() vs repr() Built-in Comparison
# datetime is a perfect example of str vs repr divergence.
today = datetime.datetime(2026, 7, 5, 12, 0, 0)

print("--- str() vs repr() Datetime Example ---")
print(f"str(today)  = {str(today)}")   # Readable: '2026-07-05 12:00:00'
print(f"repr(today) = {repr(today)}")  # Unambiguous code: 'datetime.datetime(2026, 7, 5, 12, 0)'

# 2. Custom Class implementing str and repr
class Programmer:
    def __init__(self, name, language):
        self.name = name
        self.language = language
        
    def __str__(self):
        # User-facing readable format
        return f"{self.name} writes {self.language}"
        
    def __repr__(self):
        # Developer-facing constructor format
        return f"Programmer(name={repr(self.name)}, language={repr(self.language)})"

p = Programmer("Likith", "Python")
print("\n--- Custom Class Representation ---")
print(f"print(p): {p}")  # Calls __str__
print(f"repr(p):  {repr(p)}")  # Calls __repr__

# If the object is inside a container (like a list), Python calls its __repr__!
programmers_list = [p, Programmer("Guido", "ABC")]
print(f"Container list format: {programmers_list}")

# 3. ascii() function demonstration
unicode_str = "résumé"
print(f"\nOriginal: {unicode_str} | ascii() Escaped: {ascii(unicode_str)}")

# 4. Pretty Printing (pprint) Demonstration
# Create a complex, deeply nested dictionary structure
nested_dataset = {
    "status": "success",
    "metadata": {
        "timestamp": "2026-07-05T12:00:00Z",
        "nested_arrays": [[1, 2, 3], [4, 5, 6]],
        "authorized_roles": {"admin", "developer", "tester"}
    },
    "users": [
        {"id": 1, "details": {"name": "Alice", "tags": ["lead", "frontend"]}},
        {"id": 2, "details": {"name": "Bob", "tags": ["backend", "database"]}}
    ]
}

print("\n--- Standard print() output ---")
print(nested_dataset)  # Hard to read, single compressed line

print("\n--- Pretty printed (pprint) output ---")
# pprint formats dictionaries sorted by keys and formats levels on separate lines
pprint.pprint(nested_dataset, width=50, indent=2)

print("\n--- Pretty printed with depth constraint (depth=2) ---")
# depth argument collapses elements below nested level 2 to '...'
pprint.pprint(nested_dataset, depth=2, indent=2)
