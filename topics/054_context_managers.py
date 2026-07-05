###############################################################################
# TOPIC: Context Managers, contextlib generator, and Exception Suppression
#
# 1. DEFINITION & INTRODUCTION:
#    - Context Managers: Objects that coordinate resource allocation and release
#      via the `with` statement.
#    - Common use cases: File descriptor locks, database transaction commits/rollbacks,
#      thread synchronization, and directory changes.
#
# 2. CLASS-BASED CONTEXT MANAGERS:
#    To act as a context manager, a class must implement two magic methods:
#    - `__enter__(self)`: Runs when entering the `with` block. Returns the resource (bound
#      to the variable defined in `as variable`).
#    - `__exit__(self, exc_type, exc_val, exc_tb)`: Runs when exiting the `with` block
#      (regardless of whether an exception occurred).
#        - `exc_type`: The class type of the raised exception (if any).
#        - `exc_val`: The raised exception object instance.
#        - `exc_tb`: The traceback object.
#        - Exception Suppression Rule: If `__exit__()` returns `True`, Python intercepts and
#          suppresses the exception, resuming execution on the line after the `with` block.
#          If it returns `False` or `None`, the exception is propagated normally.
#
# 3. GENERATOR-BASED CONTEXT MANAGERS (@contextlib.contextmanager):
#    - Instead of writing a full class, you can write a generator decorated with
#      `@contextlib.contextmanager`.
#    - Inside the generator:
#        - The code before the `yield` statement is equivalent to `__enter__()`.
#        - The `yield` expression returns the resource.
#        - The code after the `yield` represents `__exit__()`.
#        - Warning: To handle exceptions raised inside the `with` block, you MUST wrap the
#          `yield` statement in a `try-except-finally` block. Otherwise, exceptions propagate
#          outwards immediately, and the teardown code after `yield` is never executed!
#
# 4. TIME COMPLEXITY:
#    - Context manager resource setups and teardowns are O(1) operations.
#
# 5. INTERVIEW QUESTIONS:
#    - Q: How can you suppress exceptions raised inside a `with` block?
#      A: By returning `True` from the context manager's `__exit__()` method.
#    - Q: What happens in a generator-based context manager if an exception is raised inside the
#         `with` block, and the `yield` is not wrapped in `try-finally`?
#      A: The exception is thrown back into the generator at the `yield` point. If not caught,
#         it halts the generator immediately, meaning any cleanup code placed after the `yield`
#         statement is skipped, potentially leaking resources.
#
# 6. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a context manager that redirects stdout to a string buffer
#      inside the `with` block and restores it on exit.
#
###############################################################################

import sys  # Standard library to manipulate streams
import contextlib  # Standard library containing context manager decorators
import io  # Stream buffer utilities

# 1. Class-Based Context Manager with Exception Suppression option
class DatabaseTransaction:
    def __init__(self, should_suppress_errors):
        self.should_suppress = should_suppress_errors
        
    def __enter__(self):
        print(" -> [Transaction] Starting database transaction...")
        return self  # Returned object bound to 'as' variable
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            # An error occurred inside the with block
            print(f" -> [Transaction] Exception detected: {exc_val}")
            print(" -> [Transaction] Rolling back transaction state changes!")
            # If we return True, the error is caught and suppressed.
            return self.should_suppress
        else:
            print(" -> [Transaction] Committing transaction changes successfully.")
            return True

print("--- Case A: Successful Transaction (no exceptions) ---")
with DatabaseTransaction(should_suppress_errors=False) as db:
    print("  Executing database query 1...")
    print("  Executing database query 2...")

print("\n--- Case B: Failed Transaction with Exception Propagation ---")
try:
    with DatabaseTransaction(should_suppress_errors=False) as db:
        print("  Executing query before crash...")
        raise ValueError("Database constraint violated!")
except ValueError as e:
    print(f"Caught propagated exception: {e}")

print("\n--- Case C: Failed Transaction with Exception Suppression ---")
# When should_suppress_errors=True, the ValueError is caught in __exit__ and suppressed
with DatabaseTransaction(should_suppress_errors=True) as db:
    print("  Executing query before crash...")
    raise ValueError("Database unique constraint violation (Suppressed)!")
print("Execution continues normally after suppressed with block.")

# 2. Generator-Based Context Manager using contextlib
# We write a custom stdout redirector context manager.
@contextlib.contextmanager
def redirect_stdout_buffer():
    # Setup step (equivalent to __enter__)
    original_stdout = sys.stdout
    buffer_stream = io.StringIO()
    sys.stdout = buffer_stream
    print(" -> Context started: redirecting stdout to buffer.")
    
    try:
        # Yield the resource to the with block
        yield buffer_stream
    except Exception as e:
        # Intercept and print errors to standard error stream
        sys.stderr.write(f"Error captured in redirector generator: {e}\n")
        raise e
    finally:
        # Teardown step (equivalent to __exit__)
        # This executes unconditionally, ensuring stdout is restored!
        sys.stdout = original_stdout
        print(" -> Context finished: stdout stream restored.")

print("\n--- Generator-Based Context Manager (Redirector) ---")
with redirect_stdout_buffer() as buf:
    print("This line will not print to the console.")
    print("It is captured in the string buffer stream.")
    
# Retrieve captured output from the stream
captured_string = buf.getvalue()
print(f"Captured output: {repr(captured_string)}")
