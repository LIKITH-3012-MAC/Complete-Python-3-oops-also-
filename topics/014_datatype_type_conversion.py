###############################################################################
# TOPIC: Type Conversion (Implicit vs Explicit Casting)
#
# 1. DEFINITION & INTRODUCTION:
#    - Python is strongly typed, meaning it does not automatically perform operations between
#      incompatible types (e.g., adding a string and an integer raises a `TypeError`).
#    - However, it supports:
#        1. Implicit Type Conversion: Automatically handled by the interpreter when safe
#           (e.g., promotion of integer to float).
#        2. Explicit Type Conversion: Programmatically converted by calling constructor
#           functions (e.g. `int()`, `float()`, `str()`).
#
# 2. INTERNAL IMPLEMENTATION:
#    - When you call an explicit converter like `int(obj)`, Python delegates internally to
#      the object's special magic method `obj.__int__()`.
#    - When you call `float(obj)`, it delegates to `obj.__float__()`.
#    - When you call `str(obj)`, it delegates to `obj.__str__()` (falling back to `__repr__()`
#      if `__str__()` is not defined).
#    - Conversions to containers like `list(obj)` or `tuple(obj)` require the object to
#      implement the iterator protocol (`__iter__()` or `__getitem__()`).
#
# 3. CONVERSION EXCEPTIONS & EDGE CASES:
#    - `ValueError`: Raised when the operand has the correct type but an incompatible value
#      for conversion (e.g., `int("abc")`).
#    - `TypeError`: Raised when trying to convert an object of a type that has no conversion
#      interface defined (e.g., `int([1, 2, 3])`).
#    - Casting floating-point special values:
#        - Casting `float('inf')` or `float('nan')` to `int` will raise an `OverflowError`
#          or `ValueError`, as infinity and undefined states cannot be mapped to integers.
#
# 4. BEST PRACTICES:
#    - Always wrap explicit user-input type conversions (e.g. `int(input())`) in a
#      `try-except` block to capture `ValueError`.
#    - Use `isinstance()` to check types instead of comparing `type(obj) == target_type`
#      to support subclass inheritance compatibility.
#
# 5. INTERVIEW QUESTIONS:
#    - Q: What happens when you cast `float('nan')` to an integer?
#      A: It raises a `ValueError` because a Not-a-Number value has no integer equivalent.
#    - Q: How does Python resolve the expression `3 + 4.5`?
#      A: Python implicitly converts the integer `3` to float `3.0` and performs float addition,
#         returning the float `7.5`.
#
# 6. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a custom class representing a fractional string (e.g. "3/4")
#      that supports conversion to float and int by implementing magic methods.
#
###############################################################################

import math  # Standard module to inspect floating-point special states

# 1. Implicit Type Conversion (Promotion)
int_num = 10
float_num = 5.5
# Python automatically promotes 'int_num' to a float before addition
implicit_sum = int_num + float_num
print("--- Implicit Type Conversion ---")
print(f"10 + 5.5 = {implicit_sum} | Result Type: {type(implicit_sum)}")  # Expected: float

# 2. Explicit Type Conversion (Casting)
# String to Integer
str_val = "123"
int_val = int(str_val)
print(f"\nString '{str_val}' cast to int: {int_val} | Type: {type(int_val)}")

# Float to Integer (Truncation)
# Casting a float to int always truncates toward zero (discards fractional part).
float_val = -3.9
truncated_int = int(float_val)
print(f"Float {float_val} cast to int: {truncated_int}")  # Expected: -3

# 3. Custom Class Type Conversion Methods
# Let's create a custom class that implements type casting protocols.
class FractionRepresenter:
    def __init__(self, numerator, denominator):
        self.num = numerator
        self.den = denominator
        
    def __float__(self):
        # Called when float(self) is evaluated
        print(" -> Custom __float__ called!")
        return self.num / self.den
        
    def __int__(self):
        # Called when int(self) is evaluated
        print(" -> Custom __int__ called!")
        return self.num // self.den
        
    def __str__(self):
        # Called when str(self) or print(self) is evaluated
        return f"{self.num}/{self.den}"

frac = FractionRepresenter(10, 3)
print("\n--- Custom Class Conversions ---")
print(f"Fraction object representation: {frac}")
print(f"Casting to float: {float(frac)}")  # Expected: 3.3333333333333335
print(f"Casting to int (floor division): {int(frac)}")  # Expected: 3

# 4. Conversion Failures and Edge Cases
print("\n--- Conversion Error Handling ---")
try:
    # Attempting incompatible conversion
    int("invalid_numeric_string")
except ValueError as e:
    print(f"Caught expected ValueError: {e}")

try:
    # Converting type with no dunder method interface
    int([1, 2])
except TypeError as e:
    print(f"Caught expected TypeError: {e}")

try:
    # Casting infinity to integer raises OverflowError
    int(float('inf'))
except OverflowError as e:
    print(f"Caught expected OverflowError (inf to int): {e}")

try:
    # Casting NaN to integer raises ValueError
    int(float('nan'))
except ValueError as e:
    print(f"Caught expected ValueError (nan to int): {e}")
