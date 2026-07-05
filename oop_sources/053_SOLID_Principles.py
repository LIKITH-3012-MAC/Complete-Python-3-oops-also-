###############################################################################
# TOPIC: SOLID Principles - SRP, OCP, LSP, ISP, and DIP design structures
#
# 1. DEFINITION & INTRODUCTION:
#    - SOLID: Five design principles for writing understandable, flexible, and maintainable
#      object-oriented software.
#
# 2. THE FIVE PRINCIPLES DEFINED:
#    - Single Responsibility Principle (SRP): A class should have only one reason to change.
#      It should perform exactly one task or encapsulate one module of functionality.
#    - Open/Closed Principle (OCP): Classes should be open for extension but closed for modification.
#      You should extend class behaviors (via subclasses/polymorphism) without altering the source code
#      of the original class.
#    - Liskov Substitution Principle (LSP): Subclasses must be completely substitutable for their
#      base classes without breaking execution contracts.
#    - Interface Segregation Principle (ISP): Clients should not be forced to depend on methods they
#      do not use. Python emulates this by keeping abstract interfaces small and modular (using Mixins or Protocols).
#    - Dependency Inversion Principle (DIP): High-level modules should not depend on low-level modules.
#      Both should depend on abstractions (interfaces), not concrete implementations.
#
# 3. INTERVIEW QUESTIONS:
#    - Q: Give a bad vs good code scenario illustrating the Open/Closed Principle.
#      A: Bad: A calculator function with a series of `if type == 'add':` checks. Adding a new operator
#         requires modifying the calculator source code.
#         Good: Calculator takes abstract `Operator` objects. Adding new operations simply involves subclassing
#         `Operator` without touching the calculator code.
#
# 4. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a database saver class violating DIP, and refactor it conforming to DIP.
#
###############################################################################

import abc  # Standard module for interface definitions

# =============================================================================
# 1. SRP: SINGLE RESPONSIBILITY PRINCIPLE
# =============================================================================
# BAD: Class handles user data AND file writing operations (two reasons to change)
class BadUser:
    def __init__(self, name):
        self.name = name
    def save_to_file(self):
        with open("user.txt", "w") as f:
            f.write(self.name)

# GOOD: Split roles into domain class and persistence class
class GoodUser:
    def __init__(self, name):
        self.name = name

class UserFileStorage:
    @staticmethod
    def save(user: GoodUser):
        with open("user.txt", "w") as f:
            f.write(user.name)

# =============================================================================
# 2. OCP: OPEN/CLOSED PRINCIPLE
# =============================================================================
# GOOD: Open for extension (subclasses), closed for modification
class OrderDiscount(abc.ABC):
    @abc.abstractmethod
    def calculate(self, total) -> float:
        pass

# Adding new discount types requires creating new classes (No modification to core code!)
class RegularDiscount(OrderDiscount):
    def calculate(self, total): return total * 0.05

class VIPDiscount(OrderDiscount):
    def calculate(self, total): return total * 0.20

class OrderProcessor:
    def calculate_final(self, total, discount: OrderDiscount):
        # Closed for modification: does not need IF/ELSE chains for discount types
        return total - discount.calculate(total)

print("--- OCP Discount Calculations ---")
processor = OrderProcessor()
vip_discount = VIPDiscount()
print(f"VIP total for $100: ${processor.calculate_final(100.0, vip_discount)}")

# =============================================================================
# 5. DIP: DEPENDENCY INVERSION PRINCIPLE
# =============================================================================
# BAD: High-level 'AppManager' depends directly on concrete low-level 'MySQLDatabase'
class MySQLDatabase:
    def execute_query(self): return "MySQL records"

class BadAppManager:
    def __init__(self):
        self.db = MySQLDatabase()  # Rigid direct dependency link!

# GOOD: Invert dependency by introducing Abstract Database interface
class DatabaseConnector(abc.ABC):
    @abc.abstractmethod
    def query(self) -> str:
        pass

class PostgreSQLDatabase(DatabaseConnector):
    def query(self): return "PostgreSQL records"

class SQLiteDatabase(DatabaseConnector):
    def query(self): return "SQLite records"

class GoodAppManager:
    # High-level manager depends on abstract interface, not concrete class!
    def __init__(self, db_connector: DatabaseConnector):
        self.db = db_connector
        
    def fetch_records(self):
        return f"Manager retrieved: {self.db.query()}"

print("\n--- DIP Execution ---")
pg_connector = PostgreSQLDatabase()
# Inject PG database
manager1 = GoodAppManager(pg_connector)
print(manager1.fetch_records())

# Inject SQLite database easily
lite_connector = SQLiteDatabase()
manager2 = GoodAppManager(lite_connector)
print(manager2.fetch_records())
