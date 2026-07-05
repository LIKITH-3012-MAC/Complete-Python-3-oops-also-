###############################################################################
# TOPIC: Classes - blueprints, Namespaces, and mappingproxy Internals
#
# 1. DEFINITION & INTRODUCTION:
#    - Class: A user-defined prototype or blueprint from which objects are created.
#      It defines a set of attributes and methods that characterize any object of the class.
#    - Syntax: `class ClassName:`
#
# 2. CLASS COMPILATION & NAMESPACE MECHANICS:
#    - How does CPython build a class at runtime?
#    - When Python encounters a `class` statement:
#        1. The compiler creates a new dictionary namespace.
#        2. It executes the entire body of the class (variables, function definitions)
#           sequentially inside this dictionary context.
#        3. Once execution completes, the class object is constructed by calling the metaclass
#           (usually `type`) with three arguments:
#           `ClassName = type(name, bases, namespace_dict)`
#        4. The namespace dictionary is converted into a read-only dictionary proxy object
#           (`mappingproxy`) accessible via `ClassName.__dict__`.
#
# 3. CLASS ATTRIBUTES:
#    - Attributes defined directly inside the class body (outside any method block) are Class
#      Attributes. They are shared across all instances of the class.
#    - Memory: Stored exactly once in the class namespace dictionary.
#
# 4. BEST PRACTICES:
#    - Use PascalCase naming convention for class names (PEP 8).
#    - Initialize all instance-specific variables inside the constructor (`__init__`), not
#      directly in the class body.
#
# 5. INTERVIEW QUESTIONS:
#    - Q: What type is `ClassName.__dict__` and why can't you modify it directly?
#      A: It is a `mappingproxy` object. Python exposes it as read-only to optimize lookup speeds
#         and prevent accidental damage to the class lookup tables during execution.
#    - Q: How does Python execute a class declaration block?
#      A: It executes the class body as a standard sequence of statements inside a temporary
#         dictionary namespace, then passes this namespace to `type()` to instantiate the class object.
#
# 6. EXERCISES & SOLUTIONS:
#    - Coding challenge: Dynamically inspect class attributes, examine `ClassName.__dict__`, and
#      attempt class attribute modification using both `setattr` and direct assignments.
#
###############################################################################

import types  # Standard module to inspect types (like mappingproxy)

# 1. Defining a Class
class Employee:
    # Class attributes (shared by all employees)
    COMPANY_NAME = "TechCorp"
    TOTAL_EMPLOYEES = 0
    
    def __init__(self, name):
        self.name = name  # Instance attribute (unique to each employee)

# 2. Class Namespace Inspection (__dict__)
# Class __dict__ returns a mappingproxy, a read-only dictionary.
print("--- Class Namespace (Employee.__dict__) ---")
print(f"Type of Employee.__dict__: {type(Employee.__dict__)}")
# Print keys present in class dictionary
print(f"Class keys: {list(Employee.__dict__.keys())}")

# 3. Modifying Class Attribute
# Direct modification on mappingproxy is blocked
try:
    Employee.__dict__["COMPANY_NAME"] = "NewCorp"
except TypeError as e:
    print(f"\nCaught expected TypeError (direct mappingproxy edit): {e}")

# Correct way to modify class attributes:
# Via class assignment
Employee.COMPANY_NAME = "GiganticCorp"
print(f"Updated Company (assignment): {Employee.COMPANY_NAME}")

# Via setattr() built-in
setattr(Employee, "COMPANY_NAME", "MegaCorp")
print(f"Updated Company (setattr):    {Employee.COMPANY_NAME}")

# 4. Creating Class Dynamically (Metaclass type instantiation)
# We can dynamically create a class without using the 'class' keyword!
# type(name, bases, dict)
dynamic_class_dict = {
    "DATA_SOURCE": "SQL_DB",
    "fetch_data": lambda self: "Query results from dynamic class"
}

# Dynamically construct a class named 'DatabaseConnector'
DatabaseConnector = type("DatabaseConnector", (object,), dynamic_class_dict)

# Instantiate and run
db_instance = DatabaseConnector()
print("\n--- Dynamic Class Execution ---")
print(f"Class Name: {DatabaseConnector.__name__}")
print(f"Attribute DATA_SOURCE: {db_instance.DATA_SOURCE}")
print(f"Calling fetch_data(): {db_instance.fetch_data()}")
