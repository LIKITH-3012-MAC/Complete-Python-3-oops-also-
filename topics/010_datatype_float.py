###############################################################################
# TOPIC: Core Data Types - Floats (float)
#
# 1. DEFINITION & INTRODUCTION:
#    - Python's `float` represents real numbers using double-precision floating-point
#      format. Unlike integers, floats do not have arbitrary precision; they are bounded
#      by standard hardware-level precision limits.
#
# 2. INTERNAL REPRESENTATION (IEEE 754 standard):
#    - Python floats map directly to C's `double` type, which implements the IEEE 754
#      double-precision binary floating-point standard.
#    - Memory Layout (64 bits total):
#        - Sign bit: 1 bit (determines positive or negative)
#        - Exponent: 11 bits (determines scale/magnitude)
#        - Fraction (Mantissa): 52 bits (determines precision/significand)
#    - CPython Object Layout (`PyFloatObject`):
#        - 8 bytes reference count (`ob_refcnt`)
#        - 8 bytes type pointer (`ob_type`)
#        - 8 bytes actual double-precision value (`ob_fval`)
#      Thus, a float object occupies exactly 24 bytes of memory on a 64-bit platform.
#
# 3. FLOAT REPRESENTATION LIMITATION (The 0.1 + 0.2 Problem):
#    - Computers represent floats in base 2 (binary). Decimal fractions like `0.1` and `0.2`
#      cannot be represented exactly in binary because they result in repeating fractional
#      expansions (similar to how `1/3` is `0.3333...` in decimal).
#    - For example, `0.1` in binary is: `0.00011001100110011001100110011...` (repeating).
#    - Since the mantissa is truncated to 52 bits, small rounding errors occur.
#      Evaluating `0.1 + 0.2` results in `0.30000000000000004` instead of `0.3`.
#
# 4. SPECIAL FLOATING-POINT VALUES:
#    - Infinity (`inf` / `-inf`): Represents values that overflow exponent limits.
#      Can be created using `float('inf')` or `float('-inf')`.
#    - Not a Number (`nan`): Represents undefined mathematical states (e.g., `inf - inf`).
#      Created using `float('nan')`.
#      Crucial properties of `nan`: It is never equal to anything, including itself
#      (`float('nan') == float('nan')` returns `False`).
#
# 5. SAFE FLOATING-POINT COMPARISONS:
#    - Never compare floats directly using `==`.
#    - Instead, verify that their difference is smaller than a minute threshold (epsilon),
#      or use the standard library function `math.isclose()`.
#
# 6. TIME COMPLEXITY:
#    - Float operations (addition, multiplication) are performed directly by the CPU's FPU
#      (Floating-Point Unit), making them extremely fast O(1) hardware operations.
#
# 7. BEST PRACTICES:
#    - For monetary/financial calculations where representation errors are unacceptable,
#      use Python's standard `decimal` module instead of `float`.
#    - Use `math.isclose()` to write unit tests checking floating-point outputs.
#
# 8. INTERVIEW QUESTIONS:
#    - Q: Why is `0.1 + 0.2 == 0.3` False in Python?
#      A: Because 0.1 and 0.2 cannot be represented exactly in binary floating-point representation.
#         The truncation of repeating binary patterns introduces a tiny rounding error.
#    - Q: How can you check if a variable is `NaN`?
#      A: You cannot use `x == float('nan')`. You must use `math.isnan(x)` or check if
#         it is not equal to itself: `x != x` (which is only true for NaN).
#
# 9. EXERCISES & SOLUTIONS:
#    - Coding challenge: Write a safe comparison function for floating-point calculations
#      without using the `math` module.
#
###############################################################################

import sys  # Standard library to read system float parameters
import math  # Standard module containing floating-point utility functions

# 1. Memory Footprint of Float Object
f_val = 3.14
print("--- Float Memory Footprint ---")
print(f"Float value: {f_val}")
print(f"Memory Size: {sys.getsizeof(f_val)} bytes")  # Expected: 24 bytes

# 2. Float Info and Precision Parameters
# sys.float_info contains limits and precision constants of the platform's float.
print(f"\nMax representable float: {sys.float_info.max}")
print(f"Machine Epsilon (diff between 1 and next float): {sys.float_info.epsilon}")

# 3. Precision Rounding Demonstration
a = 0.1
b = 0.2
sum_ab = a + b
print(f"\nSum: 0.1 + 0.2 = {sum_ab}")  # Expected: 0.30000000000000004
print(f"Is 0.1 + 0.2 == 0.3? {sum_ab == 0.3}")  # Expected: False

# Safe comparison using math.isclose()
is_close = math.isclose(sum_ab, 0.3)
print(f"Is 0.1 + 0.2 close to 0.3? {is_close}")  # Expected: True

# 4. Infinity and NaN Behavior
inf_val = float('inf')
neg_inf_val = float('-inf')
nan_val = float('nan')

print("\n--- Special Values ---")
print(f"Infinity: {inf_val} | Negative Infinity: {neg_inf_val}")
print(f"Infinity plus one: {inf_val + 1}")  # Returns 'inf'
print(f"Is Infinity greater than large number? {inf_val > 10**300}")  # Expected: True

print(f"\nNaN value: {nan_val}")
print(f"Is NaN equal to NaN? {nan_val == nan_val}")  # Expected: False

# Checking for NaN
print(f"Is NaN checked via math.isnan()? {math.isnan(nan_val)}")  # Expected: True
print(f"Is NaN checked via self-inequality? {nan_val != nan_val}")  # Expected: True

# 5. Arithmetic yielding Special Values
# Operations like division of non-zero by zero in pure float values:
# Note: 1.0 / 0.0 raises ZeroDivisionError in Python, but operations on infinity can return NaN.
print(f"Infinity minus Infinity: {inf_val - inf_val}")  # Expected: nan
print(f"NaN times 5: {nan_val * 5}")  # Expected: nan
