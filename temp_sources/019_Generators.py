# %% [markdown]
# # Topic: Generators - Lazy evaluations, execution state suspension, and memory efficiency
# 
# ## 1. DEFINITION & ITERATOR PROTOCOL
# - **Generator Function**: A function defined using the `yield` keyword instead of `return`.
# - **Generator Object**: Calling a generator function does NOT execute the body statements. Instead, it instantiates and returns a **Generator Object**.
# - **Iterator Protocol**: The Generator Object automatically implements the Iterator Protocol (defines `__iter__` and `__next__` methods).
# 
# ## 2. STATE SUSPENSION VS FRAME POPPING
# - **Regular Function**: Returns a value, completely destroys its stack frame, and exits.
# - **Generator Function**:
#   - When `next(gen)` is called, Python executes the generator body until it hits a `yield` statement.
#   - It returns the yielded value and **suspends** execution.
#   - Importantly, it keeps the local stack frame, variable references, and the execution instruction pointer alive in heap memory.
#   - The next call to `next(gen)` resumes execution immediately after the last `yield` statement.
#   - When the generator finishes (reaches return or end of function), it raises a `StopIteration` exception.
# 
# ## 3. MEMORY OPTIMIZATION
# - **List Generation**: Allocating a list of $N$ items consumes $O(N)$ memory space.
# - **Generator Generation**: A generator yields items on demand, maintaining only the current value and state references, consuming **$O(1)$ constant space** regardless of the sequence limit length.
# 
# ## 4. INTERVIEW QUESTIONS
# - **Q: What happens internally when a generator executes a yield statement?**
#   - *A*: CPython suspends the execution state of the current frame, saving the instruction pointer and registers on the heap, and passes the yielded value to the caller.
# - **Q: How does a generator communicate that it has completed yielding values?**
#   - *A*: It raises a `StopIteration` exception. In a `for` loop, Python automatically intercepts this exception to terminate the loop cleanly.
# 
# ---

# %%
import sys

# 1. Defining a Generator Function
def simple_generator(max_val):
    """Yields integers from 1 to max_val sequentially."""
    print(" -> Generator started")
    n = 1
    while n <= max_val:
        print(f" -> Suspending state at n={n}")
        yield n  # Suspends execution, returns n
        print(f" -> Resuming execution state at n={n}")
        n += 1
    print(" -> Generator finished")

print("--- Generator Initialization ---")
# Call generator function
gen = simple_generator(3)
print(f"Object: {gen} | Type: {type(gen).__name__}")
# Note: no body prints occurred yet!

# %%
# 2. Sequential execution using next()
print("\n--- Iterating Generator ---")
print(f"Call 1: {next(gen)}")
print(f"Call 2: {next(gen)}")
print(f"Call 3: {next(gen)}")

try:
    print(f"Call 4: {next(gen)}")
except StopIteration:
    print("Caught expected StopIteration: Generator has finished!")

# %%
# 3. Memory Comparison: List vs Generator
print("\n--- Memory Space Optimization ---")
limit = 10000

# List approach allocates all items in memory
list_nums = [i for i in range(limit)]
# Generator approach only retains current state
gen_nums = (i for i in range(limit))

print(f"List size in memory:      {sys.getsizeof(list_nums)} bytes")
print(f"Generator size in memory: {sys.getsizeof(gen_nums)} bytes")
# Expected: Generator is significantly smaller!
