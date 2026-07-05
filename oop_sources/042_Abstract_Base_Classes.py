###############################################################################
# TOPIC: Abstract Base Classes - Dynamic registration, virtual subclasses, and collections.abc
#
# 1. DEFINITION & ARCHITECTURAL PATTERNS:
#    - Abstract Base Classes (ABCs) define interfaces that are checked at run time using nominal
#      type checks.
#
# 2. DYNAMIC SUBCLASS REGISTRATION (Virtual Subclasses):
#    - A highly advanced and powerful feature of CPython is the ability to register a completely
#      unrelated class as a "virtual subclass" of an ABC.
#    - Syntax: `MyABC.register(MyUnrelatedClass)`
#    - How it behaves:
#        - `issubclass(MyUnrelatedClass, MyABC)` returns `True`.
#        - `isinstance(instance_of_unrelated, MyABC)` returns `True`.
#        - MRO Isolation: The virtual subclass does NOT inherit any methods or attributes from the
#          ABC, and the ABC is NOT added to the virtual subclass's Method Resolution Order (MRO).
#        - Why use this? It allows classes to satisfy interface contracts and nominal type checks
#          (e.g., custom adapters satisfying a plugin check) without forcing rigid inheritance links
#          or method lookups.
#
# 3. collections.abc CONTAINER HIERARCHY:
#    - Python's standard library provides `collections.abc` containing abstract templates for
#      container types:
#        - `Iterable`: Defines `__iter__`.
#        - `Sized`: Defines `__len__`.
#        - `Container`: Defines `__contains__`.
#        - `Collection`: Combines Sized, Iterable, and Container.
#        - `Sequence`, `Mapping`, `Set`: Specialized read-only and mutable structures.
#
# 4. INTERVIEW QUESTIONS:
#    - Q: What is a "virtual subclass" in Python?
#      A: A class registered with an ABC using the `register()` method. It passes `isinstance()`
#         and `issubclass()` checks for that ABC but does not inherit from it or appear in its MRO.
#    - Q: Why does `isinstance(my_list, collections.abc.Iterable)` return True even though list
#         does not inherit from Iterable?
#      A: CPython implements `__subclasshook__` on many standard ABCs. This magic method checks
#         if the target class defines the required methods (e.g. `__iter__` for Iterable) dynamically.
#
# 5. EXERCISES & SOLUTIONS:
#    - Coding challenge: Create a custom ABC `Validator`, dynamically register a separate class
#      as its subclass, and verify type checking and MRO properties.
#
###############################################################################

import abc  # Standard library module to build ABCs
import collections.abc  # Standard module containing built-in container interfaces

# 1. Define custom ABC
class PluginInterface(abc.ABC):
    @abc.abstractmethod
    def run_plugin(self):
        pass

# 2. Define completely unrelated class (No inheritance link)
class CustomLogger:
    def run_plugin(self):
        # Implements matching method signature
        print(" -> Running custom logger plugin...")

# Register CustomLogger as a virtual subclass of PluginInterface
PluginInterface.register(CustomLogger)

print("--- Dynamic Registration & Virtual Subclass Checks ---")
# Verify subclass relationship
print(f"Is CustomLogger subclass of PluginInterface? {issubclass(CustomLogger, PluginInterface)}")  # Expected: True

# Verify instance check
logger_inst = CustomLogger()
print(f"Is logger_inst instance of PluginInterface? {isinstance(logger_inst, PluginInterface)}")  # Expected: True

# 3. Inspect MRO (MRO Isolation proof)
# Notice that PluginInterface is NOT in CustomLogger's MRO!
print(f"CustomLogger MRO: {[c.__name__ for c in CustomLogger.mro()]}")
# Expected: ['CustomLogger', 'object'] (No PluginInterface!)

# Consequently, the virtual subclass inherits no methods.
# Calling a non-overridden parent method on a virtual subclass instance raises AttributeError,
# not TypeError, because the parent class is not in its MRO.

# 4. collections.abc and subclasshook verification
# We will show how standard collections satisfy ABC checks without explicit inheritance
# by defining custom class implementing __len__ (which satisfies Sized ABC).
class CustomContainer:
    def __len__(self):
        return 42

container = CustomContainer()
print("\n--- collections.abc __subclasshook__ check ---")
print(f"Is CustomContainer subclass of Sized? {issubclass(CustomContainer, collections.abc.Sized)}")  # Expected: True
print(f"Is container instance of Sized?      {isinstance(container, collections.abc.Sized)}")   # Expected: True
# This works because collections.abc.Sized overrides __subclasshook__ to verify __len__ presence!
