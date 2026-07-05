# %% [markdown]
# # Topic: Yield - Two-way send communication, generator priming, and yield from delegation
# 
# ## 1. TWO-WAY COMMUNICATION: send()
# - The `yield` statement is not just an output channel; it acts as a two-way communication bridge:
#   `received_value = yield output_value`
# - **Mechanics**:
#   - Calling `generator.send(value)` resumes execution, pushes `value` back into the generator, and assigns it as the evaluation result of the current suspended `yield` expression.
# - **Priming Rule**: You cannot send a non-`None` value to a newly created generator. You must first "prime" it by executing `next(generator)` or `generator.send(None)` to advance it to its first `yield` expression.
# 
# ## 2. SUBGENERATOR DELEGATION: yield from
# - Introduced in PEP 380 (Python 3.3).
# - **`yield from subgenerator`**:
#   - Delegates the iteration process directly to an inner subgenerator or iterable.
#   - Automatically handles sending values back and forth and raising exceptions (`StopIteration`, `throw()`) directly between the caller and the subgenerator, eliminating complex boilerplate loops.
# 
# ## 3. GENERATOR CONTROL METHODS
# - **`generator.throw(exception_type)`**: Raises an exception inside the generator at the point where it is currently suspended.
# - **`generator.close()`**: Raises a `GeneratorExit` exception inside the generator, forcing it to close and terminate immediately.
# 
# ## 4. INTERVIEW QUESTIONS
# - **Q: What is the purpose of `yield from` in Python?**
#   - *A*: It delegates generator execution to a subgenerator or iterable, creating a direct bidirectional channel between the caller and the subgenerator for values and exceptions.
# - **Q: Why must you prime a generator before calling `send()`?**
#   - *A*: Because a new generator is not suspended at a `yield` expression yet. Calling `next()` or `send(None)` executes code up to the first `yield` statement where it can receive values.
# 
# ---

# %%
# 1. Two-way communication using send()
def interactive_echo():
    """Receives and echoes inputs."""
    print(" -> echo started")
    value = None
    while True:
        # Yield 'value' to caller, suspend, and wait for next send() input
        received = yield value
        print(f" -> Generator received: {received}")
        value = f"Echo: {received}"

print("--- Interactive Generator (send) ---")
echo = interactive_echo()

# Priming the generator (advancing to first yield)
prime_val = echo.send(None)
print(f"Priming returned: {prime_val}")  # Expected: None

# Send active values
response1 = echo.send("Hello")
print(f"Send 1 returned: {response1}")  # Expected: "Echo: Hello"

response2 = echo.send("Python")
print(f"Send 2 returned: {response2}")  # Expected: "Echo: Python"

# %%
# 2. Generator delegation using yield from
def sub_sequence(start, end):
    for i in range(start, end):
        yield i

def main_sequence():
    yield "Start"
    # Delegate to subgenerator
    yield from sub_sequence(1, 4)
    yield "End"

print("\n--- Subgenerator Delegation (yield from) ---")
for val in main_sequence():
    print(val)
# Expected sequence: 'Start', 1, 2, 3, 'End'

# %%
# 3. Generator control: close() and throw()
def control_demo():
    try:
        yield "Step 1"
        yield "Step 2"
    except ValueError:
        print(" -> Caught ValueError inside generator!")
        yield "Recovered Step"
    finally:
        print(" -> Generator cleaning up resources...")

print("\n--- Testing Generator throw() ---")
gen = control_demo()
print(next(gen))
# Throw ValueError inside generator
print(gen.throw(ValueError))  # Expected: prints Caught ValueError and returns "Recovered Step"

print("\n--- Testing Generator close() ---")
gen2 = control_demo()
print(next(gen2))
# Terminate generator execution immediately
gen2.close()  # Expected: prints Generator cleaning up resources...
