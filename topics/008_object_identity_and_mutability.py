###############################################################################
# TOPIC: Object Identity, Value Equality, Mutability, and caching Optimization
#
# 1. DEFINITION & INTRODUCTION:
#    - Object Identity: Every object in Python has a unique identifier which represents
#      its memory address. This is accessed via the built-in `id(obj)` function.
#      The identity operator `is` compares the memory addresses of two references.
#    - Value Equality: The `==` operator compares the structural values of two
#      objects, resolving internally to the `__eq__` magic method.
#    - Mutability:
#        - Mutable Objects: Objects whose internal state or contents can be altered in
#          place without changing their memory address (e.g., `list`, `dict`, `set`, `bytearray`).
#        - Immutable Objects: Objects whose value cannot be changed after creation. Any
#          modification operation returns a new object with a new identity (e.g., `int`,
#          `float`, `str`, `tuple`, `frozenset`, `bytes`).
#
# 2. CACHING & INTERNING OPTIMIZATIONS (CPython Internals):
#    To optimize performance and memory, CPython caches and reuses certain immutable objects:
#    - Small Integer Caching: At startup, CPython allocates and caches a static array
#      of integer objects for values between -5 and 256 (inclusive).
#      Any assignment matching this range points to the pre-existing cached objects.
#    - String Interning: Python automatically interns compile-time string constants
#      that look like identifiers (letters, digits, underscores).
#      This is done so that string comparison of identifiers can run in O(1) time
#      using pointer comparison (`is`) instead of character-by-character validation.
#      Interning can be manually triggered using `sys.intern()`.
#
# 3. HASHABILITY RULES:
#    - An object is hashable if it has a hash value that never changes during its
#      lifetime (implemented via `__hash__`) and can be compared to other objects
#      (implemented via `__eq__`).
#    - All immutable built-in types are hashable (except tuples containing mutable elements).
#    - All mutable objects are unhashable, preventing them from being used as keys in
#      dictionaries or elements in sets, since modifying them would break hash table lookup structures.
#
# 4. TIME & SPACE COMPLEXITY:
#    - Identity check (`is` or `id()`): O(1) time complexity.
#    - Value equality (`==`): O(1) for cached/primitives, but up to O(N) where N is the
#      size of structural container structures (like comparing lists or strings).
#
# 5. BEST PRACTICES:
#    - Use `==` for standard comparison of values.
#    - Use `is` or `is not` exclusively when comparing with singletons like `None`,
#      `True`, or `False` (e.g., `if x is None:`).
#    - Be cautious of using mutable default arguments in functions (common bug).
#
# 6. COMMON PITFALLS:
#    - Writing `if x is 10:` instead of `if x == 10:`. If `x` gets calculated at runtime to
#      exceed the small integer cache (e.g. 1000), `is` will return `False` even though the
#      values match.
#    - Supposing that an immutable container (like a tuple) is always hashable.
#      Example: `([1, 2], 3)` is an immutable tuple, but it contains a mutable list, making
#      the tuple unhashable.
#
# 7. INTERVIEW QUESTIONS:
#    - Q: What is the difference between `==` and `is`?
#      A: `==` compares structural value (equality); `is` compares memory address (identity).
#    - Q: Why is a tuple of lists unhashable?
#      A: Hashability requires that the object's value and hash never change. Since the inner
#         list can be modified, the tuple's state can change, so it cannot compute a stable hash.
#
# 8. EXERCISES & SOLUTIONS:
#    - Coding challenge: Prove CPython small integer caching behavior by comparing variables
#      assigned inside and outside the [-5, 256] range.
#
###############################################################################

import sys  # Standard library to perform manual string interning

# 1. Identity vs Value Equality Demonstration
list_a = [1, 2, 3]
list_b = [1, 2, 3]  # Creates a distinct list object with identical contents

print("--- Identity and Equality Check ---")
print(f"list_a == list_b (Value Equality): {list_a == list_b}")  # Expected: True
print(f"list_a is list_b (Memory Identity): {list_a is list_b}")  # Expected: False
print(f"id(list_a) = {id(list_a)} | id(list_b) = {id(list_b)}")

# 2. Mutability in Action
# Modifying a mutable list keeps the identity (id) unchanged.
original_id = id(list_a)
list_a.append(4)
print(f"\nMutable update id matches original? {id(list_a) == original_id}")  # Expected: True

# Immutable string update creates a new object
str_a = "Hello"
str_id = id(str_a)
str_a += " World"
print(f"Immutable update id matches original? {id(str_a) == str_id}")  # Expected: False (New object created)

# 3. Small Integer Caching (-5 to 256)
# Numbers within the cache range share object references.
int_a = 250
int_b = 250
print(f"\nWithin small int cache (250 is 250): {int_a is int_b}")  # Expected: True

# Numbers outside the cache range do not share object references.
int_c = 300
int_d = 300
print(f"Outside small int cache (300 is 300): {int_c is int_d}")  # Expected: False (Usually False, depending on interactive compiler optimizations)

# 4. String Interning Optimization
# Compile-time strings containing only alphanumeric characters/underscores are automatically interned.
s1 = "python_string"
s2 = "python_string"
print(f"\nInterned identifier strings (s1 is s2): {s1 is s2}")  # Expected: True

# Dynamic strings created at runtime are not automatically interned.
s3 = "".join(["python", "_string"])
print(f"Dynamic string (s3 is s1): {s3 is s1}")  # Expected: False

# Force manual interning using sys.intern
s4 = sys.intern(s3)
print(f"Manually interned string (s4 is s1): {s4 is s1}")  # Expected: True

# 5. Hashability Edge Case
# Let's inspect hashability.
tuple_clean = (1, 2, 3)
tuple_dirty = ([1, 2], 3)

print(f"\nIs clean tuple hashable? {isinstance(tuple_clean, collections.abc.Hashable) if 'collections' in sys.modules else True}")
try:
    hash(tuple_clean)
    print("Successfully hashed clean tuple")
except TypeError:
    print("Failed to hash clean tuple")

try:
    # This will raise a TypeError because tuple contains a mutable list element
    hash(tuple_dirty)
except TypeError as e:
    print(f"Failed to hash tuple with list: {e}")
