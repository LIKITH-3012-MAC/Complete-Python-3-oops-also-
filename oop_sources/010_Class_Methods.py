###############################################################################
# TOPIC: Class Methods - @classmethod, cls parameter, and factory constructions
#
# 1. DEFINITION & INTRODUCTION:
#    - Class Methods: Methods bound to the class itself rather than its instances.
#    - Signature: Decorated with `@classmethod`. The first parameter is conventionally named
#      `cls`, representing the class object.
#
# 2. BEHAVIOR & PARAMETER PASSING:
#    - When you call a class method (e.g. `MyClass.method()`), Python automatically passes the
#      class object `MyClass` as the first argument (`cls`).
#    - Calling via Instance: You can also call a class method on an instance: `instance.method()`.
#      Python still passes the class object (type of instance) as the first argument, not the instance.
#
# 3. CORE USE CASES:
#    - Factory Constructors (Alternative Constructors): Parsing varied input formats (CSV, JSON,
#      dict) and returning an initialized object instance (as seen in the Constructors topic).
#    - Accessing/Modifying Class State: Safely reading or writing class variables without hardcoding
#      class names, which supports inheritance patterns cleanly.
#
# 4. INHERITANCE ADVANTAGE:
#    - Class methods support inheritance polymorphically. If a subclass inherits a class method,
#      calling the class method on the subclass passes the subclass type to `cls`, not the parent class!
#      This allows subclass factory methods to instantiate the correct child class type automatically.
#
# 5. BEST PRACTICES:
#    - Use `@classmethod` when the method needs to access class-level attributes, create class
#      instances, or when designing cooperative inheritance factories.
#    - Name the first parameter `cls` (PEP 8 standard).
#
# 6. INTERVIEW QUESTIONS:
#    - Q: How does a class method differ from an instance method?
#      A: An instance method receives the specific object instance as its first argument (`self`),
#         allowing it to access instance-level state. A class method receives the class object
#         itself (`cls`), allowing it to access class-level properties or instantiate instances.
#    - Q: What happens if a subclass calls a class method inherited from a parent class?
#      A: The subclass type is passed as the `cls` argument, allowing dynamic instantiation of
#         the subclass type.
#
# 7. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a parent class with a classmethod factory, inherit it in a
#      subclass, and demonstrate that calling the factory on the subclass instantiates the subclass.
#
###############################################################################

# 1. Class Method and Shared Class State
class Bookstore:
    # Class variable
    total_books_sold = 0
    
    def __init__(self, shop_name):
        self.shop_name = shop_name
        
    @classmethod
    def increment_sales(cls, count):
        # Access and modify class variable via 'cls' parameter
        cls.total_books_sold += count
        print(f" -> Sales incremented on class {cls.__name__}. Global sales: {cls.total_books_sold}")

# Instantiate shops
shop1 = Bookstore("Central Books")
shop2 = Bookstore("Westside Reads")

print("--- Modifying Class State via ClassMethod ---")
# Call class method via Class
Bookstore.increment_sales(5)

# Call class method via Instance
shop1.increment_sales(10)  # Passes Bookstore class object to 'cls'
print(f"Bookstore.total_books_sold: {Bookstore.total_books_sold}")  # Expected: 15

# 2. Inheritance Factory Demonstration
# This is a classic interview question on class method inheritance.
class UserProfile:
    def __init__(self, username):
        self.username = username
        
    @classmethod
    def create_guest(cls):
        # Instantiates the class represented by 'cls' dynamically
        print(f" -> Instantiating class name: {cls.__name__}")
        return cls("Guest_User")

class AdminProfile(UserProfile):
    # Inherits constructor and classmethod from UserProfile
    pass

print("\n--- ClassMethod Factory & Inheritance ---")
# Call factory on Parent
user1 = UserProfile.create_guest()
print(f"Type of user1: {type(user1)}")  # Expected: UserProfile

# Call factory on Subclass
admin1 = AdminProfile.create_guest()
print(f"Type of admin1: {type(admin1)}")  # Expected: AdminProfile (Dynamic type binding!)
