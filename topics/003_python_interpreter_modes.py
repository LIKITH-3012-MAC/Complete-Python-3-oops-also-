###############################################################################
# TOPIC: Python Interpreter Modes (Interactive, Script, Command Execution, Modules)
#
# 1. DEFINITION & INTRODUCTION:
#    Python can be executed in several distinct modes depending on how code is
#    delivered to the interpreter. The two primary modes are:
#    - Interactive Mode (REPL: Read-Evaluate-Print Loop): Executing `python` without
#      arguments opens an interactive shell where code lines are compiled and
#      evaluated immediately upon pressing Enter.
#      It prints the result of expressions automatically.
#    - Script Mode: Executing a saved file containing Python instructions
#      (e.g., `python script.py`).
#
# 2. ADDITIONAL INTERPRETER FLAGS & MODES:
#    CPython supports several command-line options that modify how scripts run:
#    - Command Mode (`python -c "code"`): Compiles and runs a string of Python code.
#    - Module Execution (`python -m module`): Locates a module on `sys.path` and runs
#      it as the main program (`__main__`).
#    - Interactive script mode (`python -i script.py`): Runs the specified script,
#      then leaves the user in an interactive session with all script variables alive.
#    - Optimized mode (`python -O`): Removes assert statements and sets `__debug__` to False.
#    - Unbuffered output (`python -u`): Disables stdout buffering, ensuring output is
#      flushed immediately (useful in logging or container pipelines).
#
# 3. HISTORY & MOTIVATION:
#    - Interactive mode was designed for rapid prototyping, exploration of APIs, and
#      education. It provides immediate feedback without the cycle of writing to a
#      file and executing it.
#    - Module mode (`-m`) was standardized to run library utilities cleanly without
#      having to locate their physical file paths (e.g., `python -m pip install`).
#
# 4. INTERNAL IMPLEMENTATION & CPYTHON INTERNALS:
#    - In Interactive Mode, CPython runs a specialized loop. When you type an
#      expression (e.g., `2 + 2`), CPython parses it as a single interactive statement,
#      compiles it, evaluates it, checks if the output is not `None`, and passes it
#      to `sys.displayhook` which calls `repr()` and prints it to stdout.
#    - In Script Mode, CPython compiles the entire file into a single module-level code
#      object and executes it within a single global namespace.
#
# 5. MEMORY LAYOUT & MANAGEMENT:
#    - Variables created in the interactive session remain in the interpreter's global
#      dictionary (`sys.modules['__main__'].__dict__`) until the interpreter is closed.
#    - In script execution, when the script finishes running, CPython tears down all
#      modules, cleans up namespaces, and releases memory to the OS.
#
# 6. TIME & SPACE COMPLEXITY:
#    - Interactive evaluation overhead is high per command because it compiles and runs
#      each line individually, updating the terminal repeatedly.
#    - Script mode is more efficient as compilation occurs once for the entire source unit.
#
# 7. PERFORMANCE & OPTIMIZATION:
#    - Using the `-O` (optimize) flag causes the compiler to generate slightly more compact
#      bytecode by discarding asserts and docstrings (when double `-OO` is used).
#      However, this provides negligible speedup and is rarely used today.
#
# 8. SECURITY CONSIDERATIONS:
#    - Executing external strings using `python -c` or `exec()` poses code-injection risks.
#      Never pass unsanitized user inputs to these commands.
#
# 9. BEST PRACTICES:
#    - Use `python -m` to execute system scripts (e.g., `python -m venv` or `python -m pytest`)
#      to ensure the correct Python version's standard library is targeted.
#
# 10. COMMON PITFALLS & CODE SMELLS:
#     - Relying on variables in interactive mode to persist between restarts.
#     - Forgetting that standard output buffering (especially on non-tty devices)
#       might delay console output in containers unless `-u` or `PYTHONUNBUFFERED=1` is set.
#
# 11. INTERVIEW QUESTIONS:
#     - Q: What does `python -m` do?
#       A: It executes a module from the import path (`sys.path`) as the `__main__` entrypoint.
#     - Q: How can you drop into an interactive shell after a script crashes?
#       A: Run it using the interactive inspect flag: `python -i script.py`.
#
# 12. EXERCISES & SOLUTIONS:
#     - Coding challenge: Write a Python program that inspects its execution arguments
#       passed through the CLI and prints how many arguments were supplied.
#
###############################################################################

import sys  # standard library module for interaction with interpreter environment

# 1. Inspect sys.argv (Argument List)
# sys.argv is a list of strings containing the command-line arguments passed to the script.
# The first element, sys.argv[0], is the script path. Subsequent elements are user inputs.
print("--- CLI Command Arguments ---")
arguments_received = sys.argv
print(f"Number of arguments: {len(arguments_received)}")
print(f"Arguments list: {arguments_received}")

# 2. Emulate sys.displayhook (how Interactive mode prints expressions automatically)
# In interactive mode, simple calculations like:
# >>> 10 + 20
# print 30 automatically. We can simulate how Python decides to print this.
def custom_displayhook(value):
    # Interactive mode checks if the evaluated value is None.
    # If not None, it binds the special variable '_' (underscore) to the result and prints it.
    if value is not None:
        # set the special variable in builtins module (interactive console uses it)
        import builtins
        builtins._ = value
        print(repr(value))  # Print using repr representation

# Test displaying expressions using our custom hook
print("\n--- Displaying evaluated expression ---")
custom_displayhook(100 + 200)  # Prints 300
print(f"Value bound to underscore (_): {_}")  # Special variable containing last output

# 3. Detect Optimizations
# If Python is run with '-O', the __debug__ flag is set to False.
# This variable is a built-in constant and cannot be modified at runtime.
print(f"\nIs interpreter running in optimization mode? {not __debug__}")
if __debug__:
    print("Assertions are ACTIVE. Running with default mode.")
else:
    print("Assertions are INACTIVE. Running with -O optimize flag.")

# Demonstrating an assertion (this will fail in normal execution, but be ignored under 'python -O')
try:
    assert False, "This is an assertion failure test!"
except AssertionError as e:
    print(f"Caught expected AssertionError: {e}")
