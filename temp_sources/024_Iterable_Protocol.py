# %% [markdown]
# # Topic: Iterable Protocol - __iter__ returning fresh iterators, and __getitem__ index fallbacks
# 
# ## 1. THE ITERABLE PROTOCOL
# - **Iterable**: An object that can return its elements one at a time (e.g. list, tuple, dictionary, set, string).
# - **The Iterable Protocol**: An object is iterable if it implements:
#   - **`__iter__()`**: Must return an **iterator** object instance.
# - **Multi-use Loop behavior**:
#   - Unlike an iterator (which exhausts itself), an iterable can be looped over multiple times.
#   - Every time a `for` loop begins on an iterable, Python calls `iter(iterable)` to obtain a **fresh iterator** instance, leaving the parent iterable's sequence data unmodified.
# 
# ## 2. THE GETITEM FALLBACK MECHANISM
# - If an object does not implement `__iter__()`, but has a **`__getitem__()`** method:
#   1. Python's built-in `iter()` function falls back to using `__getitem__()`.
#   2. It creates a wrapper iterator that fetches values sequentially by calling `obj[0]`, `obj[1]`, `obj[2]`, etc.
#   3. The loop continues until a `IndexError` exception is raised, signaling termination.
# 
# ## 3. INTERVIEW QUESTIONS
# - **Q: How does a `for` loop work under the hood?**
#   - *A*: It first calls `iter(obj)` to get an iterator. Then it repeatedly calls `next(iterator)` to retrieve elements, catching `StopIteration` to exit the loop.
# - **Q: What is the fallback if an object does not implement `__iter__`?**
#   - *A*: Python searches for `__getitem__`. If present, it generates a virtual iterator invoking indexes sequentially from `0` upwards until it encounters an `IndexError`.
# 
# ---

# %%
# 1. Custom Iterable creating fresh Iterators
class SentenceIterator:
    """The Iterator: keeps state (index cursor)."""
    def __init__(self, words):
        self.words = words
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.words):
            raise StopIteration
        word = self.words[self.index]
        self.index += 1
        return word

class Sentence:
    """The Iterable: contains data and returns a fresh iterator on each call."""
    def __init__(self, text):
        self.words = text.split()

    def __iter__(self):
        # Always return a fresh iterator instance!
        return SentenceIterator(self.words)

print("--- Custom Iterable Execution ---")
my_sentence = Sentence("Python is beautiful")

print("First iteration:")
for word in my_sentence:
    print(f" -> {word}")

print("Second iteration (starts fresh!):")
for word in my_sentence:
    print(f" -> {word}")

# %%
# 2. Getitem Fallback Mechanism Demo
class IndexIterable:
    """Does NOT define __iter__, but defines __getitem__."""
    def __init__(self, items):
        self.items = items

    def __getitem__(self, index):
        # Python calls obj[0], obj[1], obj[2] ... until IndexError
        return self.items[index]

print("\n--- Fallback __getitem__ Iteration ---")
fallback_obj = IndexIterable(["A", "B", "C"])

# Even without __iter__, this loop succeeds!
for item in fallback_obj:
    print(f" -> Fallback item: {item}")
