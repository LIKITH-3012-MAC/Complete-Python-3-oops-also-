###############################################################################
# TOPIC: Generator Context Managers - @contextmanager, yield try-finally, and ExitStack
#
# 1. DEFINITION & INTRODUCTION:
#    - Generator-Based Context Managers: Created by decorating a generator function with the
#      `@contextlib.contextmanager` decorator.
#    - Flow mapping:
#        - Statements before `yield`: Behave as `__enter__()`.
#        - The `yield` value: Binds to the variable in the `as` clause.
#        - Statements after `yield`: Behave as `__exit__()`.
#
# 2. EXCEPTION HANDLING REQUIREMENT:
#    - If an exception occurs inside the `with` block, Python throws that exception back
#      into the generator at the `yield` statement line.
#    - If the generator does not wrap the `yield` statement in a `try-except-finally` block:
#        1. The exception propagates out of the generator immediately.
#        2. The teardown/cleanup code placed after the `yield` is completely skipped!
#    - Therefore, you must always wrap the `yield` inside a `try-finally` (or `try-except-finally`)
#      block to guarantee that cleanup executes despite crashes.
#
# 3. ADVANCED CONTEXTLIB UTILITIES:
#    - `contextlib.closing(thing)`: Wraps objects lacking a context manager interface but having a
#      `.close()` method, calling `.close()` automatically on exit.
#    - `contextlib.ExitStack`: A context manager that lets you combine other context managers
#      dynamically at runtime, exiting all registered resources in reverse order on block teardown.
#      Highly useful when the number of resources to open is variable or only known at runtime.
#
# 4. INTERVIEW QUESTIONS:
#    - Q: What happens in a generator-based context manager if an exception is raised inside the
#         `with` block and there is no `try-finally` block?
#      A: The exception is thrown at the `yield` point, halting the generator immediately, and
#         skipping the remaining cleanup code.
#    - Q: When is `contextlib.ExitStack` used?
#      A: When you need to manage a dynamic number of context managers (e.g., opening a variable list
#         of files) whose count or file paths are determined at runtime.
#
# 5. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a generator-based context manager that mocks database connection setups,
#      wrapped in try-finally, and demonstrate how it handles exception propagation.
#
###############################################################################

import contextlib  # Standard context manager utility module
import sys  # Standard library to print diagnostic traces

# 1. Generator-Based Context Manager with try-except-finally wrapper
@contextlib.contextmanager
def db_session_manager(db_name):
    # Setup step (before yield)
    print(f" -> [Generator Setup] Opening connection to database: {db_name}")
    connection_active = True
    try:
        # Yield the active connection resource to the with block
        yield f"active_connection_to_{db_name}"
        # If execution resumes here, the with block completed successfully
        print(" -> [Generator Teardown] Committing transaction changes.")
    except Exception as e:
        # If an error occurred inside the with block, it is thrown here
        print(f" -> [Generator Teardown] Error intercepted: {e}. Rolling back changes!")
        # We must re-raise the exception if we don't want to swallow it
        raise e
    finally:
        # Teardown step: always executes, guaranteeing resource cleanup
        print(f" -> [Generator Teardown] Closing connection: {db_name}")
        connection_active = False

print("--- Case A: Normal Asynchronous Execution ---")
with db_session_manager("SalesDB") as conn:
    print(f"  Inside with: Using resource: {conn}")

print("\n--- Case B: Failed Execution (Exception thrown back into generator) ---")
try:
    with db_session_manager("InventoryDB") as conn:
        print("  Performing database query...")
        # Force a crash inside the with block
        raise RuntimeError("Network Timeout")
except RuntimeError as e:
    print(f"Caught error outside with block: {e}")

# 2. Dynamic Resource Management using ExitStack
# Open a dynamic list of files concurrently.
print("\n--- Dynamic Context Management via ExitStack ---")
filenames = ["file_alpha.txt", "file_beta.txt", "file_gamma.txt"]

# We will write temp files to test the stack
for fname in filenames:
    with open(fname, "w") as f:
        f.write(f"Data inside {fname}")

# Use ExitStack to open all files concurrently
with contextlib.ExitStack() as stack:
    # Dynamically enter file context managers and save references
    file_objects = [stack.enter_context(open(name, "r")) for name in filenames]
    
    print(f"Opened {len(file_objects)} files concurrently:")
    for f in file_objects:
        print(f"  Content of {f.name}: '{f.read()}'")

# ExitStack block completes: all files are automatically closed!
# Clean up workspace
for fname in filenames:
    import os
    if os.path.exists(fname):
        os.remove(fname)
print("All files closed and cleaned up safely.")
