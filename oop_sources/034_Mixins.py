###############################################################################
# TOPIC: Mixin Classes - Stateless utility injection, modular design, and MRO sequencing
#
# 1. DEFINITION & INTRODUCTION:
#    - Mixin: A specialized class that provides method implementations to other classes
#      via multiple inheritance, but is not intended to stand on its own or be instantiated.
#    - Key Characteristic: Stateless. A true mixin should not define its own constructor
#      `__init__` or maintain instance-level variables. It only defines methods that operate on
#      the attributes of the classes that inherit it.
#
# 2. MOTIVATION & COMPARISON:
#    - Multiple Inheritance safety: Because mixins are stateless and do not define initializers,
#      they do not disrupt cooperative `super().__init__()` chains, bypassing the constructor
#      argument mapping bugs common in multiple inheritance.
#    - Modularity: Enables sharing helper capabilities (e.g., serialization, logging, auditing,
#      representation) across completely unrelated classes in a clean, plug-and-play fashion.
#
# 3. MRO SEQUENCING RULE:
#    - In the subclass definition list, mixins should be specified **before** the main base class
#      in the inheritance parents listing:
#      `class ConcreteClass(JSONMixin, AuditMixin, MainBaseClass):`
#      This ensures the mixin's specialized method implementations shadow or override default methods
#      in the main base class.
#
# 4. INTERVIEW QUESTIONS:
#    - Q: What is a Mixin class and how does it differ from a standard base class?
#      A: A Mixin is a stateless helper class designed to inject specific methods into other classes
#         via multiple inheritance. Unlike base classes, it is not designed to be instantiated
#         or maintain state.
#    - Q: What order should Mixins occupy in a class inheritance list?
#      A: They should occupy the left-hand positions before the main base class, ensuring their methods
#         take precedence in the MRO lookup sequence.
#
# 5. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a `JSONSerializationMixin` that dynamically reads any instance's
#      `__dict__` and returns a JSON string, and inherit it in unrelated classes `Car` and `User`.
#
###############################################################################

import json  # standard library module to serialize data

# 1. Define Stateless Mixin Class
class JSONSerializationMixin:
    """Stateless Mixin injecting JSON serialization capabilities."""
    
    def to_json(self):
        # The mixin reads attributes from whatever instance inherits it
        # by accessing self.__dict__
        print(f" -> [JSONMixin] Serializing instance of class: {self.__class__.__name__}")
        # filter out private/protected attributes to keep JSON clean
        public_data = {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
        return json.dumps(public_data)

# 2. Inherit Mixin in Unrelated Class A
class User(JSONSerializationMixin):
    def __init__(self, username, email):
        self.username = username
        self.email = email
        self._private_token = "secret_123"  # Protected, ignored by mixin

# 3. Inherit Mixin in Unrelated Class B
class Product(JSONSerializationMixin):
    def __init__(self, product_id, name, price):
        self.product_id = product_id
        self.name = name
        self.price = price

print("--- Testing Mixin Capabilities ---")
# Instantiate unrelated classes
user = User("likith", "likith@example.com")
prod = Product(501, "MacBook Pro", 1999.99)

# Both classes can immediately call .to_json() despite having no shared base class!
user_json = user.to_json()
print(f"User JSON:    {user_json}")
# Expected: {"username": "likith", "email": "likith@example.com"}

prod_json = prod.to_json()
print(f"Product JSON: {prod_json}")
# Expected: {"product_id": 501, "name": "MacBook Pro", "price": 1999.99}

# 4. Verify Instantiation Block (by design check)
# While Python doesn't block instantiating a mixin class directly, doing so makes no sense
# because it lacks attributes.
mixin_inst = JSONSerializationMixin()
print(f"\nDirect mixin serialization output: {mixin_inst.to_json()}")  # Expected: "{}" (empty dict)
