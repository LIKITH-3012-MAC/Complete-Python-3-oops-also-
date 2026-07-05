###############################################################################
# TOPIC: Closures - State Capture, Enclosing Scopes, and CPython cell Objects
#
# 1. DEFINITION & INTRODUCTION:
#    - Closure: A record storing a nested function along with an environment: a mapping
#      associating each free variable of the function with the value or storage cell it referenced
#      in the enclosing outer scope at definition time.
#    - Requirements for a closure:
#        1. Must have a nested function.
#        2. The nested function must reference a variable from the enclosing outer scope.
#        3. The enclosing function must return the nested function object.
#    - Closures allow a function to retain access to its defining environment even when called
#      outside its original outer scope.
#
# 2. CPYTHON IMPLEMENTATION & CELL OBJECTS:
#    - How does CPython keep enclosing variables alive after the outer function frame is popped?
#    - When CPython detects that an inner function references a variable in the outer scope
#      (a "free variable"), it does not allocate that variable directly on the stack frame.
#    - Instead, CPython wraps the variable inside a special heap-allocated object called a
#      `cell` object.
#    - Both the outer and inner functions store pointers to this `cell` object.
#    - When the outer function exits and its frame is destroyed, the cell object remains alive
#      on the heap because the inner function still holds a reference to it.
#    - You can inspect the cell references of a closure via the `__closure__` attribute, which
#      contains a tuple of cell objects. The value inside is accessed via `cell.cell_contents`.
#
# 3. STATE MODIFICATION & NONLOCAL:
#    - By default, inner functions can read outer variables but cannot modify them.
#      Attempting to assign `x = new_value` creates a local variable instead.
#    - To modify the cell value directly, use the `nonlocal` keyword.
#
# 4. TIME & SPACE COMPLEXITY:
#    - Closure creation: Small overhead of allocating cell objects and returning the function object.
#    - Closure lookup: Slightly slower than local variable access (`LOAD_DEREF` vs `LOAD_FAST`)
#      but faster than global lookups.
#
# 5. BEST PRACTICES:
#    - Use closures to implement lightweight state trackers or callbacks instead of writing full
#      classes with a single method, reducing class definition boilerplate.
#
# 6. INTERVIEW QUESTIONS:
#    - Q: Where does a closure store the variables it captures?
#      A: In the function object's `__closure__` attribute, which is a tuple containing CPython
#         heap-allocated `cell` objects.
#    - Q: What happens if you try to mutate a captured integer in a closure without `nonlocal`?
#      A: It raises an `UnboundLocalError` (if you read it before writing) or creates a new
#         local variable, shadowing the outer variable.
#
# 7. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a stateful counter closure that has increment, decrement,
#      and reset behaviors, returning a dict of dispatchers.
#
###############################################################################

# 1. Basic Closure and State Capture
def make_multiplier(factor):
    # 'factor' is an enclosing scope variable
    def multiply(number):
        # 'multiply' references 'factor' (free variable)
        return number * factor
    return multiply

double_func = make_multiplier(2)
triple_func = make_multiplier(3)

print("--- Closure Executions ---")
print(f"double_func(10) = {double_func(10)}")  # Expected: 20
print(f"triple_func(10) = {triple_func(10)}")  # Expected: 30

# 2. Inspecting CPython Closure Internals
# Let's inspect the __closure__ attribute of our function object.
print("\n--- Inspecting __closure__ Internals ---")
print(f"double_func.__closure__: {double_func.__closure__}")
# Expected: A tuple containing a cell object

if double_func.__closure__:
    # Access the captured content inside the cell
    captured_cell = double_func.__closure__[0]
    print(f"Captured Cell Object: {captured_cell}")
    print(f"Captured Value (cell_contents): {captured_cell.cell_contents}")  # Expected: 2

# 3. Stateful Closure using nonlocal
# Create a running average calculator
def make_averager():
    # Enclosing state
    total = 0.0
    count = 0
    
    def averager(new_value):
        # Declare nonlocal to modify outer float/int cells
        nonlocal total, count
        total += new_value
        count += 1
        return total / count
        
    return averager

avg = make_averager()
print("\n--- Stateful Closure (Averager) ---")
print(f"Average after adding 10: {avg(10)}")  # 10 / 1 = 10.0
print(f"Average after adding 20: {avg(20)}")  # (10 + 20) / 2 = 15.0
print(f"Average after adding 30: {avg(30)}")  # (30 + 30) / 3 = 20.0

# 4. Challenge: Stateful Closure with Multi-behavior Dispatcher
# A stateful counter with dynamic operations.
def make_counter(start_val=0):
    current = start_val
    
    def increment():
        nonlocal current
        current += 1
        return current
        
    def decrement():
        nonlocal current
        current -= 1
        return current
        
    def get_value():
        return current
        
    # Return a dictionary of callables (dispatcher pattern)
    return {
        "inc": increment,
        "dec": decrement,
        "get": get_value
    }

counter = make_counter(100)
print("\n--- Dispatcher Closure ---")
print(f"Current counter:   {counter['get']()}")  # 100
print(f"After increment:   {counter['inc']()}")  # 101
print(f"After decrement:   {counter['dec']()}")  # 100
print(f"Captured closure cell contents: {counter['inc'].__closure__[0].cell_contents}")  # Inspect cell
