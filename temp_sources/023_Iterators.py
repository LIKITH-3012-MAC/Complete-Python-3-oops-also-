# %% [markdown]
# # Topic: Iterators - Iterator Protocol (__iter__ / __next__), stateful streams, and iterator exhaustion
# 
# ## 1. DEFINITION & ITERATOR PROTOCOL
# - **Iterator**: An object that represents a stream of data.
# - **The Iterator Protocol**: An object is an iterator if it implements:
#   1. **`__iter__()`**: Returns the iterator object itself. This allows iterators to be used in `for` loops.
#   2. **`__next__()`**: Returns the next item from the stream. If there are no more elements, it must raise a `StopIteration` exception.
# 
# ## 2. STATEFUL STREAM & EXHAUSTION
# - **State Preservation**: An iterator maintains internal state (such as the current index pointer or reference to the collection) to know what element to return next.
# - **One-time Iteration (Exhaustion)**:
#   - Once an iterator yields all of its elements and raises `StopIteration`, it is **exhausted**.
#   - Subsequent calls to `next()` continue to raise `StopIteration`.
#   - You cannot reset or restart an exhausted iterator; you must instantiate a new iterator object.
# 
# ## 3. INTERVIEW QUESTIONS
# - **Q: What is the difference between an iterable and an iterator?**
#   - *A*: An iterable is any object that can return an iterator (defines `__iter__()` or `__getitem__()`). An iterator is the stateful stream object itself that yields values via `__next__()` and returns itself in `__iter__()`.
# - **Q: Can you run a `for` loop twice over an iterator?**
#   - *A*: No. The first loop consumes all elements, exhausting the iterator. The second loop starts on an exhausted state, immediately receiving `StopIteration` and returning no elements.
# 
# ---

# %%
# 1. Custom Iterator Implementation
class CountDown:
    """An iterator that counts down from start to 1."""
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        # Iterator protocol: return self
        return self

    def __next__(self):
        # Stateful check
        if self.current <= 0:
            # Exhaustion signal
            raise StopIteration
        val = self.current
        self.current -= 1
        return val

print("--- Custom Iterator Execution ---")
counter = CountDown(3)

# Retrieve elements using next()
print(f"Next 1: {next(counter)}")  # Expected: 3
print(f"Next 2: {next(counter)}")  # Expected: 2
print(f"Next 3: {next(counter)}")  # Expected: 1

try:
    print(f"Next 4: {next(counter)}")
except StopIteration:
    print("Caught expected StopIteration! Iterator is exhausted.")

# %%
# 2. Testing loop behavior on exhausted iterator
print("\n--- Testing Exhaustion in loops ---")
iterator = CountDown(2)

print("First loop execution:")
for x in iterator:
    print(f" -> {x}")

print("Second loop execution (over same iterator):")
for x in iterator:
    print(f" -> {x}")
# Expected: Second loop prints nothing!
