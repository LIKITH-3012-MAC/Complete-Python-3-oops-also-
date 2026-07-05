###############################################################################
# TOPIC: CPython Object Model - PyObject structs, type pointers, and the type-object cycle
#
# 1. DEFINITION & THE PyObject STRUCTURE:
#    - In CPython (the standard reference implementation of Python written in C), everything
#      is an object allocated on the heap.
#    - At the C level, every Python object is represented by a struct that starts with the
#      fields defined by the `PyObject` structure:
#      ```c
#      typedef struct _object {
#          _PyObject_HEAD_EXTRA  // Doubly-linked list for active heap objects tracking
#          Py_ssize_t ob_refcnt; // Reference count (used for memory cleanup/GC)
#          struct _typeobject *ob_type; // Pointer to the type descriptor object
#      } PyObject;
#      ```
#    - If the object has a variable size (like strings, lists, tuples), it is represented by
#      `PyVarObject`, which adds an `ob_size` field.
#
# 2. THE DYNAMIC TYPE-CLASS CYCLE (The Root of Python):
#    - How does Python unify class structures and type structures?
#    - There is a circular dependency at the root of CPython's object model:
#        1. `object` is the base class of all objects, including `type` (`issubclass(type, object) -> True`).
#        2. `type` is the metaclass of all objects, including `object` itself (`isinstance(object, type) -> True`).
#        3. `type` is also its own metaclass! Calling `isinstance(type, type)` returns `True`.
#    - This unification cycle ensures that classes behave as objects, and types behave as classes,
#      creating a clean, unified object model.
#
# 3. INTERVIEW QUESTIONS:
#    - Q: What are the two essential fields present in every CPython object structure?
#      A: `ob_refcnt` (reference count) and `ob_type` (pointer to the type descriptor object).
#    - Q: Explain the circular relationship between `object` and `type` in Python.
#      A: `object` is the base class of all types (including `type`), while `type` is the metaclass
#         responsible for creating all class objects (including `object` and `type` itself).
#
# 4. EXERCISES & SOLUTIONS:
#    - Coding challenge: Write a script that checks the classes, base classes, and metaclasses of
#      `object` and `type` using `isinstance`, `issubclass`, and type calls to prove the cycles.
#
###############################################################################

# 1. Verifying Class and Metaclass Relationships
print("--- Class and Metaclass Checks ---")

# Check type of instances
print(f"Type of 5:       {type(5)}")        # Expected: <class 'int'>
print(f"Type of 'hello': {type('hello')}")  # Expected: <class 'str'>

# Check type of class objects (classes are instances of type)
print(f"Type of int:     {type(int)}")      # Expected: <class 'type'>
print(f"Type of str:     {type(str)}")      # Expected: <class 'type'>

# 2. Proving the type-object cycle
print("\n--- The Type-Object Cycle Proof ---")

# Rule A: object is the ultimate base class of everything
print(f"Is type a subclass of object?     {issubclass(type, object)}")      # Expected: True
print(f"Is int a subclass of object?      {issubclass(int, object)}")       # Expected: True

# Rule B: type is the metaclass of everything
print(f"Is object an instance of type?    {isinstance(object, type)}")     # Expected: True
print(f"Is int an instance of type?       {isinstance(int, type)}")        # Expected: True

# Rule C: type is an instance of itself (Metaclass cycle)
print(f"Is type an instance of type?      {isinstance(type, type)}")        # Expected: True
print(f"Is object an instance of object?  {isinstance(object, object)}")    # Expected: True

# 3. Traversing type chains
class CustomClass:
    pass

c_obj = CustomClass()

print("\n--- Custom Class type Chain lookup ---")
print(f"c_obj type:         {c_obj.__class__}")      # Expected: CustomClass
print(f"CustomClass type:   {CustomClass.__class__}")  # Expected: type
print(f"type type:          {type.__class__}")        # Expected: type (Self-referential loop terminates)
