###############################################################################
# TOPIC: Objects - Instantiation mechanics (__new__ vs __init__) and object Namespaces
#
# 1. DEFINITION & INTRODUCTION:
#    - Object: An instance of a class. It is the concrete realization of the blueprint
#      defined by the class, carrying its own state (data).
#
# 2. INSTANTIATION MECHANICS UNDER THE HOOD:
#    - When you instantiate a class (e.g. `obj = MyClass()`), Python performs two distinct steps:
#        1. Memory Allocation (`__new__`): Python calls `MyClass.__new__(MyClass)`.
#           `__new__` is a static method (implicitly treated as classmethod) responsible for
#           allocating the memory block for the object and returning the raw, uninitialized
#           instance object.
#        2. State Initialization (`__init__`): If `__new__` returns an instance of `MyClass`,
#           Python then calls `MyClass.__init__(instance)`.
#           `__init__` is an instance method that initializes the attributes of the object.
#
# 3. OBJECT NAMESPACE & __DICT__:
#    - Each object instance stores its attributes inside a writeable dictionary called `__dict__`.
#    - When you assign `obj.x = 10`, Python inserts `"x": 10` into `obj.__dict__`.
#    - When you read `obj.x`, Python looks it up in `obj.__dict__` first, falling back to the
#      class `__dict__` if missing.
#
# 4. DYNAMIC ATTRIBUTE ASSIGNMENT (Monkey Patching):
#    - By default, Python allows adding new attributes to an object instance at runtime, even
#      if they were not defined in the class body.
#      Example: `obj.new_attribute = "patched"` is valid.
#
# 5. BEST PRACTICES:
#    - Avoid dynamic attribute additions in production code (confuses linters and makes debugging
#      difficult).
#    - Define all instance fields clearly in `__init__` to make object shapes predictable.
#
# 6. INTERVIEW QUESTIONS:
#    - Q: What is the difference between `__new__` and `__init__`?
#      A: `__new__` is a constructor that allocates and returns the raw object instance.
#         `__init__` is an initializer that configures the properties of the allocated instance.
#    - Q: Where does an object instance store its attributes?
#      A: In the object's instance dictionary `__dict__`.
#
# 7. EXERCISES & SOLUTIONS:
#    - Coding challenge: Override both `__new__` and `__init__` to intercept instantiation steps
#      and print log messages demonstrating execution order.
#
###############################################################################

# 1. Class demonstrating __new__ vs __init__
class User:
    def __new__(cls, *args, **kwargs):
        # Step 1: Allocate memory for the object by delegating to base object class
        print(f"1. __new__ called! Allocating memory for class: {cls}")
        raw_instance = super().__new__(cls)
        return raw_instance  # Must return the allocated object
        
    def __init__(self, username):
        # Step 2: Initialize properties on the returned instance
        print(f"2. __init__ called! Configuring instance state with username: {username}")
        self.username = username

print("--- Instantiating User Object ---")
user_obj = User("likith")
print(f"User Object reference: {user_obj}")

# 2. Inspecting Object Namespace (__dict__)
print("\n--- Object Namespace Inspection ---")
print(f"user_obj.__dict__: {user_obj.__dict__}")  # Expected: {'username': 'likith'}

# Writing directly to __dict__ is allowed and has the same effect as standard attribute writing
user_obj.__dict__["role"] = "admin"
print(f"Role read from property: {user_obj.role}")  # Expected: 'admin'

# 3. Dynamic Attribute Assignment (Monkey Patching)
# We can attach attributes that were never specified in the class definition.
user_obj.age = 25
print(f"user_obj.__dict__ after monkey patching: {user_obj.__dict__}")
# Expected: {'username': 'likith', 'role': 'admin', 'age': 25}

# 4. Identity Check of Instances
user_obj2 = User("likith")
print(f"\nComparing identities of two instances (user_obj is user_obj2): {user_obj is user_obj2}")
# Expected: False (They occupy different memory slots)
