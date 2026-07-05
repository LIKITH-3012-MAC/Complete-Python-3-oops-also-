###############################################################################
# TOPIC: Descriptors - Descriptor Protocol, dynamic lookups, and Data vs Non-Data precedence
#
# 1. DEFINITION & INTRODUCTION:
#    - Descriptor: A Python object that defines database-like access control for other objects
#      by implementing the **Descriptor Protocol**.
#    - The protocol consists of four magic methods:
#        - `__get__(self, instance, owner)`: Called when retrieving the attribute.
#        - `__set__(self, instance, value)`: Called when setting the attribute.
#        - `__delete__(self, instance)`: Called when deleting the attribute.
#        - `__set_name__(self, owner, name)`: (PEP 487, Python 3.6+): Automatically called at
#          class definition time, passing the class object `owner` and the variable name string `name`
#          the descriptor was assigned to. This avoids passing the field name string manually.
#
# 2. DATA VS NON-DATA DESCRIPTORS (Critical Lookup Precedence rules):
#    - Data Descriptors: Implement `__set__()` or `__delete__()` (or both).
#        - Lookup Priority: Data descriptors take precedence over the instance dictionary `__dict__`.
#          If `x` is a data descriptor and you write `obj.x = 20`, it routes to `__set__`. If you read
#          `obj.x`, it routes to `__get__`, even if `"x"` is also a key in `obj.__dict__`!
#    - Non-Data Descriptors: Implement only `__get__()` (e.g. methods, classmethods, staticmethods).
#        - Lookup Priority: The instance dictionary `__dict__` takes precedence over non-data descriptors.
#          If you write `obj.method = "override"`, it writes `"method": "override"` to `obj.__dict__`,
#          shadowing the descriptor completely on subsequent reads.
#
# 3. INTERVIEW QUESTIONS:
#    - Q: What does `__set_name__` do in the descriptor protocol?
#      A: It captures the variable name string the descriptor is bound to in the class namespace
#         automatically at compile time, resolving the need to hardcode backing field names.
#    - Q: Explain the difference in lookup priority between Data and Non-Data descriptors.
#      A: Data descriptors (defining `__set__`/`__delete__`) override instance dictionary lookups.
#         Non-data descriptors (defining only `__get__`) are overridden (shadowed) by keys in the
#         instance dictionary.
#
# 4. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement an integer validator descriptor `IntegerField` using the
#      descriptor protocol, incorporating `__set_name__` to automatically assign backing storage
#      keys (e.g. `_name`), and enforce bounds.
#
###############################################################################

# 1. Custom Data Descriptor
class IntegerField:
    def __set_name__(self, owner, name):
        # PEP 487: Automatically captures the property name (e.g., 'age')
        print(f" -> [IntegerField __set_name__] Bound to attribute name: '{name}'")
        self.public_name = name
        # We define a unique backing variable name in the instance dictionary
        self.private_name = "_" + name
        
    def __get__(self, instance, owner):
        if instance is None:
            # Called via Class directly (e.g. ClassName.field)
            return self
        print(f" -> [__get__] Reading '{self.public_name}' from instance {instance}")
        # Fetch the value from the instance's private backing variable
        return getattr(instance, self.private_name, None)
        
    def __set__(self, instance, value):
        print(f" -> [__set__] Writing '{self.public_name}' = {value}")
        if not isinstance(value, int):
            raise TypeError(f"Attribute '{self.public_name}' must be an integer!")
        # Write directly to instance backing variable (bypasses descriptor __set__)
        setattr(instance, self.private_name, value)

# Class consuming our descriptor
class Profile:
    # Instantiate descriptors. __set_name__ is called automatically for 'age' and 'score'
    age = IntegerField()
    score = IntegerField()
    
    def __init__(self, username, age, score):
        self.username = username
        self.age = age      # Calls descriptor __set__
        self.score = score  # Calls descriptor __set__

print("--- Class Compilation (Descriptor Binding) ---")
# When class Profile is compiled, __set_name__ is run automatically.
# Let's instantiate and test:
user_profile = Profile("Alice", 25, 95)

print("\n--- Reading Attributes ---")
print(f"User Age:   {user_profile.age}")
print(f"User Score: {user_profile.score}")

print("\n--- Testing Descriptor Type Constraints ---")
try:
    user_profile.age = "twenty-five"
except TypeError as e:
    print(f"Caught expected TypeError: {e}")

# Inspect instance dict namespace
print(f"\nInstance __dict__: {user_profile.__dict__}")
# Expected backing storage: {'username': 'Alice', '_age': 25, '_score': 95}
