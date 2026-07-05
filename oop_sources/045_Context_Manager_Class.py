###############################################################################
# TOPIC: Class-Based Context Managers - __enter__/__exit__, exception hooks, and rollbacks
#
# 1. DEFINITION & INTRODUCTION:
#    - To create a custom context manager class, the class must implement the context manager
#      protocol: `__enter__(self)` and `__exit__(self, exc_type, exc_val, exc_tb)`.
#
# 2. MAGIC METHODS SIGNATURES:
#    - `__enter__(self)`:
#        - Prepares the resource.
#        - Returns the resource (or the context manager instance itself) to be bound to the
#          variable in the `as` clause.
#    - `__exit__(self, exc_type, exc_val, exc_tb)`:
#        - Handles cleanup actions.
#        - Arguments (all are `None` if the `with` block exits successfully without errors):
#            - `exc_type`: The class type of the raised exception (e.g. `<class 'ValueError'>`).
#            - `exc_val`: The actual exception object instance (e.g. `ValueError("error msg")`).
#            - `exc_tb`: The traceback object containing stack call records.
#        - Return value (Exception Suppression):
#            - If `__exit__` returns `True`, Python swallows the exception and continues execution.
#            - If it returns `False` or `None`, the exception is raised and propagates up the call stack.
#
# 3. BEST PRACTICES:
#    - Do not suppress exceptions indiscriminately by always returning `True`. Only suppress
#      errors you have explicitly handled, logged, or resolved.
#
# 4. INTERVIEW QUESTIONS:
#    - Q: What are the three parameters of the `__exit__` method?
#      A: `exc_type` (exception class), `exc_val` (exception instance), and `exc_tb` (traceback object).
#    - Q: How do you tell the interpreter to suppress an exception raised inside a `with` block?
#      A: By returning `True` from the `__exit__` method.
#
# 5. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a `DatabaseConnector` class-based context manager. If an error
#      occurs inside the `with` block, rollback changes and suppress database-specific exceptions.
#
###############################################################################

# 1. Class-Based Context Manager
class LockManager:
    def __init__(self, resource_name):
        self.resource = resource_name
        self.locked = False
        
    def __enter__(self):
        # Setup: acquire the lock
        print(f" -> [__enter__] Acquiring lock for resource: {self.resource}")
        self.locked = True
        return self  # Return self to let client inspect lock state
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Teardown: release lock
        print(f" -> [__exit__] Releasing lock for resource: {self.resource}")
        self.locked = False
        
        # Check if an exception occurred inside the with block
        if exc_type is not None:
            print(f" -> [__exit__] Caught error in with block: {exc_val}")
            # Decide whether to suppress
            if issubclass(exc_type, KeyError):
                print(" -> [__exit__] KeyError is recoverable. Suppressing error!")
                return True  # returning True swallows the exception
            print(" -> [__exit__] Critical error. Propagating exception...")
            return False  # returning False lets the exception propagate
            
        print(" -> [__exit__] Block completed with no exceptions.")
        return None  # Defaults to False, no suppression needed

# 2. Test Cases
print("--- Case A: Normal Execution ---")
with LockManager("PaymentAPI") as lock:
    print(f"  Inside with: Is lock active? {lock.locked}")
print("Outside with block.")

print("\n--- Case B: Recoverable Exception (KeyError) ---")
with LockManager("UserDB") as lock:
    print("  Attempting operation that triggers KeyError...")
    # Raising KeyError should trigger suppression in __exit__
    raise KeyError("User record not found")
print("Execution resumes safely here because KeyError was swallowed.")

print("\n--- Case C: Critical Exception (ValueError) ---")
try:
    with LockManager("FileConfig") as lock:
        print("  Attempting operation that triggers ValueError...")
        # Raising ValueError should NOT be suppressed
        raise ValueError("Invalid configuration data")
except ValueError as e:
    print(f"Caught critical error outside with block: {e}")
