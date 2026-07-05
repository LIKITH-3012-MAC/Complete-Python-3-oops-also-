###############################################################################
# TOPIC: OOP Exercises - coding challenges and solutions for advanced patterns
#
# 1. DEFINITION & INTRODUCTION:
#    - This topic provides practical coding challenges covering key OOP concepts:
#        - Challenge 1: Custom JSON serializer capable of parsing nested object hierarchies.
#        - Challenge 2: A simulated thread-locking context manager.
#        - Challenge 3: A dynamic plugin registry metaclass.
#
# 2. OBJECTIVES:
#    - Apply advanced techniques (descriptors, metaclasses, context managers) to solve
#      practical software architecture problems.
#
###############################################################################

import json  # standard library module to serialize data
import abc  # Standard module for interface definitions

# =============================================================================
# CHALLENGE 1: NESTED OBJECT JSON SERIALIZER
# =============================================================================
# Write a helper class or mixin that can serialize any object, converting nested custom
# class objects into JSON representation dictionary structures recursively.
#
# SOLUTION:
class RecursiveJSONSerializer:
    def to_dict(self):
        # Recursively converts instance attributes to dictionary
        result = {}
        for key, val in self.__dict__.items():
            if key.startswith("_"):
                continue  # skip internal attributes
            if isinstance(val, RecursiveJSONSerializer):
                result[key] = val.to_dict()  # recursive step
            elif isinstance(val, list):
                # parse lists containing serializer objects
                result[key] = [item.to_dict() if isinstance(item, RecursiveJSONSerializer) else item for item in val]
            else:
                result[key] = val
        return result

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

# Test models
class Address(RecursiveJSONSerializer):
    def __init__(self, city, zip_code):
        self.city = city
        self.zip_code = zip_code

class User(RecursiveJSONSerializer):
    def __init__(self, username, address: Address):
        self.username = username
        self.address = address

print("--- Challenge 1: Nested Serializer ---")
addr = Address("San Francisco", "94103")
usr = User("likith", addr)
print(usr.to_json())

# =============================================================================
# CHALLENGE 2: TRANSACTION LOCK CONTEXT MANAGER
# =============================================================================
# Create a class-based context manager `TransactionLock` that takes a database transaction
# identifier, print-logs locks/unlocks, and handles rolback if a division error occurs.
#
# SOLUTION:
class TransactionLock:
    def __init__(self, tx_id):
        self.tx_id = tx_id
        
    def __enter__(self):
        print(f"\n -> [Tx Lock] Acquiring write lock for Tx: {self.tx_id}")
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print(f" -> [Tx Lock] Rollback executed on error: {exc_val}")
            # Suppress ArithmeticError, propagate others
            return issubclass(exc_type, ArithmeticError)
        print(f" -> [Tx Lock] Transaction {self.tx_id} committed successfully. Releasing locks.")
        return True

print("\n--- Challenge 2: Transaction Lock Context ---")
with TransactionLock("TX_9001") as lock:
    print("  Updating user account records...")

try:
    with TransactionLock("TX_9002") as lock:
        print("  Calculating averages...")
        x = 1 / 0  # Triggers rollback, suppresses error
except ZeroDivisionError:
    print("ZeroDivisionError escaped! (Should not happen due to suppression)")

# =============================================================================
# CHALLENGE 3: PLUGIN REGISTER METACLASS
# =============================================================================
# Implement a metaclass `PluginRegistryMeta` that automatically registers any subclass
# inheriting from it to a global list `REGISTERED_PLUGINS`.
#
# SOLUTION:
REGISTERED_PLUGINS = []

class PluginRegistryMeta(type):
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        # Avoid registering the base abstract classes themselves
        if name != "BasePlugin":
            print(f" -> [Metaclass Register] Registering plugin subclass: {name}")
            REGISTERED_PLUGINS.append(cls)

class BasePlugin(metaclass=PluginRegistryMeta):
    pass

class AuthPlugin(BasePlugin):
    pass

class CompressionPlugin(BasePlugin):
    pass

print("\n--- Challenge 3: Metaclass Plugin Registry ---")
print(f"Registered Plugins list: {[p.__name__ for p in REGISTERED_PLUGINS]}")
# Expected: ['AuthPlugin', 'CompressionPlugin']
