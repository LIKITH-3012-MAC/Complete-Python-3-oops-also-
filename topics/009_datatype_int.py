###############################################################################
# TOPIC: Core Data Types - Integers (int)
#
# 1. DEFINITION & INTRODUCTION:
#    - Python's `int` represents signed integers of arbitrary precision. Unlike many
#      languages (C, C++, Java) that have fixed-width integer types (like 32-bit or
#      64-bit limits), Python integers have no upper or lower limit, restricted only
#      by the system's available memory.
#
# 2. INTERNAL IMPLEMENTATION & CPYTHON INTERNALS:
#    - How does arbitrary precision work? Under the hood in CPython, integers are represented
#      by a variable-length structural object defined in C:
#      ```c
#      struct _longobject {
#          PyObject_VAR_HEAD
#          digit ob_digit[1];
#          ...
#      };
#      ```
#    - The `ob_digit` field is an array of 32-bit unsigned integers representing the
#      value in base 2^30 (or base 2^15 on 32-bit platforms).
#    - Each element of this array is called a "limb". The sign of the integer is stored
#      in the size of the array (positive size = positive integer, negative size = negative integer).
#    - Limbs allow Python to carry out arithmetic operations of any size by performing
#      limb-by-limb operations, carrying values over manually as taught in school arithmetic.
#
# 3. MEMORY FOOTPRINT:
#    - A Python integer object carries significant metadata overhead compared to native C integers.
#    - The minimum size of a Python integer on 64-bit systems is 28 bytes:
#        - 8 bytes reference count (`ob_refcnt`)
#        - 8 bytes type pointer (`ob_type`)
#        - 8 bytes size metadata (`ob_size`)
#        - 4 bytes for the first limb value (`ob_digit[0]`)
#    - Every additional limb adds 4 bytes of memory footprint.
#
# 4. LITERAL REPRESENTATIONS:
#    Python supports defining integer literals in multiple bases:
#    - Decimal (base 10): Default (e.g., `123`)
#    - Binary (base 2): Starts with `0b` or `0B` (e.g., `0b1111011`)
#    - Octal (base 8): Starts with `0o` or `0O` (e.g., `0o173`)
#    - Hexadecimal (base 16): Starts with `0x` or `0X` (e.g., `0x7B`)
#
# 5. DIVISION MECHANICS:
#    - True Division (`/`): Returns a float value (e.g., `5 / 2` evaluates to `2.5`),
#      even if the division is clean (e.g., `4 / 2` evaluates to `2.0`).
#    - Floor Division (`//`): Performs division and truncates the decimal component down
#      to the nearest smaller integer (e.g., `5 // 2` evaluates to `2`, `-5 // 2` to `-3`).
#    - Modulo (`%`): Computes remainder of floor division. Follows sign of divisor (denominator).
#
# 6. TIME COMPLEXITY OF ARITHMETIC:
#    - Addition/Subtraction: O(N) where N is the number of limbs.
#    - Multiplication: Python uses Karatsuba multiplication for large numbers,
#      running in O(N^1.58) instead of O(N^2).
#
# 7. BEST PRACTICES:
#    - Use underscores `_` in large integer literals for readability (e.g., `1_000_000`).
#      Underscores are ignored by the compiler.
#    - Use `int.bit_length()` to dynamically inspect the number of bits needed to
#      represent the integer in binary.
#
# 8. COMMON PITFALLS:
#    - Confusing `//` (floor division) with truncation toward zero. For positive numbers,
#      they behave the same. For negative numbers, floor division rounds down (away from zero).
#
# 9. INTERVIEW QUESTIONS:
#    - Q: How does Python prevent integer overflow?
#      A: It represents integers as arrays of digits (limbs) in C, automatically allocating
#         more limbs as the number grows, bypassing register-size limitations.
#    - Q: What is the output of `-5 // 2`?
#      A: `-3`. Floor division rounds down to the next lower integer, which for -2.5 is -3.
#
# 10. EXERCISES & SOLUTIONS:
#     - Coding challenge: Implement a function to calculate the byte size of an integer
#       using sys.getsizeof() and count its limb increments.
#
###############################################################################

import sys  # standard library to inspect object memory sizes

# 1. Base Literal Declarations
# All these assignments create integer objects representing the value 123.
dec_val = 123
bin_val = 0b1111011  # Binary representation
oct_val = 0o173      # Octal representation
hex_val = 0x7B       # Hexadecimal representation

print("--- Base Conversions ---")
print(f"Values match? {dec_val == bin_val == oct_val == hex_val}")  # Expected: True
print(f"Hex output: {hex(dec_val)}")  # Converts integer to hex string '0x7b'
print(f"Octal output: {oct(dec_val)}")  # Converts to octal string '0o173'
print(f"Binary output: {bin(dec_val)}")  # Converts to binary string '0b1111011'

# 2. Arbitrary Precision Demonstration
# Compute an extremely large number that would overflow standard 64-bit integer registers
super_large = 10**60
print(f"\nSuper Large Integer: {super_large}")
print(f"Bit length of 10^60: {super_large.bit_length()} bits")

# 3. Memory Overhead of python Integers
# Observe how size increases as the number grows and requires more digits/limbs.
small_int = 0
mid_int = 2**30 - 1  # Fits in 1 limb (on 64-bit CPython, digits are 30-bit)
large_int = 2**30    # Requires 2 limbs

print(f"\nMemory Size of 0: {sys.getsizeof(small_int)} bytes")  # Expected: 24 or 28 bytes
print(f"Memory Size of 2^30 - 1 (1 limb): {sys.getsizeof(mid_int)} bytes")  # Base object + 1 limb
print(f"Memory Size of 2^30 (2 limbs): {sys.getsizeof(large_int)} bytes")  # Base object + 2 limbs

# 4. Division Mechanics
print("\n--- Division Behavior ---")
print(f"5 / 2 (True Division) = {5 / 2} | type: {type(5 / 2)}")  # Expected: 2.5, type float
print(f"5 // 2 (Floor Division) = {5 // 2} | type: {type(5 // 2)}")  # Expected: 2, type int
print(f"-5 // 2 (Negative Floor Division) = {-5 // 2}")  # Expected: -3 (rounds down)
print(f"5 % 2 (Modulo) = {5 % 2}")  # Remainder is 1
print(f"-5 % 2 (Negative Modulo) = {-5 % 2}")  # -5 // 2 is -3. -3 * 2 = -6. -5 - (-6) = 1. Remainder is 1.
print(f"5 % -2 (Negative Divisor Modulo) = {5 % -2}")  # Divisor is negative, remainder is -1.

# 5. Native Bitwise Operations
# Python integers support standard bitwise operations.
bit_x = 0b1100  # 12
bit_y = 0b1010  # 10

print("\n--- Bitwise Operations ---")
print(f"Bitwise AND (x & y): {bin(bit_x & bit_y)}")  # Expected: 0b1000 (8)
print(f"Bitwise OR (x | y): {bin(bit_x | bit_y)}")   # Expected: 0b1110 (14)
print(f"Bitwise XOR (x ^ y): {bin(bit_x ^ bit_y)}")  # Expected: 0b0110 (6)
print(f"Bit Shift Left (x << 2): {bin(bit_x << 2)}")  # Expected: 0b110000 (48)
