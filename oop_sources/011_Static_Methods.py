###############################################################################
# TOPIC: Static Methods - @staticmethod, utility functions, and namespace scoping
#
# 1. DEFINITION & INTRODUCTION:
#    - Static Methods: Methods inside a class namespace that have no access to the class
#      state or instance state.
#    - Signature: Decorated with `@staticmethod`. They behave like regular, plain functions,
#      meaning they receive no implicit first argument (no `self`, no `cls`).
#
# 2. MOTIVATION & SCOPING:
#    - Namespace Organization: Used to group utility or helper functions within a class namespace,
#      making the codebase cleaner and grouping related operations together.
#    - Self-Contained: Ideal for operations that are completely input-to-output mapping functions
#      (e.g., verifying a format, converting units) and do not need to query object instance
#      or class attributes.
#    - Invocation: Can be called via the class name (`Class.method(args)`) or via an instance
#      (`instance.method(args)`). In both contexts, it acts as a direct function call.
#
# 3. STATICMETHOD VS CLASSMETHOD VS INSTANCEMETHOD:
#    - Instance Method: Needs access to object instance details (`self`).
#    - Class Method: Needs access to class attributes or factory constructors (`cls`).
#    - Static Method: Needs access to neither; operates strictly on its passed arguments.
#
# 4. BEST PRACTICES:
#    - Use `@staticmethod` for purely utility-focused functions that do not reference `self` or `cls`.
#      This informs developers (and compiler optimizers) that the function does not modify state.
#
# 5. INTERVIEW QUESTIONS:
#    - Q: When should you use a static method instead of a class method?
#      A: Use a static method when the function performs a self-contained utility operation that
#         does not need to access class variables, subclass references, or construct class instances.
#    - Q: Does a static method support polymorphism (overriding) in subclasses?
#      A: Yes. Like any other method, static methods can be overridden by subclasses to define
#         custom implementations.
#
# 6. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a `TemperatureConverter` class containing static methods to
#      convert Celsius to Fahrenheit and vice versa, verifying execution parameters.
#
###############################################################################

class TemperatureConverter:
    def __init__(self, location):
        self.location = location
        
    # Static method: behaves like a normal utility function
    @staticmethod
    def celsius_to_fahrenheit(celsius):
        # Only operates on input arguments, no self or cls references
        return (celsius * 9/5) + 32
        
    @staticmethod
    def fahrenheit_to_celsius(fahrenheit):
        return (fahrenheit - 32) * 5/9

print("--- Calling Static Methods ---")
# Call static methods directly via Class name (Preferred)
c_val = 25
f_val = TemperatureConverter.celsius_to_fahrenheit(c_val)
print(f"{c_val}°C is equal to {f_val}°F")  # Expected: 77.0°F

f_input = 100
c_output = TemperatureConverter.fahrenheit_to_celsius(f_input)
print(f"{f_input}°F is equal to {c_output:.2f}°C")  # Expected: 37.78°C

# Call static method via Instance
converter_nyc = TemperatureConverter("New York")
print(f"Call via instance: {converter_nyc.celsius_to_fahrenheit(0)}")  # Expected: 32.0 (implicit self NOT passed)

# 2. Verification of Method Types under the hood
print("\n--- Inspecting Method Types ---")
# Unbound static method is simply a function object
print(f"Type of TemperatureConverter.celsius_to_fahrenheit: {type(TemperatureConverter.celsius_to_fahrenheit)}")
# Expected: <class 'function'>

# Accessing via instance also returns a raw function object in modern Python 3
print(f"Type of instance.celsius_to_fahrenheit:           {type(converter_nyc.celsius_to_fahrenheit)}")
# Expected: <class 'function'> (Unlike instance methods which return <class 'method'>)
