###############################################################################
# TOPIC: Single Inheritance - constructor delegation, super(), and method overrides
#
# 1. DEFINITION & INTRODUCTION:
#    - Single Inheritance: A subclass inherits attributes and behaviors from exactly
#      one parent class.
#    - This is the simplest and most common form of inheritance.
#
# 2. CONSTRUCTOR DELEGATION & super():
#    - When a subclass defines its own `__init__()` method, it overrides the parent's
#      `__init__()`.
#    - If you want the parent class attributes to be configured correctly on the subclass
#      instance, you must explicitly call the parent's initializer from within the child's
#      initializer.
#    - In Python, we do this using the `super()` function:
#      `super().__init__(arg1, arg2)`
#      This dynamically locates the parent class in the MRO and executes its constructor.
#
# 3. METHOD OVERRIDING:
#    - Subclasses can redefine parent methods to customize behavior.
#    - If the child wants to extend the parent's method rather than completely replace it,
#      it can call the parent's method internally:
#      `super().parent_method()`
#
# 4. BEST PRACTICES:
#    - Always call `super().__init__()` at the very beginning of the child class initializer
#      to ensure the parent class is initialized before setting subclass-specific properties.
#
# 5. INTERVIEW QUESTIONS:
#    - Q: What happens if a subclass overrides `__init__` but does not call `super().__init__()`?
#      A: The parent's initializer will not run, meaning any attributes configured by the parent
#         class (e.g. `self.name`) will not be created on the child instance, leading to
#         `AttributeError` exceptions when accessed.
#    - Q: Why is `super()` preferred over hardcoding parent class names (e.g. `Parent.__init__(self)`)?
#      A: `super()` is dynamic; it resolves the parent according to the MRO at runtime. This prevents
#         bugs in complex multiple inheritance hierarchies and maintains maintenance flexibility.
#
# 6. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a `Person` class (name, age), inherit it in a `Student` class
#      (name, age, student_id), delegate instantiation via `super()`, and override description methods.
#
###############################################################################

# 1. Parent Class
class Employee:
    def __init__(self, name, base_salary):
        self.name = name
        self.base_salary = base_salary
        
    def get_details(self):
        return f"Employee: {self.name} | Base Salary: ${self.base_salary}"

# 2. Child Class (Single Inheritance)
class Manager(Employee):
    def __init__(self, name, base_salary, bonus):
        # Delegate constructor allocation and attribute setup to parent
        super().__init__(name, base_salary)
        self.bonus = bonus  # Set manager-specific attribute
        
    # Override get_details method
    def get_details(self):
        # We can call the parent's method using super() to reuse code
        parent_details = super().get_details()
        return f"{parent_details} | Bonus: ${self.bonus} | Total: ${self.base_salary + self.bonus}"

print("--- Single Inheritance Execution ---")
# Instantiate parent
emp = Employee("Bob", 50000)
print(emp.get_details())

# Instantiate child
mgr = Manager("Alice", 80000, 15000)
print(mgr.get_details())  # Runs overridden method

# Verify types
print(f"\nIs mgr an Employee? {isinstance(mgr, Employee)}")  # Expected: True
print(f"Is emp a Manager?  {isinstance(emp, Manager)}")   # Expected: False
