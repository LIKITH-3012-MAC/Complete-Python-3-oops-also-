###############################################################################
# TOPIC: Exception Handling, try-except-else-finally, and Exception Groups (3.11)
#
# 1. DEFINITION & INTRODUCTION:
#    - Exceptions: Objects representing errors or anomalous conditions detected during execution,
#      interrupting standard control flow.
#    - Python keywords: `try`, `except`, `else`, `finally`.
#
# 2. PYTHON EXCEPTION HIERARCHY:
#    - All built-in exceptions inherit from `BaseException`.
#    - Root Categories:
#        - `BaseException`: Not intended to be caught directly. Parent of control signals
#          like `SystemExit`, `KeyboardInterrupt`, `GeneratorExit`.
#        - `Exception`: Parent class for all user-level, non-system-exiting errors.
#          Custom exceptions must subclass `Exception`.
#        - `ArithmeticError`: Base class for mathematical errors like `ZeroDivisionError`, `OverflowError`.
#        - `LookupError`: Base class for search lookup errors like `IndexError`, `KeyError`.
#
# 3. TRY-EXCEPT-ELSE-FINALLY EXECUTION RULES:
#    - `try`: Code block monitored for exceptions.
#    - `except`: Catches and handles matching exception classes.
#    - `else`: Runs **ONLY if no exceptions occurred** inside the `try` block.
#    - `finally`: Runs **unconditionally** after all other blocks (regardless of whether exceptions
#      occurred, were caught, or were raised).
#    - Return Override Trap: If a `return` statement is executed inside `try` or `except` AND a
#      `return` statement is also present inside `finally`, the value in `finally` takes precedence,
#      overwriting the original return value!
#
# 4. EXCEPTION GROUPS AND except* (Python 3.11 - PEP 654):
#    - Introduced in Python 3.11 to support raising and handling multiple independent exceptions
#      simultaneously. Highly useful in concurrent systems (like asyncio task groups).
#    - `ExceptionGroup(message, [exceptions])`: Exception container class.
#    - `except* ExceptionType:`: Syntax that intercepts matching individual exceptions inside
#      the group, allowing processing of multiple exception types in separate blocks.
#
# 5. BEST PRACTICES:
#    - Never catch `BaseException` or write empty `except:` clauses; always catch specific
#      exceptions (e.g. `except ValueError:`) to avoid silencing system exit codes.
#
# 6. INTERVIEW QUESTIONS:
#    - Q: What happens if both `try` and `finally` blocks return a value?
#      A: The `finally` block's return statement overrides the `try` block's return statement;
#         the value returned by `finally` is what the caller receives.
#    - Q: What is the purpose of the `else` block in exception handling?
#      A: It runs code that should execute only if the `try` block completes successfully
#         without raising any exceptions, separating test-monitored code from success-handling code.
#
# 7. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a function demonstrating try-except-else-finally return values
#      and execute an ExceptionGroup handling demonstration.
#
###############################################################################

# 1. Try-Except-Else-Finally Execution Sequence
def divide_numbers(a, b):
    print(f"\nRunning divide_numbers({a}, {b}):")
    try:
        result = a / b
    except ZeroDivisionError as e:
        print(f" -> [except] Caught zero division: {e}")
        return "division_error"
    else:
        # Executes only if no exception occurred in try
        print(" -> [else] Division successful!")
        return result
    finally:
        # Executes unconditionally
        print(" -> [finally] Cleanup block executed.")

print("--- try-except-else-finally Flow ---")
print(f"Result A: {divide_numbers(10, 2)}")
print(f"Result B: {divide_numbers(10, 0)}")

# 2. Finally Return Precedence Trap
def return_precedence_trap():
    try:
        print("\n -> [try] Running block...")
        return "val_from_try"
    finally:
        print(" -> [finally] Running block...")
        # This return statement overrides the return in the try block!
        return "val_from_finally"

print(f"Returned value from trap: '{return_precedence_trap()}'")  # Expected: 'val_from_finally'

# 3. Exception Groups (Python 3.11+ - PEP 654)
# Demonstrates raising and catching multiple exceptions concurrently.
def exception_group_demo():
    print("\n--- Exception Groups Demo ---")
    try:
        # Create a group containing a ValueError and a TypeError
        raise ExceptionGroup(
            "Multiple background failures occurred",
            [
                ValueError("Invalid user entry"),
                TypeError("Unsupported parameter type"),
                ValueError("Database constraint violated")
            ]
        )
    except* ValueError as eg:
        # Handles all ValueError instances from the group
        print(" -> [except* ValueError] Handling ValueError items:")
        for err in eg.exceptions:
            print(f"    - Caught ValueError: {err}")
    except* TypeError as eg:
        # Handles all TypeError instances from the group
        print(" -> [except* TypeError] Handling TypeError items:")
        for err in eg.exceptions:
            print(f"    - Caught TypeError: {err}")

exception_group_demo()
