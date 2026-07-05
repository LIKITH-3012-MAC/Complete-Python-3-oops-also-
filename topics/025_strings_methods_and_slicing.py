###############################################################################
# TOPIC: String Slicing and String Methods
#
# 1. DEFINITION & INTRODUCTION:
#    - Python strings are immutable sequences. We access characters using indices or
#      sub-sequences using slicing.
#    - Slicing Syntax: `string[start:stop:step]`
#        - `start`: Initial index of the slice (inclusive, defaults to 0).
#        - `stop`: Ending index of the slice (exclusive, defaults to len).
#        - `step`: Interval between steps (defaults to 1).
#      Negative indices refer to positions from the end of the string (e.g. `-1` is the last char).
#
# 2. CASEFOLD() VS LOWER() (Crucial caseless matching detail):
#    - `lower()`: Standard lowercase conversion. Handles characters in basic Latin scripts.
#    - `casefold()`: Aggressive lowercase conversion. Used for caseless matching of characters
#      in European and non-Latin alphabets.
#      Example: The German lowercase letter 'ß' (called Eszett) is converted to "ss" by
#      `casefold()`, whereas `lower()` leaves it unchanged as 'ß'.
#
# 3. SPLIT VS PARTITION:
#    - `split(sep, maxsplit)`: Splits the string by a separator and returns a list.
#    - `partition(sep)`: Searches for a separator and returns a 3-tuple:
#      `(part_before, separator, part_after)`. If the separator is not found, it returns
#      the original string followed by two empty strings. This is extremely efficient because
#      it does not scan the entire string once a match is found and doesn't allocate list objects.
#
# 4. TIME COMPLEXITY:
#    - Slicing: O(K) where K is the length of the slice (creates a new string).
#    - Reversing `[::-1]`: O(N) where N is string length.
#    - Search methods (`find`, `index`, `replace`): O(N * M) worst-case, but highly optimized
#      internally using C-level string search implementations (Boyer-Moore-Horspool algorithm).
#
# 5. BEST PRACTICES:
#    - Use `str.casefold()` whenever you need to compare user-supplied text values case-insensitively.
#    - Use `''.join(list_of_strings)` to build strings. Do NOT loop and accumulate strings
#      using `+` (e.g. `s += char`), because strings are immutable, and `+=` in a loop generates
#      multiple temporary string objects, leading to O(N^2) memory reallocation behavior.
#
# 6. INTERVIEW QUESTIONS:
#    - Q: How can you reverse a string using slicing?
#      A: `reversed_str = original_str[::-1]`.
#    - Q: What is the difference between `find()` and `index()`?
#      A: Both locate substrings. However, `find()` returns `-1` if the substring is not found,
#         while `index()` raises a `ValueError` exception.
#
# 7. EXERCISES & SOLUTIONS:
#    - Coding challenge: Write a function to check if a string is a palindrome case-insensitively,
#      ignoring non-alphanumeric characters, using slicing and string methods.
#
###############################################################################

# 1. String Slicing Mechanics
text = "PythonLanguage"

print("--- String Slicing ---")
print(f"Original text: {text}")
print(f"Slice text[0:6]: {text[0:6]}")          # Expected: "Python"
print(f"Slice text[6:]:   {text[6:]}")           # Expected: "Language"
print(f"Slice with negative indices [-8:-1]: {text[-8:-1]}")  # Expected: "Languag"
print(f"Reverse string via slice [::-1]: {text[::-1]}")  # Expected: "egaugnaLnohtyP"

# Using slice objects explicitly
# slice(start, stop, step) is the underlying Python object created by string[start:stop:step]
custom_slice = slice(0, 6, 2)
print(f"Using slice object [0:6:2]: {text[custom_slice]}")  # Expected: "Pto"

# 2. Case Mapping & casefold() Demonstration
german_word = "Fluß"  # German word for river containing Eszett 'ß'

print("\n--- casefold() vs lower() ---")
print(f"Original German word: {german_word}")
print(f"lower():    {german_word.lower()}")     # Expected: "fluß"
print(f"casefold(): {german_word.casefold()}")  # Expected: "fluss" (converts 'ß' to 'ss')

# 3. String Querying methods (isnumeric, isdigit, isdecimal)
# This is a common interview confusion point.
print("\n--- Digits vs Numeric vs Decimal ---")
num_char = "½"  # Unicode fraction half
print(f"'{num_char}': isdecimal()? {num_char.isdecimal()} | isdigit()? {num_char.isdigit()} | isnumeric()? {num_char.isnumeric()}")
# Expected: isdecimal: False, isdigit: False, isnumeric: True. Fractions are numeric, but not decimal digits.

# 4. Search and Replace
search_target = "banana"
print("\n--- Search and Replace ---")
print(f"find('nan'):  {search_target.find('nan')}")  # Expected: 2 (Index)
print(f"find('xyz'):  {search_target.find('xyz')}")  # Expected: -1 (Not found, no error)
try:
    search_target.index("xyz")
except ValueError as e:
    print(f"index('xyz') throws: {e}")  # Expected: raises ValueError

# 5. Splitting and Partitioning
data_record = "user_name:admin:root"
print("\n--- Split vs Partition ---")
print(f"split(':'): {data_record.split(':')}")  # Returns a list of strings
print(f"partition(':'): {data_record.partition(':')}")  # Returns 3-tuple: ('user_name', ':', 'admin:root')

# 6. Padding and Trimming
padding_demo = "  content  "
print("\n--- Trimming & Padding ---")
print(f"strip():  '{padding_demo.strip()}'")  # Removes leading/trailing spaces
print(f"zfill(5): '{'42'.zfill(5)}'")  # Pads zero left: "00042"
print(f"center(20, '*'): '{'text'.center(20, '*')}'")  # Center pads: "********text********"
