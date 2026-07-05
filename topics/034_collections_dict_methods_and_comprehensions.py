###############################################################################
# TOPIC: Dictionary Methods, Views, Comprehensions, and Merge Operators
#
# 1. DEFINITION & INTRODUCTION:
#    - Python dictionaries feature methods for safe lookup, modifications, dynamic views,
#      and structural merges.
#
# 2. COMPLETE DICTIONARY METHODS:
#    - Query & Safe Access:
#        - `get(key, default=None)`: Returns value for key if key is in dictionary, else default.
#          Prevents `KeyError`.
#        - `setdefault(key, default=None)`: If key is in dictionary, return its value.
#          If not, insert key with a value of default and return default. Useful for groups.
#    - Removal:
#        - `pop(key, default)`: Removes specified key and returns the corresponding value.
#          If not found, returns default, or raises KeyError if no default is provided.
#          `popitem()`: Removes and returns a `(key, value)` pair. Pairs are returned in LIFO order.
#    - Creation & Updates:
#        - `fromkeys(iterable, value=None)`: Class method creating a new dict with keys from iterable.
#        - `update([other])`: Update the dictionary with the key-value pairs from other, overwriting existing keys.
#
# 3. DICTIONARY VIEWS:
#    - Methods `.keys()`, `.values()`, and `.items()` do not return static list copies of keys/values.
#      Instead, they return dictionary view objects (`dict_keys`, `dict_values`, `dict_items`).
#    - View properties:
#        - Dynamic: Any change to the dictionary is immediately reflected in the view objects.
#        - Set-like: Keys and items views support set operations (like union, intersection) because
#          keys are unique and hashable.
#
# 4. DICTIONARY COMPREHENSIONS:
#    - Syntactic shortcut to create dictionaries: `{key_expr: value_expr for item in iterable if condition}`.
#
# 5. MERGE OPERATORS (PEP 584 - Python 3.9+):
#    - Python 3.9 introduced dictionary merge (`|`) and update (`|=`) operators.
#    - `d1 | d2`: Returns a new dictionary containing the union of d1 and d2. If keys overlap,
#      d2's values take precedence.
#    - `d1 |= d2`: Updates d1 in-place with keys and values from d2.
#
# 6. INTERVIEW QUESTIONS:
#    - Q: Explain what `dict.setdefault()` does.
#      A: It checks if a key exists. If it does, it returns the value. If not, it inserts the key
#         with the specified default value and returns that default value.
#    - Q: What makes dictionary views special?
#      A: They do not copy dictionary elements (saving memory) and dynamically reflect changes
#         to the source dictionary instantly. Keys/Items views also support set operations.
#
# 7. EXERCISES & SOLUTIONS:
#    - Coding challenge: Given a list of words, group them by their starting letter using a dictionary
#      and the `setdefault` method.
#
###############################################################################

# 1. Safe Access: get() and setdefault()
print("--- Dictionary Safe Access ---")
info = {"name": "Alice"}

# get() prevents KeyError
print(f"get('age') (returns default): {info.get('age', 18)}")

# setdefault() for grouping
# Suppose we want to build a group mapping.
group_map = {}
group_map.setdefault("users", []).append("Alice")
group_map.setdefault("users", []).append("Bob")
group_map.setdefault("admins", []).append("Guido")
print(f"setdefault Group Map: {group_map}")
# Expected: {'users': ['Alice', 'Bob'], 'admins': ['Guido']}

# 2. Dictionary Views (Dynamic Behavior)
print("\n--- Dictionary Dynamic Views ---")
inventory = {"apples": 10, "bananas": 5}
keys_view = inventory.keys()
items_view = inventory.items()

print(f"Keys view: {keys_view}")
# Modify the underlying dictionary
inventory["cherries"] = 15
# The view updates automatically without re-evaluating keys()!
print(f"Keys view after insertion: {keys_view}")  # Expected: contains 'cherries'

# Set-like behaviors of views
other_set = {"apples", "grapes"}
common_keys = keys_view & other_set  # Set intersection on view!
print(f"Intersection of keys view and set: {common_keys}")  # Expected: {'apples'}

# 3. Dictionary Comprehension
words = ["python", "is", "awesome"]
word_lengths = {word: len(word) for word in words}
print(f"\nDictionary Comprehension: {word_lengths}")

# 4. Merging Dictionaries (PEP 584)
dict_x = {"a": 1, "b": 2}
dict_y = {"b": 99, "c": 3}

# Merge operator '|' creates a new dict. Overlapping keys take right-hand value (dict_y)
merged_dict = dict_x | dict_y
print(f"\nMerged (dict_x | dict_y): {merged_dict}")  # Expected: {'a': 1, 'b': 99, 'c': 3}

# Update operator '|=' modifies in-place
dict_x |= dict_y
print(f"In-place updated dict_x: {dict_x}")  # Expected: {'a': 1, 'b': 99, 'c': 3}
