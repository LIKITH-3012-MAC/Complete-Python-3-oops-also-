###############################################################################
# TOPIC: Tuples - Immutability, Memory optimization, and NamedTuples
#
# 1. DEFINITION & INTRODUCTION:
#    - Python's `tuple` is an immutable, ordered sequence of heterogeneous objects.
#    - Although values inside a tuple cannot be changed after creation, the tuple itself
#      can contain mutable objects (e.g., lists), whose states can be modified.
#
# 2. CPYTHON INTERNAL STRUCTURE:
#    - A tuple is represented by the `PyTupleObject` C struct:
#      ```c
#      typedef struct {
#          PyObject_VAR_HEAD
#          PyObject *ob_item[1];
#      } PyTupleObject;
#      ```
#    - Contiguous Array: `ob_item` is a contiguous array of pointers to `PyObject` structures.
#    - Unlike lists, tuples are fixed-size. There is no `allocated` capacity tracker; the
#      allocated size is exactly the tuple's length. This saves memory and allocation overhead.
#
# 3. TUPLE MEMORY OPTIMIZATIONS (Freelist cache):
#    CPython implements highly optimized memory reuse patterns for tuples:
#    - Empty Tuple Singleton: Since empty tuples are immutable and identical, CPython creates a
#      single global empty tuple object. Any call to `tuple()` or `()` returns this singleton.
#    - Deallocation Freelist: To speed up memory allocation, CPython retains a cache of freed
#      tuples (up to 2000 elements for each tuple size from 1 to 20).
#      When a tuple of size <= 20 is destroyed, its C structure is not returned to the heap;
#      instead, it is saved in a "freelist" array. Subsequent creations of tuples of that size
#      instantly reuse this C structure, bypassing system allocator routines.
#
# 4. SYNTAX RULE:
#    - To define a tuple with exactly one element, you MUST include a trailing comma (e.g., `(1,)`).
#      Writing `(1)` is parsed as an integer grouped in standard parentheses, not a tuple.
#
# 5. NAMED TUPLES:
#    - `collections.namedtuple`: Factory function for creating tuples with named fields,
#      allowing attribute access by name (e.g., `point.x`) while maintaining tuple properties.
#    - `typing.NamedTuple`: Modern alternative subclassing syntax that supports type hints.
#
# 6. TIME & SPACE COMPLEXITY:
#    - Access by index: O(1).
#    - Tuple Creation: Faster than list creation due to static sizing and freelists.
#    - Space: Smaller overhead than lists. A list has growth padding; a tuple has zero padding.
#
# 7. INTERVIEW QUESTIONS:
#    - Q: Can a tuple be used as a key in a dictionary?
#      A: Yes, but ONLY if all elements inside the tuple are themselves hashable (immutable).
#         A tuple containing a list (e.g. `(1, [2, 3])`) is unhashable and will raise a `TypeError`.
#    - Q: Why are tuples faster to construct than lists?
#      A: Tuples have a fixed size and use CPython freelist pools to recycle allocated structs,
#         preventing repeated system allocator overheads.
#
# 8. EXERCISES & SOLUTIONS:
#    - Coding challenge: Prove that all declarations of empty tuples (`()`, `tuple()`) reference the
#      exact same object ID, and compare the construction speeds of lists vs tuples.
#
###############################################################################

import sys  # Standard library to inspect memory sizes
import timeit  # Module to benchmark speed differences
from collections import namedtuple  # standard namedtuple factory
from typing import NamedTuple  # typed NamedTuple class wrapper

# 1. Single-element Tuple Syntax
t_wrong = (1)    # An integer, not a tuple
t_correct = (1,)  # A valid tuple with 1 element

print("--- Tuple Syntax Check ---")
print(f"Type of (1):   {type(t_wrong)}")    # Expected: <class 'int'>
print(f"Type of (1,):  {type(t_correct)}")   # Expected: <class 'tuple'>

# 2. Empty Tuple Singleton Proof
t_empty1 = ()
t_empty2 = tuple()
print(f"\nEmpty tuples are singletons: {t_empty1 is t_empty2}")  # Expected: True

# 3. Tuple Immutability vs Element Mutability
# A tuple is structurally immutable (pointers cannot change), but if it holds a mutable list,
# the contents of that list can be modified.
complex_tuple = (1, 2, [3, 4])
print(f"\nBefore nested list update: {complex_tuple}")
try:
    # Attempting to assign a new pointer will fail
    complex_tuple[0] = 99
except TypeError as e:
    print(f"Caught expected TypeError (pointer change): {e}")

# Mutating the list element (works!)
complex_tuple[2].append(5)
print(f"After nested list update:  {complex_tuple}")  # Expected: (1, 2, [3, 4, 5])

# 4. Space Efficiency: Tuple vs List
# Check how many bytes a list consumes compared to a tuple of the same size.
sample_list = [1, 2, 3, 4, 5]
sample_tuple = (1, 2, 3, 4, 5)
print(f"\nMemory Size (List):  {sys.getsizeof(sample_list)} bytes")
print(f"Memory Size (Tuple): {sys.getsizeof(sample_tuple)} bytes")  # Expected: Tuple is smaller

# 5. Construction Speed: Tuple vs List
iterations = 10000000
time_list = timeit.timeit("x = [1, 2, 3, 4, 5]", number=iterations)
time_tuple = timeit.timeit("x = (1, 2, 3, 4, 5)", number=iterations)
print(f"\nConstruction speed of 10 Million lists:  {time_list:.4f} seconds")
print(f"Construction speed of 10 Million tuples: {time_tuple:.4f} seconds")
print(f"Tuple construction is {time_list / time_tuple:.1f}x faster than list!")

# 6. NamedTuples (Classic and Typed)
# Classic collections.namedtuple
Point2D = namedtuple("Point2D", ["x", "y"])
p1 = Point2D(10, 20)

# Typed typing.NamedTuple
class UserProfile(NamedTuple):
    username: str
    age: int

u1 = UserProfile(username="likith", age=25)

print("\n--- NamedTuples ---")
print(f"p1: {p1} | Access by name: p1.x={p1.x} | Access by index: p1[0]={p1[0]}")
print(f"u1: {u1} | Access by name: u1.username={u1.username}")
