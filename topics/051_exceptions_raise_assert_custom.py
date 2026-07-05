###############################################################################
# TOPIC: Raising Exceptions, Chaining (from), Assertions, and Custom Exceptions
#
# 1. DEFINITION & INTRODUCTION:
#    - Raising Exceptions: Executed programmatically using the `raise` keyword.
#    - Exception Chaining (PEP 344): Allows linking an exception to another exception
#      to trace root causes, configuring `__context__` and `__cause__` attributes.
#    - Assertions: Debugging aids evaluating a boolean condition. If False, raises `AssertionError`.
#    - Custom Exceptions: User-defined classes that inherit from `Exception`.
#
# 2. EXCEPTION CHAINING MECHANICS (from):
#    - Explicit Chaining: `raise NewException(...) from original_exception`.
#      The traceback displays both exceptions, showing "The above exception was the direct
#      cause of the following exception:".
#    - Disabling Chaining: `raise NewException(...) from None`.
#      Clears the original traceback reference, displaying only the new exception. Used when
#      exposing errors to clients to hide internal code details.
#
# 3. ASSERTION RULES & COMPILER BEHAVIOR:
#    - Syntax: `assert condition, error_message`
#    - Compilation flag: Assertions are designed for development checks. Running Python with the
#      optimization flag `-O` tells the compiler to discard all assert bytecodes.
#    - WARNING: Never use assertions to perform production validations (like verifying user input,
#      database bounds, API validation), as this logic is completely skipped in production.
#
# 4. CUSTOM EXCEPTIONS BEST PRACTICES:
#    - Always subclass `Exception` (or a more specific child like `ValueError` / `LookupError`),
#      never subclass `BaseException` directly.
#    - End the class name with the suffix `Error` (e.g. `DatabaseConnectionError`).
#    - Implement standard methods (`__init__`, `__str__` or `__repr__`) to accept and log metadata.
#
# 5. INTERVIEW QUESTIONS:
#    - Q: What does `raise Exception from None` do?
#      A: It raises a new exception while suppressing the traceback context of any previous
#         active exception, displaying only the new error.
#    - Q: Why should you not use `assert` for user input validation?
#      A: Because assertions are disabled at compile-time when Python is run with optimization
#         flags (like `python -O script.py`), bypassing input validation checks.
#
# 6. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a custom exception class `ValidationException` containing a
#      dictionary of validation error details, raise it under custom validation, and trace it.
#
###############################################################################

# 1. Exception Chaining (Explicit and Suppression)
def calculate_inverse(number):
    try:
        return 1.0 / number
    except ZeroDivisionError as e:
        # Explicit chaining: links ZeroDivisionError to ValueError
        raise ValueError("Invalid number input: division by zero!") from e

def calculate_inverse_silent(number):
    try:
        return 1.0 / number
    except ZeroDivisionError as e:
        # Suppressing chaining: hides ZeroDivisionError from traceback
        raise ValueError("Calculations failed!") from None

print("--- Exception Chaining (Explicit) ---")
try:
    calculate_inverse(0)
except ValueError as e:
    print(f"Caught ValueError: {e}")
    # Inspecting chain details
    print(f"Original Cause (__cause__): {e.__cause__}")  # Expected: ZeroDivisionError

print("\n--- Exception Chaining (Suppressed) ---")
try:
    calculate_inverse_silent(0)
except ValueError as e:
    print(f"Caught ValueError: {e}")
    print(f"Original Cause (__cause__): {e.__cause__}")  # Expected: None (Suppressed!)

# 2. Custom Exception Hierarchies
class ApplicationError(Exception):
    """Base exception for this application."""
    pass

class DatabaseValidationError(ApplicationError):
    """Raised when database parameters fail validations."""
    def __init__(self, table, field, message):
        # Pass a formatted string to base Exception class constructor
        super().__init__(f"Table '{table}' | Field '{field}': {message}")
        self.table = table
        self.field = field

print("\n--- Raising Custom Exception ---")
try:
    raise DatabaseValidationError("users", "email", "Missing '@' symbol")
except DatabaseValidationError as e:
    print(f"Caught database error: {e}")
    print(f"Table attribute: {e.table} | Field: {e.field}")
    # Verify inheritance relationship
    print(f"Is ApplicationError parent? {isinstance(e, ApplicationError)}")  # Expected: True

# 3. Assertions and Optimization flag check
def check_positive_value(x):
    # If x <= 0, raises AssertionError
    assert x > 0, f"Value must be positive, received: {x}"
    return x * 10

print("\n--- Assertions ---")
print(f"Check 5: {check_positive_value(5)}")
try:
    check_positive_value(-10)
except AssertionError as e:
    print(f"Caught expected AssertionError: {e}")
