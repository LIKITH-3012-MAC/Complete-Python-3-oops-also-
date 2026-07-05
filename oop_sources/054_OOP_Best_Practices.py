###############################################################################
# TOPIC: OOP Best Practices - Modular design, clean constructors, and typing guidelines
#
# 1. DEFINITION & INTRODUCTION:
#    - Writing clean, maintainable Python OOP code requires matching Python-specific features
#      with classic software engineering design rules.
#
# 2. KEY BEST PRACTICES:
#    - Clean Constructors (Lean Initializers):
#        - Do NOT perform complex processing, file reading, or network I/O inside `__init__()`.
#        - Initializers should only bind passed values to instance fields (`self.x = x`).
#        - Perform calculations in helper methods or use lazy-loading properties.
#    - Limit Inheritance Depth:
#        - Keep inheritance trees shallow (maximum 2-3 levels). Deep trees make checking MRO
#          and tracing state extremely difficult.
#    - Safe Class Variables:
#        - Never use mutable objects (like lists `[]` or dicts `{}`) as class-level attributes
#        - Use default_factory in dataclasses or initialize lists inside `__init__()`.
#    - Explicit Class method signatures:
#        - Use standard PEP 8 names: `self` for instance methods, `cls` for class methods.
#        - Use type annotations for all method arguments and return types.
#
# 3. INTERVIEW QUESTIONS:
#    - Q: Why is it bad design to perform API queries inside a class constructor `__init__`?
#      A: It couples object instantiation to external network state, making unit testing impossible,
#         slowing down memory allocation, and crashing execution if the network is down during setup.
#
# 4. EXERCISES & SOLUTIONS:
#    - Coding challenge: Refactor a legacy class with a heavy, error-prone constructor into a clean,
#      modular structure utilizing lazy loading properties.
#
###############################################################################

# =============================================================================
# 1. CLEAN CONSTRUCTOR & LAZY LOADING
# =============================================================================
# BAD: Constructor performs heavy file reading (blocking, couples instantiation to filesystem)
class BadConfigLoader:
    def __init__(self, filepath):
        self.filepath = filepath
        print(" -> [Bad] Reading configuration file...")
        with open(filepath, "r") as f:  # Fails if file does not exist during MyClass() instantiation
            self.data = f.read()

# GOOD: Constructor is simple; loading is deferred or explicit
class GoodConfigLoader:
    def __init__(self, filepath):
        self.filepath = filepath
        self._data = None  # Cache backing variable
        
    @property
    def data(self) -> str:
        # Lazy Loading: read file only when attribute is actually accessed
        if self._data is None:
            print(" -> [Good] Lazy loading config file data...")
            import os
            if not os.path.exists(self.filepath):
                # Set default empty string or raise clean error
                self._data = "{}"
            else:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    self._data = f.read()
        return self._data

# Setup temp file
temp_file = "app_config.json"
with open(temp_file, "w") as f: f.write('{"mode": "production"}')

print("--- Testing Constructors ---")
# Instantiation is extremely fast and safe (no I/O runs yet)
loader = GoodConfigLoader(temp_file)

# File read runs only now (on attribute access)
print(f"Loaded config data: {loader.data}")

# Clean up temp file
import os
if os.path.exists(temp_file): os.remove(temp_file)

# =============================================================================
# 2. AVOID MUTABLE CLASS VARIABLES
# =============================================================================
# BAD: Declares list at class level (Shared across instances, leads to data leaks)
class BadRegistry:
    registered_items = []  # Shared mutable list!
    
# GOOD: Declare list inside __init__ (unique to each instance)
class GoodRegistry:
    def __init__(self):
        self.registered_items = []  # Unique instance list
