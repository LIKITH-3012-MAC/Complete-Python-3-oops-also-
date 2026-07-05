###############################################################################
# TOPIC: Self vs cls - Semantic differences, memory bindings, and parameters rules
#
# 1. DEFINITION & COMPARISON:
#    - `self`: Represents the specific instance of the class. It is the target receiver
#      parameter for instance methods, granting access to instance-level attributes and state.
#    - `cls`: Represents the class object itself (the type structure). It is the target
#      receiver parameter for class methods, granting access to class-level attributes,
#      class methods, and the class constructor.
#
# 2. DETAILED COMPARISON TABLE:
#    -------------------------------------------------------------------------------------
#    Feature            | `self`                               | `cls`
#    -------------------------------------------------------------------------------------
#    Concept            | Instance Object                      | Class Object
#    Method Context     | Instance Methods                     | Class Methods
#    CPython target     | PyObject (instance struct on heap)   | PyTypeObject (type descriptor)
#    Primary usage      | Access/Modify instance properties    | Factory constructors, Class vars
#    Python Keyword?    | No (just standard parameter name)    | No (just standard parameter name)
#    -------------------------------------------------------------------------------------
#
# 3. THE "ANY NAME" RULE:
#    - Neither `self` nor `cls` are reserved keywords in Python. They are simple positional
#      arguments.
#    - You can write a class method using `this` instead of `self`, or `clazz` instead of `cls`,
#      and the code will compile and execute identically.
#    - However, doing so violates PEP 8 standards, makes code unreadable, and breaks syntax
#      highlighting or auto-completion in standard IDEs.
#
# 4. INTERVIEW QUESTIONS:
#    - Q: Are `self` and `cls` keywords in Python?
#      A: No, they are standard parameter names. Python passes the instance or class object
#         as the first argument positionally; the name used to capture it can be anything.
#    - Q: What happens if you call a classmethod via an instance: `instance.my_classmethod()`?
#      A: The class object (`type(instance)`) is still bound to the first argument `cls`,
#         not the instance itself.
#
# 5. EXERCISES & SOLUTIONS:
#    - Coding challenge: Create a class using non-standard parameter names (like `myself` and
#      `myclass`) to prove the parameter binding mechanics, then rewrite it conforming to PEP 8.
#
###############################################################################

# 1. Demonstrating parameter binding using non-standard names
# (Highly discouraged in production, shown to prove compiler rules)
class NonStandardParamDemo:
    class_name = "NonStandardClass"
    
    # We use 'myself' instead of 'self'
    def __init__(myself, value):
        myself.value = value  # binds to instance
        
    # We use 'myself' instead of 'self'
    def get_value(myself):
        return myself.value
        
    # We use 'myclass' instead of 'cls'
    @classmethod
    def get_class_name(myclass):
        return myclass.class_name

# Test instantiation and execution
instance = NonStandardParamDemo(42)
print("--- Non-Standard Parameters Execution ---")
print(f"Instance Value: {instance.get_value()}")  # Expected: 42
print(f"Class Name:     {NonStandardParamDemo.get_class_name()}")  # Expected: "NonStandardClass"

# 2. Conforming to PEP 8 (Standard self vs cls)
# Below is the clean, standard implementation of the same functionality.
class StandardParamDemo:
    class_name = "StandardClass"
    
    def __init__(self, value):
        self.value = value
        
    def get_value(self):
        return self.value
        
    @classmethod
    def get_class_name(cls):
        return cls.class_name

print("\n--- Standard (PEP 8) Parameters Execution ---")
std_inst = StandardParamDemo(100)
print(f"Instance Value: {std_inst.get_value()}")
print(f"Class Name:     {StandardParamDemo.get_class_name()}")

# 3. Object ID comparison of self and cls
class IdentityTracker:
    @classmethod
    def track_class(cls):
        print(f"cls ID:  {id(cls)}")
        
    def track_instance(self):
        print(f"self ID: {id(self)}")

it = IdentityTracker()
print("\n--- Memory Address Identity Tracker ---")
print(f"IdentityTracker Class ID: {id(IdentityTracker)}")
it.track_class()  # cls ID should match class ID exactly

print(f"Instance 'it' ID:         {id(it)}")
it.track_instance()  # self ID should match instance ID exactly
