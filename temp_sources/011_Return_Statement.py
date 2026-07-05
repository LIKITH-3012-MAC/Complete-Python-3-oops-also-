# %% [markdown]
# # Topic: Return Statement - Implicit returns, tuple packing, and RETURN_VALUE bytecode
# 
# ## 1. DEFINITION & BEHAVIOR
# - **Return Statement**: Terminates the execution of a function and passes a value (or object reference) back to the calling scope.
# - **Termination**: Any code written after a executed `return` statement in the same block is unreachable (dead code).
# 
# ## 2. IMPLICIT RETURNS & NONE
# - **Implicit Return**: If a function does not contain a `return` statement, or reaches the end of its body without hitting a return, Python implicitly returns `None`.
# - **Bare Return**: Writing `return` without specifying a value is equivalent to `return None`.
# 
# ## 3. MULTIPLE RETURN VALUES (Tuple Packing)
# - Python does NOT natively support returning multiple distinct values. Instead:
#   - Writing `return a, b, c` parses as a tuple literal.
#   - Python evaluates the expressions, packs them into a single **Tuple object**, and returns that single tuple reference.
#   - Callers can use sequence unpacking: `val1, val2, val3 = get_values()`.
# 
# ## 4. CPYTHON INTERNALS & BYTECODE
# - CPython manages function frames on an execution stack:
#   1. When execution hits a return statement, it evaluates the return expression and pushes the resulting object pointer onto the frame evaluation stack.
#   2. It executes the `RETURN_VALUE` bytecode instruction.
#   3. `RETURN_VALUE` pops the top element from the current stack frame, destroys the local frame context (except for objects referenced elsewhere), and pushes the popped pointer onto the parent caller's evaluation stack.
# 
# ## 5. INTERVIEW QUESTIONS
# - **Q: Can a Python function return multiple values?**
#   - *A*: No, it returns a single object. If multiple comma-separated values are returned, Python packs them into a single `tuple` object.
# - **Q: What does a function return if there is no return statement?**
#   - *A*: It implicitly returns the singleton object `None`.
# 
# ---

# %%
import dis

# 1. Inspecting return types
def no_return():
    """No return statement."""
    pass

def bare_return():
    """Contains a bare return."""
    return

def multiple_returns(x):
    """Returns multiple values."""
    return x, x**2, x**3

print("--- Implicit and Bare Returns ---")
print(f"no_return() result:   {no_return()} | Type: {type(no_return()).__name__}")
print(f"bare_return() result: {bare_return()} | Type: {type(bare_return()).__name__}")

print("\n--- Multiple Return Values ---")
result = multiple_returns(3)
print(f"multiple_returns(3) result: {result} | Type: {type(result).__name__}")
# Expected result: (3, 9, 27) | Type: tuple

# %%
# 2. Tuple Unpacking on caller side
val1, val2, val3 = multiple_returns(5)
print("\n--- Tuple Unpacking at Call site ---")
print(f"Unpacked values: val1={val1}, val2={val2}, val3={val3}")

# %%
# 3. Disassembling Return Bytecode
def simple_return(x):
    return x * 2

print("\n--- Disassembling return statement ---")
dis.dis(simple_return)
# Expected bytecode shows:
# 1. LOAD_FAST (loads local variable x)
# 2. LOAD_CONST (loads integer 2)
# 3. BINARY_OP (multiplication)
# 4. RETURN_VALUE (pops and returns the result)
