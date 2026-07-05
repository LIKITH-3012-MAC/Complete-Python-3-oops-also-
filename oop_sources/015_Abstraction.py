###############################################################################
# TOPIC: Abstraction - interface design, hiding complexity, and ABC contracts
#
# 1. DEFINITION & INTRODUCTION:
#    - Abstraction: The process of hiding internal details and implementation complexity,
#      exposing only the essential interface features to the outside world.
#    - Contrast with Encapsulation:
#        - Encapsulation hides data states (hiding fields).
#        - Abstraction hides execution workflows (hiding how methods compute things).
#
# 2. PYTHON IMPLEMENTATION STRATEGIES:
#    - Abstract Base Classes (ABCs): Using the standard library module `abc`. By inheriting from
#      `abc.ABC` and marking methods with `@abc.abstractmethod`, a class defines a strict interface
#      contract that subclasses must implement.
#    - Instantiation Block: Abstract classes cannot be instantiated directly; doing so raises a
#      `TypeError`.
#    - Decoupled Systems: Abstraction allows writing high-level code that works with interfaces
#      (e.g., a generic `DatabaseConnector`) rather than concrete classes (like `PostgreSQLConnector`
#      or `SQLiteConnector`). You can swap drivers later without altering client code!
#
# 3. BEST PRACTICES:
#    - Define clear abstract contracts for components that have multiple implementations (databases,
#      message brokers, payment systems, file savers).
#
# 4. INTERVIEW QUESTIONS:
#    - Q: What is the difference between abstraction and encapsulation?
#      A: Abstraction focuses on hiding implementation logic and exposing a clean interface contract.
#         Encapsulation focuses on bundling data and methods while restricting direct access to attributes.
#    - Q: Can you instantiate an abstract class that has unimplemented abstract methods?
#      A: No. Attempting to do so raises a `TypeError`. Subclasses must override all abstract methods
#         before instantiation is allowed.
#
# 5. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a `MailService` abstract base class with a `send_mail` abstract method,
#      and inherit it to create concrete implementations for `SMTPMailService` and `MockMailService`.
#
###############################################################################

import abc  # Standard library module to construct Abstract Base Classes

# 1. Define Abstract Base Class (The interface contract)
class PaymentProcessor(abc.ABC):
    
    @abc.abstractmethod
    def authorize_payment(self, card_num, amount):
        """Authorize the card details for the specified transaction amount."""
        pass
        
    @abc.abstractmethod
    def capture_payment(self, transaction_id):
        """Capture the authorized funds."""
        pass

# 2. Concrete Implementation A: Stripe API
class StripeProcessor(PaymentProcessor):
    def authorize_payment(self, card_num, amount):
        print(f" -> [Stripe API] Authorizing ${amount} on card: XXXX-{card_num[-4:]}")
        # returns dummy transaction ID
        return "stripe_txn_9999"
        
    def capture_payment(self, transaction_id):
        print(f" -> [Stripe API] Capturing payment transaction: {transaction_id}")
        return True

# 3. Concrete Implementation B: PayPal API
class PayPalProcessor(PaymentProcessor):
    def authorize_payment(self, card_num, amount):
        print(f" -> [PayPal API] Authorizing ${amount} via PayPal check...")
        return "paypal_txn_8888"
        
    def capture_payment(self, transaction_id):
        print(f" -> [PayPal API] Capturing PayPal transaction: {transaction_id}")
        return True

# 4. Client Code utilizing Abstraction
# The checkout function does not care which processor is passed, as long as it inherits
# the PaymentProcessor contract interface.
def perform_checkout(processor: PaymentProcessor, card, total_price):
    print(f"\n--- Checking out via {type(processor).__name__} ---")
    tx_id = processor.authorize_payment(card, total_price)
    success = processor.capture_payment(tx_id)
    if success:
        print("Payment checkout successfully completed.")

# Test Abstraction
stripe = StripeProcessor()
paypal = PayPalProcessor()

# Run both using the same abstract checkout function
perform_checkout(stripe, "1111-2222-3333-4444", 99.50)
perform_checkout(paypal, "5555-6666-7777-8888", 150.00)

# Verify abstract instantiation block
try:
    # Attempting to instantiate the base PaymentProcessor abstract class directly
    invalid_inst = PaymentProcessor()
except TypeError as e:
    print(f"\nCaught expected TypeError (instantiating abstract class): {e}")
