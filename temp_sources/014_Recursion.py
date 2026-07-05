# %% [markdown]
# # Topic: Recursion - Base cases, call stack frames, and CPython recursion limit overrides
# 
# ## 1. DEFINITION & ANATOMY
# - **Recursion**: A programming technique where a function calls itself, directly or indirectly, to solve a problem by dividing it into smaller sub-problems.
# - **Anatomy**:
#   1. **Base Case**: The termination condition that returns a value directly without making further recursive calls. Prevents infinite loops.
#   2. **Recursive Step**: The block where the function invokes itself, reducing the arguments to move closer to the base case.
# 
# ## 2. CALL STACK FRAME MECHANICS
# - When a recursive function is called:
#   - Every call pushes a new **Stack Frame** onto CPython's call stack, allocating memory for local variables and parameters.
#   - If the recursion is $N$ levels deep, it consumes $O(N)$ stack space.
#   - Once the base case triggers, frames are popped off the stack sequentially.
# 
# ## 3. CPYTHON SYSTEM RECURSION LIMITS
# - **Recursion Limit**: Python has a guard limit (typically `1000`) to prevent C stack overflows from crashing the interpreter.
# - Exceeding this limit raises: `RecursionError: maximum recursion depth exceeded`.
# - **Dynamic Overrides**: You can inspect and modify this safety threshold using the standard `sys` module:
#   - `sys.getrecursionlimit()`
#   - `sys.setrecursionlimit(new_limit)`
# - **No Tail-Call Optimization (TCO)**:
#   - CPython does NOT support Tail-Call Optimization.
#   - Even if the recursive call is the last statement (tail position), a new stack frame is always allocated. Guido van Rossum explicitly chose not to support TCO to maintain clear stack trace diagnostic tracebacks.
# 
# ## 4. INTERVIEW QUESTIONS
# - **Q: Why does Python raise a RecursionError, and how do you resolve it?**
#   - *A*: It raises a RecursionError when a recursive chain exceeds the default limit (1000) to prevent OS thread stack overflows. You can increase it via `sys.setrecursionlimit()`, but it is better to rewrite the function iteratively to use $O(1)$ space.
# - **Q: Does Python support Tail-Call Optimization?**
#   - *A*: No. Every recursive call creates a new stack frame.
# 
# ---

# %%
import sys

print("--- System Recursion Limit ---")
print(f"Default limit: {sys.getrecursionlimit()}")

# We can raise the limit if needed (exercise caution to prevent actual C stack crash)
sys.setrecursionlimit(1500)
print(f"Updated limit: {sys.getrecursionlimit()}")

# Restore default
sys.setrecursionlimit(1000)

# %%
# 1. Classical Recursive Implementation: Factorial
def factorial(n):
    """Calculates n! recursively."""
    # Base Case
    if n <= 1:
        return 1
    # Recursive Step
    return n * factorial(n - 1)

print("\n--- Recursive Factorial ---")
print(f"factorial(5): {factorial(5)}")  # Expected: 120

# %%
# 2. Call Stack Limit Validation
def infinite_recursion(depth):
    # This will trigger RecursionError
    return infinite_recursion(depth + 1)

print("\n--- Triggering RecursionError ---")
try:
    infinite_recursion(1)
except RecursionError as e:
    print(f"Caught expected RecursionError: {e}")

# %%
# 3. Iterative Alternative (Safe from stack overflow, O(1) space)
def factorial_iterative(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

print("\n--- Iterative Factorial (O(1) Space) ---")
print(f"factorial_iterative(5): {factorial_iterative(5)}")  # Expected: 120
