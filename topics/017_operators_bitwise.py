###############################################################################
# TOPIC: Bitwise Operators and Binary Arithmetic
#
# 1. DEFINITION & INTRODUCTION:
#    - Bitwise operators perform operations directly on the binary representation of integers.
#      Operators include:
#        - Bitwise AND (`&`): Sets bit to 1 if both bits are 1.
#        - Bitwise OR (`|`): Sets bit to 1 if at least one bit is 1.
#        - Bitwise XOR (`^`): Sets bit to 1 if bits are different.
#        - Bitwise Inversion (`~`): Inverts all bits.
#        - Left Shift (`<<`): Shifts bits left, filling empty spots with 0. Equivalents to $x \times 2^n$.
#        - Right Shift (`>>`): Shifts bits right. Equivalent to $x // 2^n$.
#
# 2. TWO'S COMPLEMENT & SIGN EXTENSION:
#    - Python integers use a Two's Complement representation for negative numbers.
#    - Unlike fixed-width systems where the sign bit is at a fixed offset (e.g., bit 31 or 63),
#      Python's arbitrary-precision integers behave as if they have an infinite number
#      of sign bits extending to the left.
#    - When you invert a positive integer `x` using `~x`, Python returns `-(x + 1)`.
#      For instance, `~0` is `-1`, and `~10` is `-11`.
#
# 3. BITMASKS & FLAGS (Real-world Application):
#    - Bitwise operations are used to pack multiple boolean flags into a single integer
#      to save memory and accelerate database/network operations.
#    - Setting a flag: `flags |= MASK`
#    - Clearing a flag: `flags &= ~MASK`
#    - Toggling a flag: `flags ^= MASK`
#    - Checking a flag: `(flags & MASK) == MASK`
#
# 4. TIME COMPLEXITY:
#    - Bitwise operations on integers are extremely fast O(1) operations, resolved directly
#      by hardware registers inside the CPU (for numbers fitting standard register size).
#
# 5. BEST PRACTICES:
#    - Use parenthesis when combining bitwise operations and comparison/arithmetic operators.
#      Bitwise operators have lower precedence than arithmetic/comparison operators,
#      which can lead to subtle bugs (e.g., `x & 1 == 0` evaluates as `x & (1 == 0)`).
#
# 6. INTERVIEW QUESTIONS:
#    - Q: Explain what `x & (x - 1)` does.
#      A: It clears the lowest set bit (the rightmost 1-bit) of the integer `x`.
#         If `x & (x - 1) == 0` and `x > 0`, the number `x` is a power of 2.
#    - Q: What is the output of `~5`?
#      A: `-6`. Bitwise inversion of `x` is computed as `-(x + 1)`.
#
# 7. EXERCISES & SOLUTIONS:
#    - Coding challenge: Write a function that counts the number of set bits (1s) in an
#      integer (Hamming Weight) using bitwise shifts.
#
###############################################################################

# 1. Bitwise Arithmetic Demonstration
a = 12  # Binary: 1100
b = 10  # Binary: 1010

print("--- Bitwise Arithmetic ---")
print(f"a = {a} (bin: {bin(a)}) | b = {b} (bin: {bin(b)})")
print(f"a & b (AND) = {a & b} (bin: {bin(a & b)})")  # Expected: 8 (bin: 0b1000)
print(f"a | b (OR)  = {a | b} (bin: {bin(a | b)})")  # Expected: 14 (bin: 0b1110)
print(f"a ^ b (XOR) = {a ^ b} (bin: {bin(a ^ b)})")  # Expected: 6 (bin: 0b0110)

# Bitwise Inversion
# ~x = -(x + 1)
print(f"~a (NOT a)  = {~a} (bin: {bin(~a)})")        # Expected: -13 (bin: -0b1101)

# Shifts
print(f"a << 2 (Left Shift)  = {a << 2}")            # Expected: 48 (12 * 4)
print(f"a >> 2 (Right Shift) = {a >> 2}")            # Expected: 3 (12 // 4)

# 2. Real-world Bitmask/Flag System Simulation
# Define bitmasks for permissions (powers of 2)
READ = 0b0001     # 1
WRITE = 0b0010    # 2
EXECUTE = 0b0100  # 4
DELETE = 0b1000   # 8

# Start with empty permission flags
user_permissions = 0b0000

# Set READ and WRITE permissions
user_permissions |= READ
user_permissions |= WRITE
print(f"\nPermissions after adding READ & WRITE: {bin(user_permissions)}")  # Expected: 0b0011

# Check if user has EXECUTE permission (should be False)
has_exec = (user_permissions & EXECUTE) != 0
print(f"Has EXECUTE permission? {has_exec}")  # Expected: False

# Check if user has WRITE permission (should be True)
has_write = (user_permissions & WRITE) != 0
print(f"Has WRITE permission? {has_write}")  # Expected: True

# Toggle EXECUTE permission
user_permissions ^= EXECUTE
print(f"Permissions after toggling EXECUTE: {bin(user_permissions)}")  # Expected: 0b0111

# Clear WRITE permission
user_permissions &= ~WRITE
print(f"Permissions after clearing WRITE: {bin(user_permissions)}")  # Expected: 0b0101 (READ and EXECUTE only)

# 3. Hamming Weight (Counting Set Bits) Algorithm
def count_set_bits(n):
    count = 0
    # Loop runs until all bits are shifted out (n becomes 0)
    while n > 0:
        count += n & 1  # Add 1 to count if rightmost bit is 1
        n >>= 1         # Shift bits to the right by 1
    return count

test_num = 29  # Binary: 11101 (Set bits: 4)
print(f"\nSet bits in 29: {count_set_bits(test_num)}")  # Expected: 4
