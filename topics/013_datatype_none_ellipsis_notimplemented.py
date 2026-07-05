###############################################################################
# TOPIC: Core Data Types - Special constants (None, Ellipsis, NotImplemented)
#
# 1. DEFINITION & INTRODUCTION:
#    Python has three special constant singletons with unique, dedicated classes:
#    - `None`: Represents the absence of a value or a null/default state.
#      Its type is `NoneType`.
#    - `NotImplemented`: A special value returned by binary magic methods (like `__eq__`,
#      `__add__`) to indicate that an operation is not supported for the given operand
#      types, prompting Python to try the reflected operation or fall back.
#      Its type is `NotImplementedType`.
#    - `Ellipsis`: Represented by the literal `...` (three dots) or the identifier `Ellipsis`.
#      Used primarily in extended slicing (e.g. NumPy arrays), type hints, or as a stub.
#      Its type is `ellipsis`.
#
# 2. SINGLETON NATURE (CPython Internals):
#    - Each of these constants is a singleton. Only one instance of their respective types
#      exists in the interpreter.
#    - Thus, identity comparison (`is`) should always be used to check for them.
#
# 3. NOTIMPLEMENTED VS NOTIMPLEMENTEDERROR (Critical Interview Trap):
#    - `NotImplemented` is a value returned by a method (e.g., `return NotImplemented`).
#      It is NOT an exception. Returning it tells the interpreter: "I don't know how to
#      interact with this type; ask the other operand if it knows how."
#    - `NotImplementedError` is a subclass of `RuntimeError` that is raised (using `raise`)
#      to indicate that an abstract method or subclass stub has not been implemented yet.
#
# 4. ELLIPSIS APPLICATIONS:
#    - Slicing: In multi-dimensional datasets (like NumPy arrays), `...` stands for "all
#      dimensions not explicitly specified". E.g., `matrix[..., 0]` fetches the first column
#      across all nested dimensions.
#    - Type hints: Used in `Callable[..., int]` to specify a function that takes any arguments
#      and returns an integer, or in `Tuple[int, ...]` to represent an arbitrary-length tuple
#      of integers.
#
# 5. MEMORY FOOTPRINT:
#    - Being singletons, creating multiple references to `None`, `...`, or `NotImplemented`
#      incurs no additional memory allocation; they all point to the same memory addresses
#      created at CPython interpreter startup.
#
# 6. BEST PRACTICES:
#    - Use `is None` or `is not None` for checking null arguments. Do not use `== None`.
#    - Return `NotImplemented` when writing custom mathematical or comparison magic methods
#      to allow proper fallback cooperation between class types.
#
# 7. INTERVIEW QUESTIONS:
#    - Q: What happens if a magic method (e.g. `__eq__`) returns `NotImplemented`?
#      A: CPython catches the return value, reverses the operands, and attempts to call
#         the reflected magic method (e.g. `__req__`) on the other object. If that also
#         fails or returns `NotImplemented`, it falls back to basic comparison or raises a TypeError.
#    - Q: Is `NotImplemented` the same as `NotImplementedError`?
#      A: No, `NotImplemented` is a singleton value returned to guide operator dispatch;
#         `NotImplementedError` is an exception class raised to signal unwritten code.
#
# 8. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a custom class where a comparison returns `NotImplemented`
#      and show how Python automatically delegates to the reflected operator of the target class.
#
###############################################################################

import sys  # Standard library to check object identity and classes

# 1. Inspection of Types
print("--- Special Singletons & Classes ---")
print(f"None Value: {None} | Type: {type(None)}")  # Expected: NoneType
print(f"Ellipsis Value: {...} | Type: {type(...)}")  # Expected: ellipsis
print(f"NotImplemented Value: {NotImplemented} | Type: {type(NotImplemented)}")  # Expected: NotImplementedType

# 2. Singleton Identity Check
# Because they are singletons, identity comparison is fast and safe.
val1 = None
val2 = None
print(f"\nNone identity check (val1 is val2): {val1 is val2}")  # Expected: True

e1 = ...
e2 = Ellipsis
print(f"Ellipsis identity check (e1 is e2): {e1 is e2}")  # Expected: True

# 3. NotImplemented Operator Cooperative Fallback
class CustomInt:
    def __init__(self, val):
        self.val = val
        
    def __add__(self, other):
        # We only know how to add if other is also a CustomInt or standard int.
        if not isinstance(other, (CustomInt, int)):
            # Returning NotImplemented instructs Python to query the right-hand operand (other)
            return NotImplemented
        other_val = other.val if isinstance(other, CustomInt) else other
        return CustomInt(self.val + other_val)
        
    def __radd__(self, other):
        # Reflected add (called when left-hand operand returned NotImplemented)
        print(" -> CustomInt.__radd__ called as fallback!")
        return self.__add__(other)

class UnrelatedClass:
    def __init__(self, val):
        self.val = val

# Test cooperation
ci = CustomInt(10)
unrelated = UnrelatedClass(5)

# Adding CustomInt and standard int (works natively)
result_1 = ci + 5
print(f"\nCooperative Add (ci + 5): {result_1.val}")

# Adding standard int and CustomInt (calls __radd__ fallback)
# Python first tries int.__add__(ci), which fails/returns NotImplemented,
# then falls back to CustomInt.__radd__(ci, 5).
result_2 = 5 + ci
print(f"Cooperative Add (5 + ci): {result_2.val}")

# 4. NotImplementedError vs NotImplemented distinction
print("\n--- Exception vs Value comparison ---")
print(f"Is NotImplemented an exception? {isinstance(NotImplemented, Exception)}")  # Expected: False
print(f"Is NotImplementedError an exception? {issubclass(NotImplementedError, Exception)}")  # Expected: True

# 5. Ellipsis Type Hinting Simulation
from typing import Tuple, Callable

# Example type annotations using Ellipsis
def process_data(data: Tuple[int, ...]) -> int:
    # Tuple[int, ...] denotes a tuple of arbitrary length containing only integers.
    return sum(data)

def execute_callback(cb: Callable[..., int]) -> int:
    # Callable[..., int] denotes a function that takes any arguments and returns an int.
    return cb()

print(f"\nFunction annotations for Ellipsis: {process_data.__annotations__}")
