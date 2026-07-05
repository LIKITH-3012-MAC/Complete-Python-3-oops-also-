###############################################################################
# TOPIC: Instance Variables - Declaration, instance __dict__ maps, and memory allocation
#
# 1. DEFINITION & INTRODUCTION:
#    - Instance Variables: Variables owned by a specific object instance. The state of these
#      variables is unique to each object; changing the value of an instance variable on one
#      object does not affect other instances of the same class.
#    - Declaration: Usually initialized inside the class initializer (`__init__`) by binding
#      them to the `self` parameter (e.g., `self.attribute_name = value`).
#
# 2. INTERNAL MECHANICS & OBJECT NAMESPACE:
#    - Instance variables are stored in the object's instance dictionary `self.__dict__`.
#    - When you access `obj.attribute`, CPython first checks `obj.__dict__` for the key `"attribute"`.
#      If found, it returns the value.
#    - If it is not found, Python falls back to searching the class's dictionary and its parents
#      (using the Method Resolution Order).
#
# 3. MEMORY IMPLICATIONS:
#    - Every instance object allocates its own `__dict__` table.
#    - If a class has hundreds of instances, each holding many instance variables, this can lead
#      to significant memory overhead due to duplicate key name allocations and sparse hash table
#      structures.
#    - PEP 412 (Key-Sharing Dictionary) mitigates this by sharing the keys mapping in the class,
#      but the values remain unique to each instance's memory block.
#
# 4. BEST PRACTICES:
#    - Initialize all expected instance variables inside `__init__` to ensure a consistent interface
#      and help IDE auto-completion.
#    - Do not dynamically create instance variables outside of class methods unless explicitly
#      required by the design pattern.
#
# 5. INTERVIEW QUESTIONS:
#    - Q: Where are instance variables stored?
#      A: In the object instance's internal dictionary: `instance.__dict__`.
#    - Q: What happens if you define a variable with the same name as both an instance variable
#         and a class variable?
#      A: The instance variable shadows the class variable during lookup. Python searches the
#         instance `__dict__` first, matching the instance variable immediately.
#
# 6. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a class where instance variables are updated dynamically,
#      and print `instance.__dict__` at each step to trace attribute lifecycle.
#
###############################################################################

class Student:
    def __init__(self, name, grade):
        # Declaring instance variables using self.
        self.name = name
        self.grade = grade

# 1. Instantiation and Unique State
s1 = Student("Alice", "A")
s2 = Student("Bob", "B")

print("--- Unique Instance State ---")
print(f"Student 1: name={s1.name}, grade={s1.grade}")
print(f"Student 2: name={s2.name}, grade={s2.grade}")

# Mutating s1's instance variable does not affect s2
s1.grade = "A+"
print(f"\nAfter mutating s1's grade:")
print(f"Student 1 grade: {s1.grade}")  # Expected: 'A+'
print(f"Student 2 grade: {s2.grade}")  # Expected: 'B' (Unchanged)

# 2. Inspecting Instance __dict__ Namespaces
# Notice that each instance has its own dict object.
print("\n--- Instance Dict Mapping ---")
print(f"s1.__dict__: {s1.__dict__}")  # Expected: {'name': 'Alice', 'grade': 'A+'}
print(f"s2.__dict__: {s2.__dict__}")  # Expected: {'name': 'Bob', 'grade': 'B'}
print(f"Are dict objects the same? {s1.__dict__ is s2.__dict__}")  # Expected: False

# 3. Dynamic Instance Attribute Addition (Monkey patching)
# We can add an instance variable to s1 only.
s1.scholarship = True
print(f"\ns1.__dict__ after dynamic addition: {s1.__dict__}")
# Expected: contains 'scholarship': True

# Checking if s2 has it (will raise AttributeError)
try:
    print(s2.scholarship)
except AttributeError as e:
    print(f"s2 has no scholarship attribute: {e}")

# 4. Shadowing Class Variable
# Let's define a class with a class attribute and show how instance variable shadows it.
class Config:
    theme = "Light Mode"  # Class variable

c1 = Config()
c2 = Config()

print("\n--- Class Attribute Shadowing ---")
print(f"Initial: c1.theme='{c1.theme}' | c2.theme='{c2.theme}'")

# Create an instance variable with the same name on c1
c1.theme = "Dark Mode"  # Shadowing occurs!
print(f"After shadow: c1.theme='{c1.theme}' (instance) | c2.theme='{c2.theme}' (class default)")
print(f"c1.__dict__: {c1.__dict__}")  # Expected: {'theme': 'Dark Mode'}
print(f"c2.__dict__: {c2.__dict__}")  # Expected: {} (Empty, falls back to class Config.theme)
