###############################################################################
# TOPIC: Recursion, call Stack Limits, Tail-Call optimization, and Memoization
#
# 1. DEFINITION & INTRODUCTION:
#    - Recursion: A programming technique where a function calls itself, directly or indirectly.
#    - Components:
#        1. Base Case: The terminating condition that exits recursion.
#        2. Recursive Case: The logic block where the function resolves a subproblem by
#           calling itself with a reduced state.
#
# 2. CALL STACK & RECURSION LIMITS:
#    - In CPython, each nested function call allocates an execution frame on the heap.
#    - To prevent runaway infinite recursion from crashing the entire C stack (which causes
#      Segmentation Faults), Python imposes a strict limit on maximum recursion depth.
#    - Default limit: Usually 1000. You can inspect/change it via `sys.getrecursionlimit()`
#      and `sys.setrecursionlimit(limit)`.
#
# 3. TAIL-CALL OPTIMIZATION (Why Python lacks it):
#    - Tail Call Optimization (TCO) is a feature where the compiler collapses a recursive call
#      frame if the recursive call is the last statement executed.
#    - Python deliberately does NOT implement TCO.
#    - Guido van Rossum's Rationale:
#        1. Debugging Tracebacks: TCO discards frame records. Discarding frames makes debugging
#           extremely difficult, as intermediate stack traces disappear.
#        2. Simplicity: Python is built on readability and simplicity, avoiding the complexity
#           of modifying execution frames dynamically at runtime.
#
# 4. OPTIMIZATION VIA MEMOIZATION:
#    - Recursive solutions for overlapping subproblems (e.g. Fibonacci) experience exponential
#      O(2^N) time complexity.
#    - Caching results of function calls (Memoization) reduces this to O(N).
#    - Python provides a built-in decorator for this: `functools.lru_cache`.
#
# 5. BEST PRACTICES:
#    - Prefer iterative approaches (loops) over recursion in Python unless the data structure
#      is naturally recursive (like Trees or Graphs), since loops do not incur frame allocation overhead.
#
# 6. INTERVIEW QUESTIONS:
#    - Q: Does Python optimize tail-recursive functions?
#      A: No. Python does not support Tail-Call Optimization (TCO) to preserve complete,
#         unaltered call stack tracebacks for debugging.
#    - Q: What happens if a recursive function exceeds recursion depth?
#      A: CPython raises a `RecursionError` exception.
#
# 7. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a recursive Fibonacci function and benchmark its speed
#      with and without memoization.
#
###############################################################################

import sys  # Standard library to check recursion limits
import functools  # Standard module containing caching decorators
import time  # Module to benchmark execution times

# 1. Inspect Recursion Limits
print("--- Python Recursion Limits ---")
print(f"Default recursion limit: {sys.getrecursionlimit()}")

# 2. Exceeding Recursion Limit (RecursionError)
def trigger_recursion_limit(depth):
    # Base case absent to force limit crash
    return trigger_recursion_limit(depth + 1)

try:
    trigger_recursion_limit(1)
except RecursionError as e:
    # Safely catch the recursion stack limit error
    print(f"Caught expected RecursionError: {e}")

# 3. Recursive Fibonacci (Without Memoization) - O(2^N)
def fib_naive(n):
    if n <= 1:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)

# 4. Recursive Fibonacci (With Memoization) - O(N)
# lru_cache caches arguments-to-return mappings, bypassing identical sub-evaluations
@functools.lru_cache(maxsize=None)
def fib_memoized(n):
    if n <= 1:
        return n
    return fib_memoized(n - 1) + fib_memoized(n - 2)

# Benchmark comparison
target_num = 32

print("\n--- Naive vs Memoized Recursion ---")
start_naive = time.perf_counter()
res_naive = fib_naive(target_num)
end_naive = time.perf_counter()
naive_time = end_naive - start_naive
print(f"Naive Fib({target_num}) = {res_naive} | Time: {naive_time:.6f} seconds")

start_memo = time.perf_counter()
res_memo = fib_memoized(target_num)
end_memo = time.perf_counter()
memo_time = end_memo - start_memo
print(f"Memoized Fib({target_num}) = {res_memo} | Time: {memo_time:.6f} seconds")
print(f"Memoized is {naive_time / memo_time:.1f}x faster than naive!")
