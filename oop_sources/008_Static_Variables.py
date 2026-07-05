###############################################################################
# TOPIC: Static Variables - Java/C++ translations and function-level statics
#
# 1. DEFINITION & TERMINOLOGY TRANSLATION:
#    - Python does not have a `static` keyword for variables.
#    - In Class Scope: What C++ or Java call "Static Member Variables" are translated
#      directly as **Class Variables** in Python (as covered in the Class Variables topic).
#      They are defined in the class body, shared by all instances, and stored in the class
#      `__dict__`.
#    - In Function Scope: In C or C++, you can declare a `static` variable inside a function.
#      Its value persists across successive calls to that function.
#
# 2. IMPLEMENTING FUNCTION-LEVEL STATIC VARIABLES:
#    - Python does not support function-level static declarations natively.
#    - However, since **functions are first-class objects** in Python, they can have custom
#      attributes bound to them.
#    - We can define an attribute on the function object itself (e.g., `func.counter = 0`).
#      This attribute is stored in the function's namespace (`func.__dict__`), persisting
#      across all calls of that function.
#
# 3. OTHER PERSISTENCE PATTERNS:
#    - Using generator state preservation (via yield).
#    - Using default mutable arguments (considered an anti-pattern/bug, but historically
#      used to store call state).
#
# 4. TIME & SPACE COMPLEXITY:
#    - Function attribute read/write: O(1) average lookup in function `__dict__`.
#
# 5. BEST PRACTICES:
#    - For class-level static state, use standard class variables.
#    - For function-level state retention, prefer classes, closures, or generator functions
#      over function attributes, as function attributes can be modified externally, breaking
#      encapsulation.
#
# 6. INTERVIEW QUESTIONS:
#    - Q: Does Python have a `static` keyword for variables?
#      A: No. Class-level static variables are declared simply as class variables. Function-level
#         static variables are not natively supported, but can be emulated using function attributes.
#    - Q: How does a function attribute persist value?
#      A: Since functions are objects in Python, they have their own `__dict__` namespace where
#         arbitrary attributes can be written, keeping state alive between calls.
#
# 7. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a function `get_next_id()` that uses a function attribute
#      to act as a thread-safe incrementing ID generator.
#
###############################################################################

# 1. Class-Level Static Variable Translation
class DatabaseConfig:
    # Functionally equivalent to 'static string connection_string' in Java/C++
    CONNECTION_STRING = "sqlite:///:memory:"

print("--- Class-Level Static Variable ---")
print(f"Read from class directly: {DatabaseConfig.CONNECTION_STRING}")

# 2. Emulating Function-Level Static Variables (Function Attributes)
# We will define a function that counts how many times it has been invoked.
def track_calls():
    # Write to function attribute.
    # We must check if the attribute exists; if not, initialize it.
    if not hasattr(track_calls, "call_counter"):
        track_calls.call_counter = 0
    
    track_calls.call_counter += 1
    print(f"Function track_calls() invoked. Total runs: {track_calls.call_counter}")

print("\n--- Function-Level Static Variable ---")
track_calls()  # Run 1: counter becomes 1
track_calls()  # Run 2: counter becomes 2
track_calls()  # Run 3: counter becomes 3

# Inspecting function namespace
print(f"Function __dict__ namespace: {track_calls.__dict__}")
# Expected: {'call_counter': 3}

# 3. Emulating Function-Level Statics using Decorators
# A cleaner way to initialize function static variables without inline 'hasattr' checks
# is to define a decorator that attaches attributes.
def static_vars(**kwargs):
    def decorate(func):
        for key, val in kwargs.items():
            setattr(func, key, val)
        return func
    return decorate

@static_vars(total_sum=0, call_history=[])
def accumulate_value(x):
    accumulate_value.total_sum += x
    accumulate_value.call_history.append(x)
    return accumulate_value.total_sum

print("\n--- Decorated Function Static Variables ---")
print(f"Sum after adding 10: {accumulate_value(10)}")  # 10
print(f"Sum after adding 20: {accumulate_value(20)}")  # 30
print(f"History tracking:     {accumulate_value.call_history}")  # Expected: [10, 20]
