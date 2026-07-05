###############################################################################
# TOPIC: Dictionary Internals - Hash Tables, order Preservation, and Compact layout
#
# 1. DEFINITION & INTRODUCTION:
#    - Python's `dict` is a mutable collection of key-value pairs, providing fast lookup,
#      insertion, and deletion.
#
# 2. HASH TABLE IMPLEMENTATION & COLLISION RESOLUTION:
#    - Dictionaries are implemented as hash tables.
#    - When you lookup `dict[key]`, Python computes the hash value of the key: `hash(key)`.
#    - It uses the lower bits of the hash as an index to find the entry bucket.
#    - Collision Resolution: If two keys hash to the same bucket (collision), CPython uses
#      Open Addressing with a pseudo-random probe sequence.
#      Formula: `i = (5 * i + 1 + perturb) % mask` (where perturb decays, shifting rights).
#      This walks the array systematically to locate the next free or matching slot.
#
# 3. COMPACT DICTIONARY REPRESENTATION (CPython 3.6+ Optimization):
#    - Prior to Python 3.6, the dictionary table was a single sparse array where each entry
#      occupied 24 bytes (8 bytes hash, 8 bytes key pointer, 8 bytes value pointer).
#      This wasted significant memory due to empty slots (usually 1/3 of the table was empty).
#    - In CPython 3.6+ (borrowed from PyPy), the layout was split into two arrays:
#        1. `dk_indices`: A small, dense array of integers (bytes, half-words, or words) representing buckets.
#        2. `dk_entries`: A compact, contiguous array containing only actual inserted records:
#           `[ {hash, key_ptr, value_ptr}, ... ]`.
#    - When looking up a key, Python hashes it to find an index in `dk_indices`. The integer stored
#      there (e.g., 2) represents the offset of the actual entry inside `dk_entries`.
#    - Since the sparse array now only stores small integers instead of large 24-byte structs,
#      this design reduces dictionary memory footprint by 30% to 40%!
#
# 4. INSERTION ORDER PRESERVATION:
#    - As a side-effect of the compact dictionary design, elements in `dk_entries` are appended
#      sequentially in the exact order they are inserted.
#    - Thus, iterating over a dictionary yields keys in their insertion order!
#      This was an implementation detail in 3.6 and became a formal language specification in 3.7.
#
# 5. KEY-SHARING DICTIONARIES (PEP 412):
#    - For custom class instances, the attributes are stored inside `self.__dict__`.
#    - Since instances of the same class share identical attribute names (keys) and differ only in
#      their values, PEP 412 splits the dictionaries:
#        - Keys are stored in a single shared table associated with the class.
#        - Values are stored in a simple array associated with each instance.
#      This eliminates duplicate key string allocations across hundreds of instances.
#
# 6. TIME COMPLEXITY:
#    - Lookup, Insertion, Deletion: O(1) average-case. O(N) worst-case (if all keys collide).
#
# 7. INTERVIEW QUESTIONS:
#    - Q: How did dictionaries become insertion-ordered in Python?
#      A: In Python 3.6, the memory layout was split into a small sparse indices array and a
#         compact, contiguous entries array. Appending new items sequentially to the entries array
#         naturally preserved insertion order.
#    - Q: What makes a class instance dictionary memory-efficient?
#      A: PEP 412 Key-Sharing. Class instances share a single key layout descriptor dictionary,
#         storing only values array locally.
#
# 8. EXERCISES & SOLUTIONS:
#    - Coding challenge: Prove that dictionary insertion order is preserved, and write a custom
#      lookup class to show how dictionaries handle hash collisions.
#
###############################################################################

import sys  # Standard library to inspect memory sizes of dictionaries

# 1. Order Preservation Demonstration
print("--- Dictionary Order Preservation ---")
# Insert elements in a specific order
d = {}
d["banana"] = 1
d["apple"] = 2
d["cherry"] = 3

print("Iterating dictionary keys (preserves insertion order):")
# Expected: banana, then apple, then cherry
for key in d:
    print(f"  Key: {key:<7} | Value: {d[key]}")

# 2. Dictionary Memory Savings Proof
# Compare memory of dict in 3.6+ vs theoretical old style (which was heavier)
empty_dict = {}
small_dict = {"a": 1, "b": 2}
print(f"\nEmpty dict size: {sys.getsizeof(empty_dict)} bytes")
print(f"2-item dict size: {sys.getsizeof(small_dict)} bytes")

# 3. Hash Collision Simulation
# To understand collision resolution, we define a class with a custom hash that always returns 42.
# This forces the dictionary to handle collision resolution.
class CollidingKey:
    def __init__(self, name):
        self.name = name
        
    def __hash__(self):
        # Force all instances of this class to hash to the same bucket
        return 42
        
    def __eq__(self, other):
        if not isinstance(other, CollidingKey):
            return False
        # Equality check ensures Python can tell them apart during lookup
        return self.name == other.name
        
    def __repr__(self):
        return f"Key({self.name})"

# Instantiate colliding keys
k1 = CollidingKey("First")
k2 = CollidingKey("Second")
k3 = CollidingKey("Third")

collision_dict = {}
collision_dict[k1] = "A"
collision_dict[k2] = "B"
collision_dict[k3] = "C"

# Verify all are present. Python successfully stored all keys despite having the same hash.
# It did this by probing the next indices using open addressing collision resolution.
print("\n--- Collision Dictionary Contents ---")
for key, val in collision_dict.items():
    print(f"Key: {key} (hash={hash(key)}) | Value: {val}")

# Lookup k2 (should resolve and return 'B')
print(f"Lookup k2: {collision_dict[k2]}")  # Expected: 'B'
