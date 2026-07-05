###############################################################################
# TOPIC: OOP Design Patterns - Factory Method, Adapter, and Strategy Pattern
#
# 1. DEFINITION & INTRODUCTION:
#    - Design Patterns: Reusable, structured solutions to common software design problems.
#    - Categories:
#        1. Creational: Focus on object creation mechanisms (e.g. Factory, Singleton, Builder).
#        2. Structural: Focus on class/object composition layouts (e.g. Adapter, Decorator, Proxy).
#        3. Behavioral: Focus on object communication and responsibility delegation (e.g. Strategy, Observer).
#
# 2. PATTERNS COVERED:
#    - Factory Method: Defines an interface for creating objects, letting subclasses decide
#      which class to instantiate. Prevents tight coupling to concrete classes.
#    - Adapter Pattern: Converts the interface of a class into another interface clients expect.
#      Acts as a translator wrapper between incompatible systems.
#    - Strategy Pattern: Defines a family of algorithms, encapsulates each one, and makes them
#      interchangeable. Lets the algorithm vary independently from the clients that use it.
#
# 3. BEST PRACTICES:
#    - Do not over-engineer. Only apply patterns when they resolve actual complexity or change requirements.
#
# 4. INTERVIEW QUESTIONS:
#    - Q: Explain the Strategy design pattern and when to use it.
#      A: It encapsulates a set of interchangeable algorithms inside separate classes. Use it when
#         you need to swap execution algorithms at runtime without modifying the caller class.
#    - Q: What does the Adapter design pattern do?
#      A: It wraps an incompatible object's interface to match the client's expected interface contract.
#
# 5. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a logging system that dynamically selects different logging strategies
#      (Console, File) based on system configuration.
#
###############################################################################

import abc  # Standard module to design pattern interfaces

# =============================================================================
# 1. CREATIONAL: FACTORY METHOD PATTERN
# =============================================================================
class Notification(abc.ABC):
    @abc.abstractmethod
    def send(self, message):
        pass

class EmailNotification(Notification):
    def send(self, message):
        print(f" -> [Email sent]: {message}")

class SMSNotification(Notification):
    def send(self, message):
        print(f" -> [SMS sent]: {message}")

# The Creator/Factory base class
class NotificationFactory:
    @staticmethod
    def create_notifier(notifier_type: str) -> Notification:
        # Resolves dynamic creation based on string type
        if notifier_type == "email":
            return EmailNotification()
        elif notifier_type == "sms":
            return SMSNotification()
        raise ValueError(f"Unknown notifier type: {notifier_type}")

print("--- Factory Method execution ---")
notifier = NotificationFactory.create_notifier("email")
notifier.send("Welcome to the system!")

# =============================================================================
# 2. STRUCTURAL: ADAPTER PATTERN
# =============================================================================
# Client expects an interface supporting json payload format
class JSONLogger:
    def log_json(self, json_str):
        print(f" -> [JSON Log]: {json_str}")

# Third-party legacy logger that only supports XML format
class LegacyXMLLogger:
    def log_xml(self, xml_str):
        print(f" -> [Legacy XML Log]: {xml_str}")

# Adapter class to translate LegacyXML to JSON interface
class LoggerAdapter(JSONLogger):
    def __init__(self, xml_logger: LegacyXMLLogger):
        self.xml_logger = xml_logger
        
    def log_json(self, json_str):
        # Translate JSON format to XML format representation
        # (Simulated translation: wrapping key values)
        import json
        data = json.loads(json_str)
        xml_converted = f"<log><msg>{data.get('message')}</msg></log>"
        # Delegate call to legacy component
        self.xml_logger.log_xml(xml_converted)

print("\n--- Adapter Pattern execution ---")
legacy_component = LegacyXMLLogger()
adapter = LoggerAdapter(legacy_component)
# Client calls JSON Logger interface, legacy XML logs execute!
adapter.log_json('{"message": "Database backup completed"}')

# =============================================================================
# 3. BEHAVIORAL: STRATEGY PATTERN
# =============================================================================
class DiscountStrategy(abc.ABC):
    @abc.abstractmethod
    def apply_discount(self, price: float) -> float:
        pass

class FlatDiscount(DiscountStrategy):
    def __init__(self, discount_amount):
        self.amount = discount_amount
    def apply_discount(self, price: float) -> float:
        return max(0.0, price - self.amount)

class PercentageDiscount(DiscountStrategy):
    def __init__(self, percent):
        self.percent = percent
    def apply_discount(self, price: float) -> float:
        return price * (1.0 - (self.percent / 100))

# Context Class (uses interchangeable strategy)
class ShoppingCart:
    def __init__(self, discount_strategy: DiscountStrategy):
        self.strategy = discount_strategy
        
    def set_strategy(self, new_strategy: DiscountStrategy):
        # Swaps strategy at runtime!
        self.strategy = new_strategy
        
    def checkout(self, raw_price):
        final_price = self.strategy.apply_discount(raw_price)
        print(f"Checkout Price (Strategy: {type(self.strategy).__name__}): ${final_price:.2f}")

print("\n--- Strategy Pattern execution ---")
cart = ShoppingCart(FlatDiscount(10.0))
cart.checkout(100.0)  # Expected: 90.00

# Swap strategy at runtime
cart.set_strategy(PercentageDiscount(20))
cart.checkout(100.0)  # Expected: 80.00
