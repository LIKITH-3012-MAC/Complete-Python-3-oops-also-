###############################################################################
# TOPIC: sys.path search Order and __name__ == "__main__" Entrypoints
#
# 1. DEFINITION & INTRODUCTION:
#    - `sys.path`: A list of directory paths representing the search path for modules.
#      When you import a module, Python looks through this list sequentially.
#    - `__name__`: A special built-in string variable automatically set by CPython on
#      every module.
#    - `"__main__"`: The value bound to `__name__` if the module is executed directly as
#      the entry point script.
#
# 2. SYS.PATH INITIALIZATION & ORDER:
#    At startup, Python initializes `sys.path` in the following priority order:
#    1. The directory containing the input script (or the current directory if run interactively).
#    2. `PYTHONPATH` environment variable directory list (if set).
#    3. Standard Library directories (built-in libraries).
#    4. Third-party packages installed in the site-packages directory (managed by pip).
#    Modifying `sys.path` (e.g. `sys.path.append()`) allows importing modules from custom locations.
#
# 3. UNDERSTANDING `__name__ == "__main__"` Idiom:
#    - When you run a script directly (e.g., `python script.py`), CPython sets that script's
#      global `__name__` variable to `"__main__"`.
#    - If that same script is imported by another module (e.g., `import script`), CPython sets
#      `__name__` to the actual filename (e.g. `"script"`).
#    - Therefore, the block `if __name__ == "__main__":` ensures that code (like unit tests,
#      demonstrations, or execution setups) inside it executes **ONLY when the file is run directly**,
#      preventing it from running when imported as a library dependency.
#
# 4. BEST PRACTICES:
#    - Always wrap script execution code (CLIs, configurations) inside the `if __name__ == "__main__":`
#      guard to allow the file to be safely imported elsewhere without triggering execution side-effects.
#    - Avoid modifying `sys.path` manually inside production code. Configure environment paths or
#      install packages in development/editable mode instead.
#
# 5. INTERVIEW QUESTIONS:
#    - Q: What does `sys.path` contain and what is the lookup order?
#      A: It is a list of strings containing directories searched during imports. Lookup order:
#         current directory, PYTHONPATH environment paths, standard library, and site-packages.
#    - Q: What value does `__name__` take when a module is imported?
#      A: It takes the string name of the module file (excluding the `.py` extension).
#
# 6. EXERCISES & SOLUTIONS:
#    - Coding challenge: Write a Python program that prints its own module name (`__name__`)
#      and displays the directory search paths in `sys.path` in a clean, numbered list format.
#
###############################################################################

import sys  # Standard library to read path details and module parameters

# 1. Print current module name
print(f"Current module name (__name__): '{__name__}'")

# 2. Check sys.path search order
# We will iterate and display search directories in order of lookup priority.
print("\n--- Module Search Path (sys.path) ---")
for index, path_dir in enumerate(sys.path):
    # Print index and folder path
    print(f"  [{index}] Path: {repr(path_dir)}")

# 3. Demonstrate safe entry point behavior
def run_application_logic():
    print(" -> Executing application main workflow logic.")

# The entrypoint guard
if __name__ == "__main__":
    # This block executes because this script is run as the main thread entrypoint.
    print("\n[Guard Entrypoint] Running because file is executed directly.")
    run_application_logic()
else:
    # This would execute if we imported this file in another script.
    print("\n[Guard Entrypoint] running because file was imported.")
