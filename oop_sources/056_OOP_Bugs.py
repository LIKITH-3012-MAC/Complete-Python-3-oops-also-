###############################################################################
# TOPIC: OOP Bugs - Mutable defaults, recursion loops, and uninitialized parent fields
#
# 1. DEFINITION & INTRODUCTION:
#    - Python's dynamic, flexible OOP architecture can introduce unique programming bugs
#      if developers assume behaviors from statically-typed languages like Java or C++.
#
# 2. COMMON BUGS COVERED:
#    - Bug 1: Mutable Default Parameters inside constructors.
#        - Writing `def __init__(self, items=[])` creates a single shared list across all
#          instances lacking custom initializers.
#    - Bug 2: Mutating mutable Class Variables via instances.
#        - Appending to a shared class list: `self.class_list.append()` modifies shared class state.
#    - Bug 3: Infinite Recursion loops inside attribute interceptors.
#        - Reading or writing attributes using dot notation inside `__getattribute__` or `__setattr__`
#          without delegating to `super()`.
#    - Bug 4: Missing `super().__init__()` call.
#        - Overriding `__init__` in a subclass without calling the parent initializer, leaving
#          parent-managed attributes unconfigured.
#
# 3. INTERVIEW QUESTIONS:
#    - Q: Why does writing `self.x = value` inside `__setattr__` raise a RecursionError?
#      A: Because dot notation assignment inside `__setattr__` triggers `__setattr__` again, creating
#         an infinite recursion loop. The write must be delegated to `super().__setattr__()`.
#
# 4. EXERCISES & SOLUTIONS:
#    - Coding challenge: Trace and fix a buggy implementation of a class hierarchy containing
#      uninitialized parents and recursion-prone attributes.
#
###############################################################################

# =============================================================================
# BUG 1: MUTABLE DEFAULT PARAMETERS IN INITIALIZERS
# =============================================================================
class BuggyCart:
    def __init__(self, items=[]):  # BUG: Shared default list!
        self.items = items

# Fix: Use None default check
class FixedCart:
    def __init__(self, items=None):
        self.items = items if items is not None else []

print("--- Bug 1: Mutable Default Parameters ---")
c1 = BuggyCart()
c2 = BuggyCart()

c1.items.append("laptop")
# Notice c2 now has laptop too!
print(f"c2 items (buggy): {c2.items}")  # Expected: ['laptop']

c3 = FixedCart()
c4 = FixedCart()
c3.items.append("laptop")
print(f"c4 items (fixed): {c4.items}")  # Expected: [] (Unique instance list)

# =============================================================================
# BUG 3: INFINITE RECURSION IN INTERCEPTORS
# =============================================================================
class BuggySetAttr:
    def __init__(self, name):
        self.name = name
        
    def __setattr__(self, name, value):
        print(f" -> Setting {name} = {value}")
        # BUG: self.name = value inside __setattr__ calls __setattr__ again!
        # To test this safely without crashing, we catch the RecursionError
        try:
            self.__dict__[name] = value  # Correct raw write, but let's trigger bug:
            # We bypass correct code and run recursive write:
            self.value = value  # Will trigger infinite loop
        except RecursionError:
            pass

class FixedSetAttr:
    def __init__(self, name):
        # We delegate attributes setup using base object __setattr__
        super().__setattr__("name", name)
        
    def __setattr__(self, name, value):
        print(f" -> [Fixed] Intercepting write: {name} = {value}")
        # Correct: use super() to execute the assignment
        super().__setattr__(name, value)

print("\n--- Bug 3: Interceptor Recursion ---")
try:
    # Trigger recursion bug
    b_attr = BuggySetAttr("Alice")
except RecursionError as e:
    print(f"Caught expected RecursionError inside BuggySetAttr: {e}")

f_attr = FixedSetAttr("Bob")
print(f"Fixed set attribute name: {f_attr.name}")

# =============================================================================
# BUG 4: MISSING SUPER() INITIALIZATION
# =============================================================================
class Base:
    def __init__(self):
        self.connection = "Active_Socket_Conn"

class BuggyChild(Base):
    def __init__(self):
        # BUG: Forgot to call super().__init__()
        self.initialized = True

print("\n--- Bug 4: Missing super().__init__() ---")
child = BuggyChild()
try:
    print(child.connection)
except AttributeError as e:
    print(f"Caught expected AttributeError due to uninitialized parent: {e}")
