###############################################################################
# TOPIC: Core Data Types - Complex Numbers (complex)
#
# 1. DEFINITION & INTRODUCTION:
#    - Python is one of the few mainstream programming languages that provides built-in
#      support for complex numbers. A complex number consists of a real part and an
#      imaginary part, both represented as floating-point numbers.
#
# 2. LITERAL SYNTAX:
#    - The imaginary part is written with a `j` or `J` suffix.
#      Example: `3 + 4j` represents the complex number 3 + 4i.
#    - You can also instantiate them using the constructor: `complex(real, imag)`.
#
# 3. INTERNAL REPRESENTATION & CPYTHON INTERNALS:
#    - Under the hood, Python represents complex numbers using the `PyComplexObject` struct:
#      ```c
#      typedef struct {
#          double real;
#          double imag;
#      } Py_complex;
#
#      typedef struct {
#          PyObject_HEAD
#          Py_complex cval;
#      } PyComplexObject;
#      ```
#    - It stores both components as raw C `double` primitives within the object wrapper.
#
# 4. MEMORY FOOTPRINT:
#    - On 64-bit platforms, a `PyComplexObject` consumes 32 bytes:
#        - 8 bytes reference count (`ob_refcnt`)
#        - 8 bytes type pointer (`ob_type`)
#        - 16 bytes for `Py_complex` (8 bytes real double, 8 bytes imag double)
#
# 5. METHODS & OPERATIONS:
#    - Properties: `z.real` returns the real component (float), `z.imag` returns the
#      imaginary component (float).
#    - Conjugate: `z.conjugate()` returns a complex number with the sign of the
#      imaginary part inverted.
#    - Absolute value: `abs(z)` computes the magnitude (Euclidean distance) of the
#      vector: $\sqrt{real^2 + imag^2}$.
#
# 6. RESTRICTIONS:
#    - Complex numbers cannot be compared using inequalities (e.g., `<` or `>`).
#      Attempting to do so raises a `TypeError`. They only support equality check `==`.
#
# 7. BEST PRACTICES:
#    - Use complex numbers for scientific computations, electromagnetic calculations,
#      quantum physics models, signal processing, or computer graphics.
#    - When parsing strings (e.g. `complex("3+4j")`), ensure there are no spaces around
#      the sign operator inside the string; spaces will trigger a `ValueError`.
#
# 8. INTERVIEW QUESTIONS:
#    - Q: Can you compare two complex numbers using `z1 > z2`?
#      A: No. Complex numbers do not have a natural ordering in mathematics, and Python
#         strictly enforces this by raising a `TypeError` for inequality comparisons.
#    - Q: What type is returned by accessing `z.real`?
#      A: It always returns a float, even if the complex number was created using integers.
#
# 9. EXERCISES & SOLUTIONS:
#    - Coding challenge: Prove that complex numbers support basic arithmetic operations
#      (addition, subtraction, multiplication, division, and exponentiation) and
#      demonstrate absolute value calculations.
#
###############################################################################

import sys  # Standard library to inspect memory sizes
import cmath  # Standard module containing mathematical functions for complex numbers

# 1. Instantiation and Properties
# Option A: Literal declaration (using 'j' or 'J')
z1 = 3 + 4j
# Option B: Constructor declaration
z2 = complex(1, -2)

print("--- Complex Properties & Types ---")
print(f"z1: {z1} | Real part: {z1.real} (type: {type(z1.real)}) | Imaginary part: {z1.imag}")
print(f"z2: {z2} | Real part: {z2.real} | Imaginary part: {z2.imag}")

# 2. Arithmetic Operations
print("\n--- Complex Arithmetic ---")
print(f"Addition (z1 + z2): {z1 + z2}")  # Expected: (4+2j)
print(f"Subtraction (z1 - z2): {z1 - z2}")  # Expected: (2+6j)
print(f"Multiplication (z1 * z2): {z1 * z2}")  # (3+4j)*(1-2j) = 3 - 6j + 4j - 8(j^2) = 11 - 2j
print(f"Division (z1 / z2): {z1 / z2}")  # Euclidean complex division
print(f"Power (z1 ** 2): {z1 ** 2}")  # Squares the complex value

# 3. Conjugate & Magnitude (Absolute Value)
print("\n--- Conjugate and Magnitude ---")
conjugate_z1 = z1.conjugate()
print(f"Conjugate of z1: {conjugate_z1}")  # Expected: (3-4j)
magnitude_z1 = abs(z1)
print(f"Magnitude of z1: {magnitude_z1}")  # Expected: 5.0 (sqrt(3^2 + 4^2))

# 4. Memory Footprint
print(f"\nMemory Size of Complex Object: {sys.getsizeof(z1)} bytes")  # Expected: 32 bytes

# 5. Scientific Math using cmath module
# cmath provides functions for complex numbers analogous to the math module.
print("\n--- Advanced Complex Functions (cmath) ---")
print(f"Phase angle of z1: {cmath.phase(z1)} radians")
polar_coords = cmath.polar(z1)  # Returns (r, phi) magnitude and phase angle
print(f"Polar coordinates (r, phi): {polar_coords}")
print(f"Square root of -1 (cmath.sqrt): {cmath.sqrt(-1)}")  # Expected: 1j

# 6. Inequality Restriction Demonstration
try:
    print(z1 < z2)
except TypeError as e:
    print(f"\nCaught expected TypeError for inequality comparison: {e}")
