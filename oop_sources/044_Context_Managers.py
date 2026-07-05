###############################################################################
# TOPIC: Context Managers - Resource safety, the with statement, and leak preventions
#
# 1. DEFINITION & INTRODUCTION:
#    - Context Managers: Objects that wrap a execution block inside a `with` statement,
#      coordinating the safe acquisition and release of system resources.
#    - Motivation: Resource Leaks. System resources (file descriptors, network sockets, DB
#      connections, locks) are limited. If a program opens a file but crashes before closing it,
#      the descriptor remains locked in the OS table.
#    - The `with` statement guarantees cleanup operations execute, even if the code block inside
#      the `with` raises an exception, crashes, or returns early.
#
# 2. RUNTIME EXECUTION SEQUENCE:
#    - When `with ContextManager() as resource:` executes:
#        1. The context manager object is instantiated.
#        2. The manager's `__enter__()` method is called. Its return value is bound to the
#           `resource` variable.
#        3. The code block inside the `with` suite is executed.
#        4. When the suite exits (normally or via an exception), the manager's `__exit__()`
#           method is called.
#
# 3. COMBINING CONTEXT MANAGERS:
#    - Python supports nesting multiple context managers in a single `with` statement:
#      `with open("a.txt") as f1, open("b.txt") as f2:`
#      They are entered from left to right and exited in reverse order (right to left, stack-like).
#
# 4. BEST PRACTICES:
#    - Always manage OS resources (files, locks, sockets) using `with` blocks to prevent leaks.
#
# 5. INTERVIEW QUESTIONS:
#    - Q: Why is the `with` statement preferred over standard `try-finally` blocks?
#      A: The `with` statement is cleaner, more readable, reduces boilerplate, and encapsulates
#         the setup/teardown logic within the resource class itself rather than scattering it in
#         caller space.
#    - Q: What happens to a file opened inside a function with `with` if the function raises an exception?
#      A: The context manager's exit hook runs automatically as the stack unwinds, closing the file
#         before propagating the exception.
#
# 6. EXERCISES & SOLUTIONS:
#    - Coding challenge: Write a script demonstrating standard file I/O operations inside nested
#      `with` blocks, catching exceptions to prove resource cleanup occurred.
#
###############################################################################

import os  # Standard library to manage file paths

temp_file = "sandbox_temp.txt"

print("--- Standard with block File I/O ---")
# Open automatically closes the file on block exit
with open(temp_file, "w", encoding="utf-8") as f:
    f.write("Safe resource management.")

# Verify file is closed
print(f"Is file closed outside with block? {f.closed}")  # Expected: True

# 2. Handling Exceptions inside with block
print("\n--- Exception Propagation in Contexts ---")
try:
    with open(temp_file, "r") as f:
        print("Reading file inside with...")
        # Force a failure
        x = 1 / 0
except ZeroDivisionError as e:
    print(f"Caught ZeroDivisionError outside with block: {e}")
    # Verify the file descriptor was STILL closed safely
    print(f"Is file closed after crash? {f.closed}")  # Expected: True

# 3. Nested Context Managers
print("\n--- Nested Context Managers ---")
dest_file = "sandbox_dest_temp.txt"

# Open two files concurrently. Entered left-to-right, exited right-to-left.
with open(temp_file, "r") as src, open(dest_file, "w") as dest:
    content = src.read()
    dest.write(content.upper())
    print("Files copied and transformed successfully.")

# Clean up
if os.path.exists(temp_file):
    os.remove(temp_file)
if os.path.exists(dest_file):
    os.remove(dest_file)
print("Temporary files cleaned up.")
