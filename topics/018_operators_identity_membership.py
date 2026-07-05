###############################################################################
# TOPIC: Identity (is) and Membership (in) Operators
#
# 1. DEFINITION & INTRODUCTION:
#    - Identity Operators (`is`, `is not`): Compare if two reference variables point to
#      the exact same object in memory.
#    - Membership Operators (`in`, `not in`): Test if a value exists within an iterable
#      or container object.
#
# 2. IDENTITY OPERATOR MECHANICS:
#    - `x is y` is equivalent to evaluating `id(x) == id(y)`.
#    - Memory Address Comparison: It checks the raw pointers of the objects at the C level,
#      making it an extremely fast operation.
#    - Standard Use: Almost exclusively used to check singletons like `None`.
#
# 3. MEMBERSHIP OPERATOR MECHANICS & COMPLEXITY:
#    - The performance of the `in` operator depends entirely on the type of container:
#        - Lists & Tuples: O(N) linear search. Python iterates through the elements
#          one by one, checking value equality (`==`).
#        - Dictionaries & Sets: O(1) average-case time complexity. Python uses the hash value
#          of the target element to look it up in a hash table immediately.
#        - Strings: O(N * M) worst-case (using optimized substring search algorithms).
#
# 4. CUSTOM CONTAINER MEMBERSHIP:
#    - When you call `item in container`, Python determines containment by looking for
#      magic methods in the following order:
#        1. `container.__contains__(item)`: Should return `True` or `False`.
#        2. If not defined, Python falls back to the iterator protocol `__iter__()`. It will
#           iterate over the container, checking equality against each item.
#        3. If `__iter__()` is missing, it falls back to `__getitem__(index)`. It fetches elements
#           sequentially by integer indices starting from 0 until an `IndexError` is raised.
#
# 5. BEST PRACTICES:
#    - Use `is None` instead of `== None`.
#    - When membership checks are frequent or the collection is large, store elements
#      in a `set` rather than a `list` to benefit from O(1) hash-based lookups.
#
# 6. INTERVIEW QUESTIONS:
#    - Q: Why is `in` faster on sets than on lists?
#      A: Sets are implemented as hash tables. Finding an item requires hashing it and
#         checking the calculated bucket, which takes O(1) time. Lists are arrays, requiring
#         an O(N) sequential search through each element.
#    - Q: What does `x in dict` check: keys or values?
#      A: Keys. Checking membership on a dictionary evaluates against the keys.
#
# 7. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a custom database-like class that tracks user IDs and
#      customizes the `__contains__` method to print a lookup query message.
#
###############################################################################

import time  # Standard library to benchmark search operations

# 1. Identity Operator (is) vs Equality (==)
ref_a = [10, 20]
ref_b = ref_a
ref_c = [10, 20]

print("--- Identity Operators ---")
print(f"ref_a is ref_b: {ref_a is ref_b}")  # Expected: True (Both point to same object)
print(f"ref_a is ref_c: {ref_a is ref_c}")  # Expected: False (Different list objects in memory)
print(f"ref_a == ref_c: {ref_a == ref_c}")  # Expected: True (Values are identical)

# Checking for None singleton (PEP 8 standard)
val = None
print(f"val is None: {val is None}")  # Expected: True

# 2. Benchmarking Membership Search (O(N) List vs O(1) Set)
# We will construct a large list and a large set of the same elements and search for a missing item.
item_count = 100000
large_list = list(range(item_count))
large_set = set(range(item_count))
missing_item = 999999

# Benchmark List Search (Linear O(N))
start_list = time.perf_counter()
is_in_list = missing_item in large_list
end_list = time.perf_counter()
list_duration = end_list - start_list

# Benchmark Set Search (Hash O(1))
start_set = time.perf_counter()
is_in_set = missing_item in large_set
end_set = time.perf_counter()
set_duration = end_set - start_set

print("\n--- Membership Benchmarks ---")
print(f"List search duration: {list_duration:.6f} seconds")
print(f"Set search duration:  {set_duration:.6f} seconds")
print(f"Set search is {list_duration / set_duration:.1f}x faster than list search!")

# 3. Custom Membership Magic Method
class LibraryCatalog:
    def __init__(self):
        self.books = {"Dune", "1984", "Foundation"}
        
    def __contains__(self, book_name):
        # intercepting membership operator checks
        print(f" -> Checking catalog database for '{book_name}'...")
        return book_name in self.books

catalog = LibraryCatalog()
print("\n--- Custom Membership Hook ---")
print(f"Is '1984' in catalog? {'1984' in catalog}")  # Expected: True, calls __contains__
print(f"Is 'Hamlet' in catalog? {'Hamlet' in catalog}")  # Expected: False
