###############################################################################
# TOPIC: Encapsulation - state protection, Getters/Setters, and Data Integrity
#
# 1. DEFINITION & INTRODUCTION:
#    - Encapsulation: The bundling of data (attributes) and behavior (methods) into a single
#      cohesive unit (the class), and restricting direct access to the object's components.
#
# 2. BENEFITS & IMPLEMENTATION:
#    - State Protection: Prevents external code from modifying an object's internal attributes
#      into invalid or corrupt states.
#    - Interface Decoupling: The internal data layout can be refactored without breaking external
#      code that calls the class interfaces.
#    - Getters and Setters: Methods used to read and write private variables safely. Setter
#      methods contain validation logic to reject illegal inputs.
#
# 3. BEST PRACTICES:
#    - Protect sensitive state variables (e.g. balances, indices, IDs) using private/protected
#      prefixes.
#    - Implement validation rules inside setters to guarantee object data integrity at all times.
#
# 4. INTERVIEW QUESTIONS:
#    - Q: What is encapsulation and why is it important?
#      A: It is the bundling of data and methods into a class while restricting direct external
#         access to attributes. It ensures data validation, hides complexity, and decouples the
#         interface from implementation.
#    - Q: How is encapsulation achieved in Python?
#      A: By using protected (`_`) or private (`__`) naming prefixes for attributes and exposing
#         public getter/setter methods to read/write them safely.
#
# 5. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a `BankAccount` class where the balance is encapsulated,
#      and deposits/withdrawals are validated through getter and setter interfaces.
#
###############################################################################

class BankAccount:
    def __init__(self, owner, initial_balance):
        self.owner = owner
        # Encapsulate balance using protected prefix to signify internal state
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative.")
        self._balance = initial_balance
        
    # Getter method: read-only access to _balance
    def get_balance(self):
        return self._balance
        
    # Setter method: controlled write access with validation checks
    def deposit(self, amount):
        if amount <= 0:
            print(" -> [Error] Deposit amount must be positive!")
            return False
        self._balance += amount
        print(f" -> Deposited ${amount}. Current Balance: ${self._balance}")
        return True
        
    def withdraw(self, amount):
        if amount <= 0:
            print(" -> [Error] Withdrawal amount must be positive!")
            return False
        if amount > self._balance:
            print(" -> [Error] Insufficient funds for withdrawal!")
            return False
        self._balance -= amount
        print(f" -> Withdrew ${amount}. Current Balance: ${self._balance}")
        return True

# 1. Instantiate Account
print("--- Creating Encapsulated BankAccount ---")
acc = BankAccount("Alice", 500)

# Verify public state access is denied (by convention)
print(f"Accessing balance via getter: ${acc.get_balance()}")  # Expected: 500

# 2. Testing Validation Constraints (Encapsulation Guard)
print("\n--- Testing Deposits ---")
acc.deposit(-50)  # Fails validation
acc.deposit(200)  # Succeeds, balance becomes 700

print("\n--- Testing Withdrawals ---")
acc.withdraw(1000)  # Fails validation (insufficient funds)
acc.withdraw(300)   # Succeeds, balance becomes 400

# Verify final state via getter
print(f"\nFinal balance: ${acc.get_balance()}")  # Expected: 400
