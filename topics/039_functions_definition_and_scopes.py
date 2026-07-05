###############################################################################
# TOPIC: Functions - Definition, Scoping, and First-Class Citizens
#
# 1. DEFINITION & INTRODUCTION:
#    - A function is a reusable, modular block of code designed to perform a specific action.
#    - Declared using the `def` keyword.
#
# 2. DOCSTRINGS (PEP 257):
#    - Docstrings (documentation strings) are triple-quoted string literals placed immediately
#      below the function header.
#    - Python's compiler processes docstrings and stores them in the function's `__doc__`
#      attribute, accessible at runtime for interactive help and automated documentation.
#
# 3. FIRST-CLASS OBJECTS:
#    - In Python, functions are First-Class Citizens. This means functions are treated as
#      objects:
#        - They can be assigned to variable names.
#        - They can be passed as arguments to other functions.
#        - They can be returned as values from other functions.
#        - They can be stored in data structures (lists, dictionaries, etc.).
#
# 4. NESTED FUNCTIONS & PARAMETER BINDING:
#    - You can define functions inside other functions (nested or inner functions).
#    - Nested functions have read-only access to variables defined in the enclosing outer
#      function's scope, forming enclosing scopes (E in the LEGB resolution rule).
#
# 5. TIME & SPACE COMPLEXITY:
#    - Function call overhead: Small cost of pushing an execution frame onto the heap.
#
# 6. BEST PRACTICES:
#    - Always include descriptive docstrings detailing input arguments, expected return types,
#      and raised exceptions.
#    - Keep functions short, focused on a single responsibility (Single Responsibility Principle).
#
# 7. INTERVIEW QUESTIONS:
#    - Q: What does it mean that functions are "first-class citizens" in Python?
#      A: It means they are objects; they can be passed as arguments, returned from other
#         functions, assigned to variables, and stored in collections.
#    - Q: How do you access a function's documentation string at runtime?
#      A: By accessing the function's `__doc__` attribute (e.g. `func.__doc__`) or using
#         the built-in `help(func)` utility.
#
# 8. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a basic mathematical operations dispatcher dictionary
#      where values are functions, and call them dynamically using keys.
#
###############################################################################

# 1. Function Definition & Docstring
def calculate_area(length, width):
    """Calculate the area of a rectangle.
    
    Args:
        length (float/int): The length of the rectangle.
        width (float/int): The width of the rectangle.
        
    Returns:
        float/int: The computed area.
    """
    return length * width

print("--- Function Docstrings ---")
print(f"Function Name: {calculate_area.__name__}")
print(f"Docstring content:\n{calculate_area.__doc__}")

# 2. Functions as First-Class Citizens
# Assigning a function to a variable
area_runner = calculate_area
print(f"Calling function via reference variable: {area_runner(5, 4)}")  # Expected: 20

# Passing a function as an argument
def execute_operation(operation_func, val_a, val_b):
    # operation_func is expected to be a callable function object
    return operation_func(val_a, val_b)

# We pass 'calculate_area' function object as a parameter
op_result = execute_operation(calculate_area, 10, 3)
print(f"Result from passed function argument: {op_result}")  # Expected: 30

# 3. Returning Functions from Functions
# Functions can create and return other functions dynamically.
def get_operation_multiplier(multiplier):
    def scale_function(value):
        # Nested function references 'multiplier' from enclosing outer scope
        return value * multiplier
    return scale_function  # Returns the inner function object

triple_scaler = get_operation_multiplier(3)
print(f"\nType of triple_scaler: {type(triple_scaler)}")  # Expected: function
print(f"Calling returned function: {triple_scaler(10)}")  # Expected: 30

# 4. Functions inside Data Structures (Dispatcher)
# We map commands to actual function objects to create a dispatcher.
def add(a, b): return a + b
def subtract(a, b): return a - b

math_dispatcher = {
    "sum": add,
    "diff": subtract
}

print("\n--- Dispatcher Call ---")
command = "sum"
# Fetch function reference from dictionary and invoke it directly
resolved_operation = math_dispatcher[command]
print(f"Executing '{command}': {resolved_operation(15, 5)}")  # Expected: 20
