###############################################################################
# TOPIC: OOP Interview Q - High-frequency theory, explanations, and code answers
#
# 1. DEFINITION & INTRODUCTION:
#    - This topic acts as a comprehensive study guide for technical interviews, focusing on
#      internals, architectural choices, and edge cases.
#
# 2. KEY QUESTIONS COVERED:
#    - Q1: How does Python's Method Resolution Order (MRO) handle multiple inheritance diamond shapes?
#      A: It compiles a search list using the C3 Linearization algorithm which guarantees that:
#         1. Subclasses are searched before their parents.
#         2. Definition order (left-to-right) is preserved.
#         3. Monotonicity is maintained.
#    - Q2: Explain the differences between data and non-data descriptors and their lookup priority.
#      A: A data descriptor implements `__set__` or `__delete__` (or both) and takes precedence
#         over the instance's dictionary `__dict__`. A non-data descriptor only implements `__get__`
#         and is overridden by any matching keys in the instance's `__dict__`.
#    - Q3: What is name mangling in Python and why is it used?
#      A: The CPython compiler automatically rewrites any class attribute starting with double
#         underscores (e.g. `__secret` inside class `Bank`) to `_ClassName__attribute`
#         (e.g. `_Bank__secret`) to prevent naming collisions in subclasses.
#
# 3. INTERACTION & EXAMPLES:
#    - The code below implements a mock test checking descriptors and MRO lookups, verifying
#      answers dynamically.
#
###############################################################################

# 1. Demonstrating descriptor lookup precedence (Interview Classic)
class DataDescriptor:
    def __get__(self, instance, owner):
        return "Descriptor_Get_Value"
    def __set__(self, instance, value):
        print(" -> DataDescriptor __set__ executed.")

class NonDataDescriptor:
    def __get__(self, instance, owner):
        return "NonDataDescriptor_Get_Value"

class TestProfile:
    # Bind descriptors
    data_field = DataDescriptor()
    nondata_field = NonDataDescriptor()
    
    def __init__(self):
        # Write keys directly to instance dictionary with same name as descriptors!
        self.__dict__["data_field"] = "Local_Dict_Value_A"
        self.__dict__["nondata_field"] = "Local_Dict_Value_B"

tp = TestProfile()

print("--- Descriptor Precedence test ---")
# Querying data_field: Data Descriptor overrides instance dict!
# Expected: Descriptor_Get_Value (ignores 'Local_Dict_Value_A')
print(f"Data Field lookup:     {tp.data_field}")

# Querying nondata_field: Instance dict overrides Non-Data descriptor!
# Expected: Local_Dict_Value_B (shadows the descriptor)
print(f"Non-Data Field lookup: {tp.nondata_field}")

# 2. Dynamic attribute extraction and type hierarchy verification
print("\n--- Introspection Interview Helpers ---")
# Quick check of class type descriptors
print(f"Is type(type) equal to type? {type(type) is type}")      # Expected: True
print(f"Is type(object) equal to type? {type(object) is type}")  # Expected: True
print(f"Is object type descriptor base? {issubclass(type, object)}")  # Expected: True
