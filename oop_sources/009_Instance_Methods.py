###############################################################################
# TOPIC: Instance Methods - Bound methods, self parameters, and method resolutions
#
# 1. DEFINITION & INTRODUCTION:
#    - Instance Methods: Functions defined inside a class body that act on individual
#      instances of that class.
#    - Signature: The first parameter of an instance method is always `self`, which represents
#      the active object instance calling the method.
#
# 2. BOUND METHODS VS UNBOUND FUNCTIONS (CPython Internals):
#    - How does Python pass the instance parameter implicitly?
#    - At compile-time, an instance method is just a standard function object defined inside
#      the class dictionary (`Employee.work` is a `<class 'function'>`).
#    - When you access the method via an instance (e.g. `emp.work`), Python's attribute lookup
#      interceptor (the descriptor protocol on functions) triggers.
#    - It wraps the raw function object and the instance pointer together, returning a new
#      temporary object: a **Bound Method** object (`<class 'method'>`).
#    - When the bound method is called (e.g., `emp.work()`), it automatically inserts the wrapped
#      instance pointer as the first argument (`self`), executing the underlying function.
#    - Calling via Class Name: You can call instance methods using the class name directly, but
#      you must pass the instance reference explicitly: `Employee.work(emp)`. In this context,
#      no bound method is created; it resolves as a direct call to the raw function.
#
# 3. TIME & SPACE COMPLEXITY:
#    - Method resolution and bound method creation: O(1) time complexity.
#
# 4. BEST PRACTICES:
#    - Always name the first parameter `self` (PEP 8 standard, not a keyword but a strong convention).
#    - Avoid calling instance methods using the class name in production code; use the standard
#      instance receiver syntax (`instance.method()`).
#
# 5. INTERVIEW QUESTIONS:
#    - Q: What is a "bound method" in Python?
#      A: An object that wraps a raw function and an instance reference together, allowing the
#         function to be called with the instance implicitly passed as the first argument (`self`).
#    - Q: What is the output of: `print(type(MyClass.method))` vs `print(type(instance.method))`?
#      A: `MyClass.method` returns `<class 'function'>` (unbound function object).
#         `instance.method` returns `<class 'method'>` (bound method object).
#
# 6. EXERCISES & SOLUTIONS:
#    - Coding challenge: Prove the bound method mechanism by checking identities, comparing
#      direct function call methods, and inspecting method attributes `__self__` and `__func__`.
#
###############################################################################

class Account:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance
        
    def deposit(self, amount):
        # Instance method accessing/mutating instance state
        self.balance += amount
        print(f"Deposited {amount} to {self.owner}'s account. New Balance: {self.balance}")
        return self.balance

# Create instance
acc = Account("Alice", 1000)

print("--- Method Objects Verification ---")
# 1. Unbound Function lookup via Class
class_func = Account.deposit
print(f"Account.deposit type: {type(class_func)}")  # Expected: <class 'function'>

# 2. Bound Method lookup via Instance
bound_method = acc.deposit
print(f"acc.deposit type:     {type(bound_method)}")  # Expected: <class 'method'>

# 3. Inspecting Bound Method Attributes
# A bound method object has special read-only attributes:
# __self__ points to the instance it is bound to
# __func__ points to the underlying raw function object defined in the class
print(f"bound_method.__self__ matches acc? {bound_method.__self__ is acc}")  # Expected: True
print(f"bound_method.__func__ matches Account.deposit? {bound_method.__func__ is Account.deposit}")  # Expected: True

# 4. Calling Bound Method vs Unbound Function
print("\n--- Method Invocations ---")
# Standard execution (implicit self passing)
bound_method(500)  # Expected: Deposits 500, balance becomes 1500

# Class-level execution (explicit self passing)
# Account.deposit(acc, 200) behaves identically to acc.deposit(200)
new_balance = Account.deposit(acc, 200)
print(f"Final Balance after class-level call: {new_balance}")  # Expected: 1700
