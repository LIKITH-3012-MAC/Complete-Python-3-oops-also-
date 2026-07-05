###############################################################################
# TOPIC: List Methods, Timsort Sorting, and Iteration Pitfalls
#
# 1. DEFINITION & INTRODUCTION:
#    - Python's `list` provides built-in methods to manipulate elements, search values,
#      and sort structural configurations.
#
# 2. COMPLETE LIST METHODS LIST:
#    - Insertion:
#        - `append(x)`: Appends an item to the end of the list. O(1).
#        - `extend(iterable)`: Extends the list by appending all items from the iterable. O(K).
#        - `insert(i, x)`: Inserts an item at a given index `i`. O(N).
#    - Deletion:
#        - `remove(x)`: Removes the first item whose value is equal to `x`. Raises ValueError if missing. O(N).
#        - `pop(i=-1)`: Removes and returns the item at index `i` (defaults to the last element). O(N) or O(1).
#        - `clear()`: Removes all items. Equivalent to `del list[:]`. O(N).
#    - Utility / Queries:
#        - `index(x, start=0, end=len)`: Returns zero-based index of first match. O(N).
#        - `count(x)`: Returns the number of times `x` appears. O(N).
#        - `reverse()`: Reverses elements of the list in-place. O(N).
#        - `sort(key=None, reverse=False)`: Sorts elements of the list in-place. O(N log N).
#
# 3. TIMSORT ALGORITHM (CPython Sorting Internals):
#    - Python's sorting (both `list.sort()` and the built-in `sorted()` function) uses Timsort.
#    - Designed by Tim Peters in 2002 for Python.
#    - It is a hybrid, stable sorting algorithm derived from Merge Sort and Insertion Sort.
#    - Stable Sort: Preserves the relative order of items with equal values.
#    - Adaptive: Takes advantage of pre-existing sorted subsequences (called "runs") in the data.
#    - Time Complexity:
#        - Worst-case: O(N log N).
#        - Best-case: O(N) (for already sorted lists).
#        - Space Complexity: O(N) auxiliary space.
#
# 4. SORT() VS SORTED():
#    - `list.sort()`: Modifies the list in-place and returns `None`. Extremely memory efficient
#      as it does not allocate a copy of the list.
#    - `sorted(iterable)`: Accepts any iterable, creates and returns a brand new sorted list,
#      leaving the original source unmodified.
#
# 5. ITERATION PITFALL (Modifying during Loop):
#    - Never append or remove elements from a list while iterating over it in a `for` loop.
#    - Python loops track iteration using an internal integer index counter. Removing items shifts
#      elements left, causing the loop to skip the adjacent item or raise unexpected index issues.
#
# 6. INTERVIEW QUESTIONS:
#    - Q: What algorithm does Python use for sorting, and what is its best-case time complexity?
#      A: Python uses Timsort. Its best-case complexity is O(N) for inputs that are already sorted,
#         requiring only a single check sweep.
#    - Q: What is a "stable" sort?
#      A: A sorting algorithm that keeps the original relative ordering of records with equal keys
#         intact.
#
# 7. EXERCISES & SOLUTIONS:
#    - Coding challenge: Sort a list of tuples containing student names and test scores first by
#      score descending, and then by name alphabetically (secondary key) using the `key` argument.
#
###############################################################################

# 1. Base List Methods Demonstration
demo_list = [10, 20, 30]

print("--- Base List Operations ---")
demo_list.append(40)  # Insert end
print(f"After append(40): {demo_list}")

demo_list.extend([50, 60])  # Extend list
print(f"After extend([50, 60]): {demo_list}")

demo_list.insert(1, 99)  # Insert index 1
print(f"After insert(1, 99): {demo_list}")  # Expected: [10, 99, 20, 30, 40, 50, 60]

removed_item = demo_list.pop(1)  # Remove index 1
print(f"Popped item: {removed_item} | Current List: {demo_list}")

demo_list.remove(30)  # Remove value 30
print(f"After remove(30): {demo_list}")

# 2. Sort() vs Sorted() Comparison
unsorted_list = [5, 2, 9, 1, 5, 6]

print("\n--- Sort() vs Sorted() ---")
# Using sorted() - Returns new list
sorted_result = sorted(unsorted_list)
print(f"Original: {unsorted_list}")
print(f"sorted() Output: {sorted_result}")

# Using sort() - In-place mutation
unsorted_list.sort()
print(f"After inline sort(): {unsorted_list}")  # Expected: [1, 2, 5, 5, 6, 9]

# 3. Custom Key Sort & Stability (Timsort)
# Sort students: first by score descending, then by age ascending.
# Student data structure: (name, score, age)
students = [
    ("Alice", 90, 22),
    ("Bob", 85, 20),
    ("Charlie", 90, 19),
    ("David", 85, 23)
]

# We sort using key lambda return tuple.
# Python supports tuple sorting: compares elements sequentially (first element, then second on tie).
# To sort score descending and age ascending, we pass (-score, age).
students.sort(key=lambda s: (-s[1], s[2]))
print("\n--- Sorted Student Records ---")
print(students)
# Expected Output: [('Charlie', 90, 19), ('Alice', 90, 22), ('Bob', 85, 20), ('David', 85, 23)]
# Charlie before Alice because 19 < 22. Bob before David because 20 < 23.

# 4. Modifying during Iteration Pitfall Proof
pitfall_list = [1, 2, 3, 4]
print("\n--- Modifying list during loop pitfall ---")
print(f"Original: {pitfall_list}")

# Attempt to remove even numbers in a loop (Incorrect)
for item in pitfall_list:
    if item % 2 == 0:
        pitfall_list.remove(item)

print(f"List after loop removal: {pitfall_list}")
# Expected Output: [1, 3, 4]. Note that '4' was skipped!
# Explanation: When 2 was removed, 3 shifted to index 1, 4 shifted to index 2.
# The iterator index advanced to 2, directly reading 4 and skipping 3 entirely.
