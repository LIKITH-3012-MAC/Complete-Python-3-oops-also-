###############################################################################
# TOPIC: OOP Master Cheat Sheet - Magic methods tables, syntax models, and reference guides
#
# 1. DEFINITION & INTRODUCTION:
#    - This notebook cell acts as a fast-reference cheat sheet for all things Python OOP.
#    - Features:
#        - Dunder Methods Quick Reference table.
#        - Decorator syntax cheat sheet.
#        - Access Modifiers naming rules.
#        - Memory models comparison summary.
#
# 2. DUNDER METHODS REFERENCE TABLE:
#    -------------------------------------------------------------------------------------
#    Dunder Method        | Invoked By                         | Purpose
#    -------------------------------------------------------------------------------------
#    `__new__(cls)`       | Class instantiation `MyClass()`    | Allocates memory for object.
#    `__init__(self)`     | Class instantiation `MyClass()`    | Initializes instance state.
#    `__del__(self)`      | Ref count reaches 0                | Destructor, finalizes object.
#    `__str__(self)`      | `str(obj)` / `print(obj)`          | User-friendly representation.
#    `__repr__(self)`     | `repr(obj)` / interactive prompt   | Unambiguous developer string.
#    `__call__(self)`     | Calling instance `obj()`           | Makes instance callable.
#    `__len__(self)`      | `len(obj)`                         | Emulates container size.
#    `__contains__(self)` | `item in obj`                      | Emulates membership check.
#    `__getitem__(self)`  | `obj[key]` / `obj[1:5]`            | Emulates indexing/slicing reads.
#    `__setitem__(self)`  | `obj[key] = val`                   | Emulates indexing/slicing writes.
#    `__getattr__(self)`  | Missing attribute lookup fallback  | Handles missing fields.
#    `__getattribute__`   | Unconditional attribute access     | Intercepts all field reads.
#    `__setattr__(self)`  | Attribute write assignment         | Intercepts all field writes.
#    `__hash__(self)`     | `hash(obj)` / Set / Dict keys      | Returns hash signature.
#    -------------------------------------------------------------------------------------
#
# 3. INTERACTION & CODE EXAMPLES:
#    - The code below features quick demonstrations of key cheat sheet syntaxes.
#
###############################################################################

# Quick Syntax Demonstrations:

# 1. Access Modifiers Naming reference:
class NamingReferenceClass:
    def __init__(self):
        self.public_var = "Anyone can read me."
        self._protected_var = "Convention says: please treat me as internal."
        self.__private_var = "Name mangling will rewrite me to include class name prefix."

# 2. Decorators Syntax Reference:
class DecoratorsReferenceClass:
    class_var = "Class State"
    
    def __init__(self, value):
        self._val = value
        
    def instance_method(self):
        return f"Instance Method has self. val: {self._val}"
        
    @classmethod
    def class_method(cls):
        return f"Class Method has cls. class_var: {cls.class_var}"
        
    @staticmethod
    def static_method():
        return "Static Method has no self or cls arguments."
        
    @property
    def val(self):
        return self._val
        
    @val.setter
    def val(self, new_val):
        self._val = new_val

print("--- Cheat Sheet Syntax Test ---")
ref_obj = DecoratorsReferenceClass(42)

# Verify methods run
print(ref_obj.instance_method())
print(DecoratorsReferenceClass.class_method())
print(DecoratorsReferenceClass.static_method())
print(f"Property get: {ref_obj.val}")
ref_obj.val = 84
print(f"Property set updated: {ref_obj.val}")

# Naming checks
names_obj = NamingReferenceClass()
print("\n--- Access Namespaces dictionary ---")
print(names_obj.__dict__)
# Expected: {'public_var': ..., '_protected_var': ..., '_NamingReferenceClass__private_var': ...}
