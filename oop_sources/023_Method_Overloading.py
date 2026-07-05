###############################################################################
# TOPIC: Method Overloading - namespace limitations, default arguments, and singledispatchmethod
#
# 1. DEFINITION & PYTHON LIMITATIONS:
#    - Method Overloading: Defining multiple methods in the same class with the same name
#      but different parameter signatures (types or counts).
#    - Python Namespace Collision: Python does NOT support native method overloading.
#      Since class methods are stored in a namespace dictionary (`class_dict`), defining
#      multiple methods with the same name results in the last definition overwriting all
#      previous definitions.
#
# 2. OVERLOADING ALTERNATIVES:
#    To achieve overloading behaviors, Python developers use three approaches:
#    - Method A: Default Parameters. Set parameters to `None` and check their presence dynamically.
#      Example: `def area(self, radius=None, length=None, width=None):`
#    - Method B: Type Checks inside the method. Check types using `isinstance()` to branch logic.
#    - Method C: `@functools.singledispatchmethod` (Python 3.8+):
#        - Decorator that registers alternative implementations of a method based on the type of
#          the first non-self/non-cls argument.
#        - Provides clean, decorator-driven type-based dispatching without write-heavy, nested
#          `if isinstance` chains.
#
# 3. BEST PRACTICES:
#    - Use default parameters or variable arguments for count-based overloading.
#    - Use `@singledispatchmethod` for type-based overloading of method logic.
#
# 4. INTERVIEW QUESTIONS:
#    - Q: Why doesn't Python support native method overloading?
#      A: Because method names are dictionary keys in the class namespace. A key can only map to
#         one value (the last method defined with that name).
#    - Q: How can you write a method that accepts either an integer or a string in Python 3.8+?
#      A: Use the `@functools.singledispatchmethod` decorator to register distinct functions
#         for `int` and `str` types.
#
# 5. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a `DataExporter` class containing an `export` method overloaded
#      to process either a list, a dictionary, or a string using `@singledispatchmethod`.
#
###############################################################################

import functools  # standard library module containing singledispatchmethod

# 1. Method Overloading via Default Parameters
class AreaCalculator:
    def calculate(self, dim1, dim2=None):
        if dim2 is None:
            # Assumed to be a square: dim1 is side
            print(" -> Square area calculation")
            return dim1 * dim1
        else:
            # Assumed to be a rectangle: dim1 is length, dim2 is width
            print(" -> Rectangle area calculation")
            return dim1 * dim2

calc = AreaCalculator()
print("--- Overloading via Default Parameters ---")
print(f"Area(5):    {calc.calculate(5)}")     # Expected: 25
print(f"Area(5, 4): {calc.calculate(5, 4)}")  # Expected: 20

# 2. Type-based Overloading using @singledispatchmethod (Python 3.8+)
class DataLogger:
    @functools.singledispatchmethod
    def log(self, data):
        # Base/Fallback method called if no registered type matches
        raise TypeError(f"Unsupported logging type: {type(data)}")
        
    # Register implementation for integer types
    @log.register
    def _(self, data: int):
        print(f" -> [Logging Integer]: Value={data} | Double={data * 2}")
        
    # Register implementation for string types
    @log.register
    def _(self, data: str):
        print(f" -> [Logging String]: Text='{data}' | Length={len(data)}")
        
    # Register implementation for list types
    @log.register
    def _(self, data: list):
        print(f" -> [Logging List]: Items count={len(data)} | Values={data}")

logger = DataLogger()

print("\n--- Overloading via singledispatchmethod ---")
# Call overloaded log() with different types
logger.log(100)            # Calls integer registration
logger.log("Hello Python") # Calls string registration
logger.log([10, 20, 30])   # Calls list registration

# Call with unsupported type
try:
    logger.log(3.14)  # float not registered
except TypeError as e:
    print(f"Caught expected TypeError: {e}")
