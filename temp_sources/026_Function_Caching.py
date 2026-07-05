# %% [markdown]
# # Topic: Function Caching - Memoization patterns, Least Recently Used (LRU) evictions, and typed cache partitions
# 
# ## 1. DEFINITION: FUNCTION CACHING
# - **Function Caching (Memoization)**: An optimization technique where you store the results of expensive function calls in memory and return the cached result when the same inputs occur again.
# - **Primary Use Case**: Pure functions with heavy CPU calculations or redundant recursive branches (like Fibonacci computation).
# 
# ## 2. CPYTHON LRU_CACHE: functools
# - **Least Recently Used (LRU)**: Discards the least recently accessed items first when the cache size reaches its limit.
# - **functools.lru_cache(maxsize=128, typed=False)**:
#   - Decorates functions to enable automatic memoization.
#   - **`maxsize`**: The maximum number of entries to keep in cache. Setting `maxsize=None` disables cache eviction, allowing it to grow unbounded (behaving like `functools.cache`).
#   - **`typed`**: If set to `True`, arguments of different types will be cached separately (e.g., `f(3)` and `f(3.0)` create distinct entries).
# - **Prerequisite**: Arguments passed to a cached function must be **hashable** (immutable), since Python uses them as dictionary keys internally.
# 
# ## 3. INTERVIEW QUESTIONS
# - **Q: What is an LRU cache, and when should you use it?**
#   - *A*: Least Recently Used cache keeps the most recently requested values in a map, discarding the oldest unused entries when full. Use it to optimize pure, deterministic functions that are called frequently with repeating inputs.
# - **Q: Can you pass a list as an argument to a function decorated with `@lru_cache`?**
#   - *A*: No, list is unhashable. Doing so raises a `TypeError: unhashable type: 'list'`.
# 
# ---

# %%
import time
from functools import lru_cache

# 1. Without caching: Recursive Fibonacci is O(2^N)
def fib_naive(n):
    if n < 2:
        return n
    return fib_naive(n-1) + fib_naive(n-2)

# 2. With caching: Recursive Fibonacci is O(N)
@lru_cache(maxsize=None)  # Unbounded caching
def fib_cached(n):
    if n < 2:
        return n
    return fib_cached(n-1) + fib_cached(n-2)

print("--- Performance Comparison ---")
# Benchmark Naive Fibonacci (n=35)
t0 = time.time()
result_naive = fib_naive(35)
t1 = time.time()
print(f"Naive result: {result_naive} | Time taken: {t1 - t0:.4f} seconds")

# Benchmark Cached Fibonacci (n=35)
t0 = time.time()
result_cached = fib_cached(35)
t1 = time.time()
print(f"Cached result: {result_cached} | Time taken: {t1 - t0:.4f} seconds")
# Expected: Cached is practically instantaneous (0.00s)!

# %%
# 3. LRU Cache Limits and Eviction
@lru_cache(maxsize=3)
def process_data(x):
    print(f" -> [EVAL] Computing process_data({x})")
    return x * 10

print("\n--- LRU Cache Eviction (maxsize=3) ---")
process_data(1)  # Evaluated
process_data(2)  # Evaluated
process_data(3)  # Evaluated

# Retrieve from cache
print(f"Fetch cached 1: {process_data(1)}")  # Cache hit (no EVAL printed)

# Add new item, exceeding maxsize limit of 3
# Evicts least recently used item (which is '2', since '1' was just fetched!)
process_data(4)  # Evaluated

print("Checking if '2' is evicted:")
process_data(2)  # Evaluated again (since it was evicted!)

# %%
# 4. Typed Caching (Float vs Int distinction)
@lru_cache(maxsize=128, typed=True)
def multiply_by_two(val):
    print(f" -> Evaluated for {val} (type: {type(val).__name__})")
    return val * 2

print("\n--- Typed Caching (typed=True) ---")
multiply_by_two(5)    # Evaluated
multiply_by_two(5.0)  # Evaluated separately because of typed=True!
multiply_by_two(5)    # Cache hit
