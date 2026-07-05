###############################################################################
# TOPIC: String Interning and Escape Characters & Raw Strings
#
# 1. DEFINITION & INTRODUCTION:
#    - String Interning: An optimization technique where Python stores only one copy of
#      each distinct string value in a lookup table, reuse-sharing the reference.
#    - Escape Characters: System to output special symbols or control signals (like newline,
#      tab, backslash) inside string literals using backslash (`\`) prefixing.
#      Examples: `\n` (newline), `\t` (tab), `\xHH` (hex code), `\uXXXX` (unicode point).
#    - Raw Strings: Strings prefixed with `r` or `R`. They treat backslashes as literal
#      characters rather than escapes.
#
# 2. STRING INTERNING IN CPYTHON (Deep Dive):
#    - CPython maintains an internal dictionary containing all interned strings (`interned`).
#    - At compile-time, CPython automatically interns:
#        - String constants containing only letters, numbers, or underscores (valid identifier names).
#        - Strings created via constant folding (e.g., `'a' * 5`).
#    - CPython does NOT automatically intern:
#        - Strings containing punctuation (spaces, hyphens, exclamation marks).
#        - Strings constructed dynamically at runtime (e.g. from file reads or user inputs).
#    - Verification: You can check if strings are interned using the identity operator `is`.
#    - Manual Interning: Call `sys.intern(string_obj)`.
#
# 3. RAW STRINGS BACKSLASH EDGE CASE:
#    - Raw strings are defined using the `r` or `R` prefix (e.g., `r"C:\Users\Name"`).
#    - Important rule: Even in a raw string, a backslash can escape a quote character.
#      Therefore, a raw string CANNOT end with an odd number of backslashes!
#      Example: `r"directory\"` is invalid because the trailing backslash escapes the closing quote,
#      resulting in a `SyntaxError: unterminated string literal`.
#      To write a raw string ending in a backslash, you must escape it or concatenate:
#      `r"directory" + "\\"` or `r"directory\\"` (which will have two backslashes).
#
# 4. TIME & SPACE COMPLEXITY:
#    - String Interning lookup: O(1) average lookup in the internal C-level dictionary.
#    - Interning saves space by eliminating duplicate string payloads, and speeds up
#      subsequent comparisons from O(N) string sweeps to O(1) pointer checks.
#
# 5. BEST PRACTICES:
#    - Use raw strings for regular expressions (`r"\d+"`) and Windows file paths to avoid
#      accidental escape sequence conversions.
#
# 6. INTERVIEW QUESTIONS:
#    - Q: Why is `a = "hello world"` and `b = "hello world"` evaluated as `a is b -> False`?
#      A: Because the string contains a space character (non-identifier), so CPython's compiler
#         bypasses automatic interning, creating two separate objects in memory.
#    - Q: Can you write `path = r"C:\Folder\"`?
#      A: No, this raises a `SyntaxError`. The trailing backslash in the raw string escapes the
#         closing double quote. You must write `r"C:\Folder" + "\\"` or `r"C:\Folder\\"`.
#
# 7. EXERCISES & SOLUTIONS:
#    - Coding challenge: Write a script demonstrating automatic interning rules, manual interning,
#      and workarounds for raw strings ending in backslashes.
#
###############################################################################

import sys  # Standard library to use sys.intern()

# 1. Automatic vs Manual Interning Demonstration
a1 = "hello_world"
a2 = "hello_world"
print("--- Automatic Interning (Identifiers) ---")
print(f"a1 is a2: {a1 is a2}")  # Expected: True (Contains only letters/underscores, auto-interned)

b1 = "hello world!"
b2 = "hello world!"
print("\n--- Non-interned String (Contains space and exclamation) ---")
print(f"b1 is b2: {b1 is b2}")  # Expected: False (Not automatically interned)

# Manually interning b1 and b2
b1_interned = sys.intern(b1)
b2_interned = sys.intern(b2)
print(f"Manual intern (b1 is b2): {b1_interned is b2_interned}")  # Expected: True

# 2. Escape Characters
print("\n--- Escape Sequences ---")
# Standard Escapes
print("Newline:\nLine2\tTabbed\rCarriageReturn (Overwritten text)")
# Unicode Escapes (\uXXXX)
print("Unicode Omega: \u03a9")  # Expected: Ω
# Hex Escapes (\xHH)
print("Hex Escapes: \x41\x42\x43")  # Expected: ABC

# 3. Raw Strings (Literal backslashes)
print("\n--- Raw Strings vs Normal Strings ---")
normal_path = "C:\\Users\\Name\\Documents"
raw_path = r"C:\Users\Name\Documents"

print(f"Normal String: {normal_path}")
print(f"Raw String:    {raw_path}")
print(f"Are they equal in value? {normal_path == raw_path}")  # Expected: True

# 4. Raw String Backslash Edge Case
# Attempting raw string ending in single backslash:
# r"C:\" -> SyntaxError because the backslash escapes the quote!
# Workaround:
safe_raw_end = r"C:\Folder" + "\\"
print(f"\nSafe path ending with backslash: {safe_raw_end}")
# Another workaround (adds two backslashes if two are intended):
double_raw_end = r"C:\Folder\\"
print(f"Double backslash path: {double_raw_end}")
