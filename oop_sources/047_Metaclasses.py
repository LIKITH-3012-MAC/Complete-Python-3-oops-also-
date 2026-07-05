###############################################################################
# TOPIC: Metaclasses - Class compilation interception, custom metaclasses, and class validation
#
# 1. DEFINITION & THE TYPE HIERARCHY:
#    - Metaclass: A class whose instances are classes. Just as an object is an instance
#      of a class, a class is an instance of a metaclass.
#    - In Python, the default metaclass is the built-in `type`. Any standard class definition:
#      `class MyClass: pass` is compiled at runtime into a class object by calling:
#      `MyClass = type("MyClass", (object,), {})`
#
# 2. CUSTOM METACLASS MECHANICS:
#    - To intercept class compilation, inherit from `type`:
#      `class CustomMeta(type):`
#    - You can override two core methods to customize class instantiation:
#        1. `__new__(mcs, name, bases, attrs)`:
#            - Receives metaclass, name of class, base classes tuple, and attribute namespace dict.
#            - Responsible for allocating and returning the new class object.
#            - Used to modify class attributes, inject methods, or filter properties *before* the
#              class object is created.
#        2. `__init__(cls, name, bases, attrs)`:
#            - Called after the class object is allocated.
#            - Used to perform configuration, validation, or registry additions.
#
# 3. USE CASES:
#    - Coding standards enforcement: Ensuring subclass methods conform to naming patterns.
#    - Automatic registry: Adding newly compiled plugin classes to a central list automatically.
#    - Singleton pattern: Overriding `__call__` on a metaclass to restrict a class to only one
#      instantiated object instance.
#
# 4. BEST PRACTICES:
#    - Avoid metaclasses if you can achieve the same goal with class decorators or `__init_subclass__`
#      (PEP 487). Metaclasses introduce complex type-binding hierarchies.
#
# 5. INTERVIEW QUESTIONS:
#    - Q: What does `type` return when called with three arguments: `type(name, bases, dict)`?
#      A: It dynamically compiles and returns a new class object.
#    - Q: What is the execution order of `__new__` and `__init__` in a metaclass?
#      A: `__new__` is called first to allocate the class object; `__init__` is called second
#         to configure the initialized class object.
#
# 6. EXERCISES & SOLUTIONS:
#    - Coding challenge: Create a metaclass `AttributeLockMeta` that verifies that all method names
#      declared inside the class body are strictly lowercase, raising a `TypeError` if not.
#
###############################################################################

# 1. Coding standards validation metaclass
class LowercaseMethodValidatorMeta(type):
    # Overriding __new__ to inspect class namespace attributes before class allocation
    def __new__(mcs, name, bases, attrs):
        print(f" -> [Metaclass __new__] Compiling class structure: {name}")
        
        # Verify that all user-defined methods are lowercase
        for attr_name, attr_val in attrs.items():
            # Filter for magic/dunder methods (like __init__) and callable methods
            if not attr_name.startswith("__") and callable(attr_val):
                if not attr_name.islower():
                    raise TypeError(f"Method '{attr_name}' in class '{name}' must be strictly lowercase!")
                    
        # Allocate and return the class object using base type.__new__
        return super().__new__(mcs, name, bases, attrs)

# 2. Inherit Metaclass in Class (conforming to style)
class ValidWorker(metaclass=LowercaseMethodValidatorMeta):
    def work(self):
        return "Working hard."
        
    def write_report(self):
        return "Report finished."

print("--- Valid class compiled successfully ---")
worker = ValidWorker()
print(f"Worker report: {worker.write_report()}")

# 3. Inherit Metaclass in Class (violating style)
try:
    class InvalidWorker(metaclass=LowercaseMethodValidatorMeta):
        def work(self):
            return "Working..."
            
        def WriteReport(self):  # Violates strictly lowercase rule!
            return "Report..."
except TypeError as e:
    print(f"\nCaught expected compilation TypeError from Metaclass validator:\n  {e}")

# 4. Metaclass Singleton implementation (Overriding __call__)
class SingletonMeta(type):
    _instances = {}
    
    # Overriding __call__ intercepts class instantiation calls: MyClass()
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            # Create instance and save to cache
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class DatabaseConnectionPool(metaclass=SingletonMeta):
    def __init__(self):
        print(" -> Initializing Database Connection Pool instance (should happen only once).")

print("\n--- Testing Singleton Metaclass ---")
db1 = DatabaseConnectionPool()
db2 = DatabaseConnectionPool()
print(f"Are db1 and db2 the exact same instance? {db1 is db2}")  # Expected: True
