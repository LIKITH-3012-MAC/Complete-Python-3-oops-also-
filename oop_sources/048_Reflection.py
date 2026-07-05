###############################################################################
# TOPIC: Reflection - dynamic attribute manipulations, importlib, and monkey patching methods
#
# 1. DEFINITION & INTRODUCTION:
#    - Reflection: The ability of a running program to examine, introspect, and dynamically
#      modify its own structure, variables, classes, and methods at runtime.
#    - Contrast with Introspection:
#        - Introspection is read-only (inspecting type, dir, inspect).
#        - Reflection includes write operations (adding/modifying/deleting attributes or methods).
#
# 2. CORE REFLECTION TOOLS:
#    - Dynamic Attributes:
#        - `setattr(obj, name, value)`: Creates or updates attribute `name` on `obj`.
#        - `getattr(obj, name [, default])`: Retrieves attribute value, supporting fallbacks.
#        - `delattr(obj, name)`: Deletes attribute from object's dictionary.
#        - `hasattr(obj, name)`: Returns boolean indicating attribute presence.
#
# 3. DYNAMIC MODULE/CLASS IMPORTING:
#    - Using the standard library `importlib` module.
#    - Allows loading modules and instantiating classes using string paths from configuration files:
#      `module = importlib.import_module("math")`
#
# 4. DYNAMIC METHOD BINDING (Monkey Patching):
#    - Binding a method to a class dynamically: Just assign the function reference. It behaves
#      as a normal method for all instances immediately.
#    - Binding a method to a *specific instance* only: You cannot do `instance.method = func` directly
#      because it gets stored as a raw function object in the instance dictionary, failing to bind
#      `self`.
#      Solution: Use `types.MethodType(function, instance)` to wrap it as a bound method first.
#
# 5. INTERVIEW QUESTIONS:
#    - Q: How do you bind a method dynamically to a single specific object instance?
#      A: Wrap the raw function with `types.MethodType(function, instance)` and assign it to the
#         desired attribute name on the instance.
#    - Q: What is the difference between introspection and reflection?
#      A: Introspection is analyzing program state (read-only); reflection is modifying program
#         elements (classes, methods, variables) at runtime (write operations).
#
# 6. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a dynamic command executor that reads command strings, dynamically
#      verifies their presence on a controller class using reflection, and executes them with inputs.
#
###############################################################################

import importlib  # Standard module for dynamic imports
import types  # Standard module to wrap bound methods

# 1. Dynamic Attribute Manipulations
class SystemConfig:
    def __init__(self):
        self.port = 8080

config = SystemConfig()

print("--- Dynamic Attributes ---")
# Verify attribute exists and fetch
if hasattr(config, "port"):
    print(f"Fetch via getattr: {getattr(config, 'port')}")

# Modify attribute
setattr(config, "port", 9090)
# Add new attribute
setattr(config, "debug_mode", True)

print(f"Updated dict: {config.__dict__}")  # Expected: {'port': 9090, 'debug_mode': True}

# 2. Dynamic Imports using importlib
# Suppose we want to dynamically load 'math' module and call 'sqrt'
print("\n--- Dynamic Module Loading ---")
module_name = "math"
math_module = importlib.import_module(module_name)
# Fetch the sqrt function object
sqrt_func = getattr(math_module, "sqrt")
print(f"Dynamically loaded math.sqrt(16): {sqrt_func(16)}")  # Expected: 4.0

# 3. Dynamic Method Binding (Monkey Patching)
class Robot:
    def __init__(self, name):
        self.name = name

# Function we want to attach
def speak_function(self, message):
    return f"{self.name} says: {message}"

# Scenario A: Bind to the Class (affects all instances)
print("\n--- Class-Level Monkey Patching ---")
Robot.speak = speak_function  # Bind function to class attribute

r1 = Robot("R2D2")
r2 = Robot("C3PO")
print(r1.speak("Beep Boop"))
print(r2.speak("Hello Sir"))

# Scenario B: Bind to a Specific Instance only
print("\n--- Instance-Level Monkey Patching ---")
def fly_function(self):
    return f"{self.name} is flying through jets!"

# Incorrect way: r1.fly = fly_function (This leaves it unbound, self will not be passed!)
# Correct way using types.MethodType:
r1.fly = types.MethodType(fly_function, r1)  # Bind function specifically to instance r1

print(r1.fly())  # Works! self is implicitly passed.

# Verify sibling r2 does not have the fly method
try:
    print(r2.fly())
except AttributeError as e:
    print(f"Caught expected AttributeError for r2: {e}")
