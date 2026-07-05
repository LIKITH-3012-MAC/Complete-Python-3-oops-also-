###############################################################################
# TOPIC: Sets and Frozensets (set, frozenset)
#
# 1. DEFINITION & INTRODUCTION:
#    - Set: A mutable, unordered collection of unique, hashable objects.
#    - Frozenset: An immutable variant of a set. Since it is immutable, it is hashable,
#      meaning a frozenset can be used as a dictionary key or placed inside another set
#      (a standard set cannot be placed inside another set).
#
# 2. CPYTHON INTERNAL STRUCTURE (Hash Tables):
#    - Sets are implemented as open-addressed hash tables.
#    - Structurally, they are very similar to dictionaries, but instead of storing key-value
#      pairs, set table entries (`dummy` or `active` slots) store only keys.
#    - To maintain unique elements, when you add an item `x`, Python hashes it, computes the
#      target slot index, and checks for collisions using equality comparison (`==`). If the value
#      already exists, the addition is skipped.
#
# 3. HASHABILITY REQUIREMENT:
#    - Any element placed in a `set` must be hashable. Mutable types (like lists, dictionaries,
#      or standard sets) cannot be added.
#    - Attempting to add an unhashable type raises a `TypeError: unhashable type`.
#
# 4. MATHEMATICAL OPERATIONS & OPERATORS:
#    Sets support standard mathematical set operations:
#    - Union (`|` or `set.union()`): Combines elements of both sets.
#    - Intersection (`&` or `set.intersection()`): Elements present in both sets.
#    - Difference (`-` or `set.difference()`): Elements in set A but not in set B.
#    - Symmetric Difference (`^` or `set.symmetric_difference()`): Elements in set A or B, but not both.
#    - Subset (`<=` or `set.issubset()`): Checks if all elements of A are in B.
#    - Superset (`>=` or `set.issuperset()`): Checks if A contains all elements of B.
#
# 5. TIME & SPACE COMPLEXITY:
#    - Add / Remove / Containment check (`in`): O(1) average-case. O(N) worst-case (if hash table
#      experiences severe collision degradation).
#    - Mathematical operators:
#        - Union A | B: O(len(A) + len(B)).
#        - Intersection A & B: O(min(len(A), len(B))) if search sizes are optimized.
#
# 6. INTERVIEW QUESTIONS:
#    - Q: Can you add a set to another set?
#      A: Not directly. Standard sets are mutable (unhashable). However, you can convert the set
#         to a `frozenset`, which is hashable, and add it to the outer set.
#    - Q: What happens if you try to add a float to a set containing an integer of the same value
#      (e.g. `s = {1}; s.add(1.0)`)?
#      A: The set remains `{1}`. In Python, `1 == 1.0` is `True` and their hash values match:
#         `hash(1) == hash(1.0)`. Thus, Python treats them as duplicate entries.
#
# 7. EXERCISES & SOLUTIONS:
#    - Coding challenge: Given two lists, find all unique elements that are present in either
#      list but not both, without using loops, leveraging set operators.
#
###############################################################################

# 1. Basic Set Instantiation & Uniqueness
# Sets discard duplicate values automatically.
s1 = {1, 2, 2, 3, 3, 3}
print("--- Set Properties ---")
print(f"Set s1: {s1} | Length: {len(s1)}")  # Expected: {1, 2, 3} | Length: 3

# Float vs Integer identity duplication check
# Python treats 1 and 1.0 as duplicates in a set.
s_dup = {1}
s_dup.add(1.0)
print(f"Set after adding 1.0: {s_dup}")  # Expected: {1}

# 2. Hashability Constraints
try:
    s_invalid = {1, [2, 3]}  # List is unhashable
except TypeError as e:
    print(f"\nCaught expected TypeError (list in set): {e}")

# 3. Mathematical Set Operators
set_a = {1, 2, 3, 4}
set_b = {3, 4, 5, 6}

print("\n--- Mathematical Operations ---")
print(f"Set A: {set_a} | Set B: {set_b}")
print(f"Union (A | B):        {set_a | set_b}")                  # Expected: {1, 2, 3, 4, 5, 6}
print(f"Intersection (A & B): {set_a & set_b}")                  # Expected: {3, 4}
print(f"Difference (A - B):   {set_a - set_b}")                  # Expected: {1, 2}
print(f"Symmetric Diff (A^B): {set_a ^ set_b}")                  # Expected: {1, 2, 5, 6}

# 4. Subset and Superset checking
set_sub = {3, 4}
print(f"\nIs {set_sub} subset of A? {set_sub <= set_a}")        # Expected: True
print(f"Is A superset of {set_sub}? {set_a >= set_sub}")        # Expected: True

# 5. Frozenset Demonstration
# frozenset is immutable and can compute a hash.
f_set = frozenset([10, 20])
print(f"\nFrozenset: {f_set} | Type: {type(f_set)}")

try:
    # Frozensets do not have an 'add' method
    f_set.add(30)
except AttributeError as e:
    print(f"Caught expected AttributeError: {e}")

# Nesting frozenset inside a normal set (works!)
nested_set = {f_set, 30, 40}
print(f"Nested set: {nested_set}")

# Verification of hashability
dict_keys_test = {f_set: "value"}
print(f"Frozenset used as dict key: {dict_keys_test}")
