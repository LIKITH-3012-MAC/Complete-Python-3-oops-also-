# %% [markdown]
# # Topic: Context Managers - Context Manager Protocol (__enter__ / __exit__), exception suppression, and contextlib
# 
# ## 1. DEFINITION & THE WITH STATEMENT
# - **Context Manager**: An object that manages setting up and tearing down resources (like files, db connections, or locks) cleanly.
# - **Syntax**:
#   ```python
#   with open("file.txt") as f:
#       # use resource
#   ```
# 
# ## 2. CONTEXT MANAGER PROTOCOL
# - A class operates as a context manager if it defines:
#   1. **`__enter__()`**:
#      - Prepares the resource (opens file, acquires lock).
#      - The return value of this method is bound to the variable following `as` in the `with` statement.
#   2. **`__exit__(exc_type, exc_val, exc_tb)`**:
#      - Executes cleanup operations.
#      - Receives parameters detailing any exception raised inside the `with` block (type, value, traceback). If execution succeeded without errors, all three arguments are `None`.
# 
# ## 3. EXCEPTION SUPPRESSION MECHANICS
# - If an exception is raised inside the `with` block, `__exit__()` is called:
#   - If `__exit__()` returns **`True`**, the exception is suppressed (swallowed), and execution continues normally after the `with` block.
#   - If it returns **`False`** or **`None`**, the exception propagates outwards to the parent scope.
# 
# ## 4. GENERATOR-BASED CONTEXT MANAGERS: contextlib
# - You can write a context manager using a single generator function decorated with **`@contextlib.contextmanager`**:
#   - Code before the `yield` statement acts as `__enter__()`.
#   - The yielded value binds to the `as` variable.
#   - Code after the `yield` statement acts as `__exit__()` (usually wrapped in a `try...finally` block).
# 
# ---

# %%
import contextlib

# 1. Class-based Context Manager with Exception Handling
class FileLogger:
    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        print(f" -> __enter__: Opening file {self.filename}")
        self.file = open(self.filename, "w")
        return self.file  # Binds to target after 'as'

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(" -> __exit__: Closing file...")
        self.file.close()
        
        if exc_type is not None:
            print(f" -> Exception detected inside with block: {exc_val}")
            # Return True to suppress ValueError exceptions
            if issubclass(exc_type, ValueError):
                print(" -> Suppressing ValueError!")
                return True
        return False  # Propagate other exceptions

print("--- Class-based Context Manager (Success Case) ---")
with FileLogger("temp_log.txt") as f:
    f.write("Log line 1\n")
    print(" -> Inside block: wrote line")

# %%
print("\n--- Class-based Context Manager (Exception Suppression) ---")
with FileLogger("temp_log.txt") as f:
    print(" -> Inside block: raising ValueError...")
    raise ValueError("Something went wrong!")
print(" -> Execution continued safely after the with block.")

# %%
# 2. Generator-based Context Manager using contextlib
@contextlib.contextmanager
def db_transaction():
    print(" -> Begin transaction (setup)")
    try:
        yield "DB_CONNECTION_OBJECT"  # Yield binding resource
        print(" -> Commit transaction (success)")
    except Exception as e:
        print(f" -> Rollback transaction (error: {e})")
        raise
    finally:
        print(" -> Clean up connection (finally)")

print("\n--- Generator-based Context Manager (Success Case) ---")
with db_transaction() as conn:
    print(f" -> Using resource: {conn}")

print("\n--- Generator-based Context Manager (Error Case) ---")
try:
    with db_transaction() as conn:
        print(" -> Raising Runtime Error...")
        raise RuntimeError("DB Crash!")
except RuntimeError:
    print(" -> RuntimeError propagated correctly.")
    
# Clean up temp file
import os
if os.path.exists("temp_log.txt"):
    os.remove("temp_log.txt")
