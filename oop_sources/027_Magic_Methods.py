###############################################################################
# TOPIC: Magic Methods - String conversions, attribute interceptors, and lifecycle
#
# 1. DEFINITION & INTRODUCTION:
#    - Magic Methods (also known as Dunder Methods due to double underscores `__`) are special
#      methods pre-defined by Python that you can override to hook into specific interpreter
#      actions or syntax elements.
#
# 2. STRING AND REPRESENTATION DUNDERS:
#    - `__repr__(self)`: Unambiguous representation of the object state. Called by `repr(obj)`
#      and shown in the interactive prompt and lists.
#    - `__str__(self)`: User-friendly string representation. Called by `str(obj)` and `print()`.
#    - `__format__(self, format_spec)`: Customizes formatting output inside f-strings or
#      `.format()` when format specifiers are provided (e.g. `f"{obj:custom_spec}"`).
#
# 3. ATTRIBUTE ACCESS INTERCEPTORS:
#    - `__getattr__(self, name)`: Called ONLY when the requested attribute is not found
#      through normal lookups (in instance or class dicts). Acts as a fallback attribute handler.
#    - `__getattribute__(self, name)`: Called unconditionally on EVERY attribute access.
#      It is the primary entry point for attribute lookups.
#      WARNING: When overriding `__getattribute__`, you must delegate to the base class
#      `super().__getattribute__(name)` to avoid infinite recursive calls!
#      Example: Accessing `self.x` inside `__getattribute__` calls `__getattribute__` again,
#      crashing the stack.
#    - `__setattr__(self, name, value)`: Called on every attribute write operation.
#    - `__delattr__(self, name)`: Called when an attribute is deleted (`del obj.name`).
#
# 4. BEST PRACTICES:
#    - When overriding attribute descriptors or interceptors, be extremely careful of recursion.
#      Use `super()` to read or write attributes rather than self-referential dot notation.
#
# 5. INTERVIEW QUESTIONS:
#    - Q: What is the difference between `__getattr__` and `__getattribute__`?
#      A: `__getattribute__` is called unconditionally for every single attribute access.
#         `__getattr__` is only called as a fallback after normal lookup fails to locate the attribute.
#    - Q: How do you prevent infinite recursion inside `__setattr__`?
#      A: By delegating the attribute write to `super().__setattr__(name, value)` or writing
#         directly to `self.__dict__[name] = value` (which bypasses the interceptor).
#
# 6. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a class `DynamicLogger` that intercepts all attribute reads
#      and writes, logs them, and implements a custom f-string formatting specifier.
#
###############################################################################

# 1. Custom Class implementing String and Formatting Dunders
class CustomTimestamp:
    def __init__(self, epoch_seconds):
        self.seconds = epoch_seconds
        
    def __repr__(self):
        return f"CustomTimestamp({self.seconds})"
        
    def __str__(self):
        import time
        # Return a readable string format
        gm_time = time.gmtime(self.seconds)
        return time.strftime("%Y-%m-%d %H:%M:%S GMT", gm_time)
        
    def __format__(self, format_spec):
        # Intercept formatting options
        if format_spec == "raw":
            return str(self.seconds)
        elif format_spec == "date_only":
            import time
            gm_time = time.gmtime(self.seconds)
            return time.strftime("%Y-%m-%d", gm_time)
        return self.__str__()

ts = CustomTimestamp(1719830400)  # July 1, 2024
print("--- String and Format Dunders ---")
print(f"repr(ts): {repr(ts)}")  # Expected: CustomTimestamp(1719830400)
print(f"str(ts):  {ts}")        # Expected: 2024-07-01 00:00:00 GMT
print(f"Format 'raw':       {ts:raw}")        # Expected: 1719830400
print(f"Format 'date_only': {ts:date_only}")  # Expected: 2024-07-01

# 2. Attribute Access Interceptors
class AttributeGuard:
    def __init__(self, key):
        # We must use super() or bypass to set attributes in __init__
        # to avoid triggering our overridden __setattr__ if we want to bypass it.
        # But here we want __setattr__ to run, which is fine.
        self.key = key
        
    def __getattr__(self, name):
        # Fallback handler: runs only if attribute is missing
        print(f" -> [__getattr__] '{name}' not found. Returning fallback string.")
        return f"Attribute '{name}' is dynamically generated."
        
    def __setattr__(self, name, value):
        print(f" -> [__setattr__] Intercepting write: {name} = {repr(value)}")
        # Check validation constraint before writing
        if name == "key" and not isinstance(value, str):
            raise TypeError("Key must be a string!")
        # Use super() to write the attribute to prevent infinite recursion loop
        super().__setattr__(name, value)

print("\n--- Attribute Interception Execution ---")
guard = AttributeGuard("API_KEY_1")

# Accessing existing attribute (resolves normally, __getattr__ NOT called)
print(f"Read key: {guard.key}")

# Accessing missing attribute (__getattr__ triggered)
print(f"Read missing: {guard.non_existent}")

# Writing attribute (__setattr__ triggered)
guard.key = "API_KEY_2"

# Attempting invalid write (validation catches it)
try:
    guard.key = 12345
except TypeError as e:
    print(f"Caught validation error: {e}")
