###############################################################################
# TOPIC: Generators - yield mechanics, bidirectional Communication, and yield from
#
# 1. DEFINITION & INTRODUCTION:
#    - Generator: A special category of function that returns an iterator object
#      yielding values sequentially on-demand.
#    - Declared using the `yield` keyword instead of `return`.
#    - Generator Expression: Syntactic equivalent of list comprehension returning a lazy
#      generator object: `(expr for item in iterable)`.
#
# 2. YIELD MECHANICS & HEAP FRAME PRESERVATION:
#    - In a standard function, returning a value destroys its execution stack frame.
#    - When a generator function is called, it does not execute any code. Instead, it returns
#      a generator object wrapping the function's execution frame.
#    - When `next()` is called on the generator:
#        1. CPython resumes execution of the frame from its current instruction pointer.
#        2. Execution runs until a `yield` statement is reached.
#        3. The frame is suspended: all local variable values are frozen in memory, and the
#           yielded value is returned to the caller.
#        4. The frame remains allocated on the heap rather than being popped, preserving its entire state.
#        5. Subsequent `next()` calls resume execution immediately after the `yield` line.
#
# 3. BIDIRECTIONAL COMMUNICATION METHODS:
#    Generators are not just one-way data producers. They support three control methods:
#    - `send(value)`: Resumes the generator and sends `value` into it. The `yield` expression
#      evaluates to this value (e.g., `received = yield output`).
#      Note: The first call must be `next(g)` or `g.send(None)` to "prime" the generator.
#    - `throw(type, value=None, traceback=None)`: Raises an exception of the specified type
#      inside the generator at the current suspended `yield` line, allowing the generator to handle
#      or propagate the exception.
#    - `close()`: Raises a `GeneratorExit` exception inside the generator, causing it to run any
#      `finally` blocks and terminate.
#
# 4. YIELD FROM DELEGATION (PEP 380):
#    - Syntax: `yield from iterable`
#    - Used to delegate operations to another generator or iterable. It handles looping and
#      bidirectional communication channel setup (propagating `send()`, `throw()`, and returns)
#      automatically, replacing verbose nested loops.
#
# 5. TIME & SPACE COMPLEXITY:
#    - Space: O(1) auxiliary memory. Generates elements on-the-fly, preventing loading massive
#      datasets into RAM.
#
# 6. INTERVIEW QUESTIONS:
#    - Q: How does a generator save memory?
#      A: It evaluates elements lazily one-at-a-time, storing only the current frame execution state,
#         instead of instantiating and loading the entire dataset sequence in memory.
#    - Q: Why must you call `next()` or `send(None)` before sending values to a generator?
#      A: To "prime" the generator, running it up to its first `yield` statement so it is ready
#         to receive inputs.
#
# 7. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a co-routine generator that calculates a running average of
#      values sent to it via `send()`.
#
###############################################################################

# 1. Yield Mechanics & Lazy Iteration
def generate_squares(limit):
    print(" -> Starting generator execution...")
    for i in range(1, limit + 1):
        print(f" -> [Generator] Yielding: {i**2}")
        yield i**2  # Execution suspends here and returns value
        print(" -> [Generator] Resumed!")

print("--- Calling Generator Function ---")
# Calling the generator function only creates the object; no code runs yet.
squares_gen = generate_squares(3)
print(f"Generator Object created: {squares_gen}")

print("\n--- Evaluating Generator elements via next() ---")
print(next(squares_gen))  # Runs to first yield
print(next(squares_gen))  # Resumes, runs to second yield
print(next(squares_gen))  # Resumes, runs to third yield
try:
    next(squares_gen)  # Runs to end of function, raises StopIteration
except StopIteration:
    print("StopIteration caught cleanly.")

# 2. Bidirectional Communication (send, throw, close)
def stateful_averager():
    total = 0.0
    count = 0
    average = None
    
    print(" -> Averager initialized.")
    while True:
        # yield returns 'average' to caller, and receives 'val' from send()
        val = yield average
        if val is None:
            break  # Exit trigger
        total += val
        count += 1
        average = total / count
        print(f" -> [Averager] Updated total={total}, count={count}")

print("\n--- Bidirectional Communication (send) ---")
avg_gen = stateful_averager()

# Step A: Prime the generator (must send None or call next)
first_output = avg_gen.send(None)
print(f"Priming output: {first_output}")  # Expected: None (returned by first yield)

# Step B: Send values
print(f"Average: {avg_gen.send(10)}")  # Expected: 10.0
print(f"Average: {avg_gen.send(20)}")  # Expected: 15.0
print(f"Average: {avg_gen.send(30)}")  # Expected: 20.0

# 3. yield from Delegation
# We delegate sequence generation to nested generators.
def generator_child():
    yield "Child 1"
    yield "Child 2"
    
def generator_parent():
    yield "Parent Start"
    yield from generator_child()  # Delegates control to child
    yield "Parent End"

print("\n--- yield from Delegation ---")
for val in generator_parent():
    print(f"Value: {val}")
