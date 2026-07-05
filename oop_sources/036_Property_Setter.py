###############################################################################
# TOPIC: Property Setter - @name.setter, data validation, and state consistency
#
# 1. DEFINITION & INTRODUCTION:
#    - Property Setter: A decorator syntax `@property_name.setter` that enables assigning
#      values to a property (e.g. `obj.name = value`), routing the assignment through a method.
#    - Motivation: Data Validation. Allows validating, sanitizing, or transforming values before
#      committing them to instance fields, enforcing class invariants.
#
# 2. SYNTAX & IMPLEMENTATION RULES:
#    - The setter method MUST share the exact same name as the base `@property` getter method.
#    - The setter method must accept exactly one parameter (besides `self`), which represents
#      the new value being assigned.
#    - Under the hood, calling `@property_name.setter` modifies the existing `property` descriptor
#      object in the class dict, setting its internal `__set__` pointer to the setter function.
#
# 3. BEST PRACTICES:
#    - Use setters to enforce types, value bounds (e.g., age cannot be negative), or formats
#      (e.g., verifying email contains '@').
#    - If validating attributes in the constructor, route the initialization write through the
#      property setter (`self.value = initial_value`) instead of the backing field (`self._value = ...`)
#      to reuse validation checks.
#
# 4. INTERVIEW QUESTIONS:
#    - Q: How do you define a setter for a property named `email`?
#      A: First, define the getter using `@property`. Then, define the setter method using the
#         decorator `@email.setter` with the same method name `def email(self, new_email):`.
#    - Q: Why should constructors assign to properties instead of backing variables?
#      A: Assigning to properties (e.g., `self.age = age` instead of `self._age = age`) ensures
#         that constructor arguments pass through the setter's validation rules, preventing invalid
#         object state initialization.
#
# 5. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a `UserAccount` class with a `username` property. Enforce that
#      the username must be a string containing only alphanumeric characters, and between 3 and 15
#      characters long, using a setter.
#
###############################################################################

class Thermostat:
    def __init__(self, temperature_c):
        # We assign to the property setter directly to trigger validation during construction!
        self.temperature = temperature_c
        
    @property
    def temperature(self):
        # Getter: returns backing field _temp_c
        return self._temp_c
        
    @temperature.setter
    def temperature(self, val):
        # Setter: validates and sanitizes input before committing to backing field
        print(f" -> [Property Setter] Validating temperature value: {val}")
        if not isinstance(val, (int, float)):
            raise TypeError("Temperature must be a numeric value.")
        # Enforce physical limit bounds (absolute zero is -273.15 C)
        if val < -273.15:
            raise ValueError("Temperature cannot be below absolute zero (-273.15°C).")
        self._temp_c = val

print("--- Constructor validation via Setter ---")
# Instantiation (triggers setter validation successfully)
t = Thermostat(20.0)
print(f"Current Temperature: {t.temperature}°C")  # Expected: 20.0

print("\n--- Modifying Temperature via Setter ---")
t.temperature = 35.5  # Triggers setter
print(f"Updated Temperature: {t.temperature}°C")  # Expected: 35.5

# Testing validation failures
print("\n--- Testing Setter Failures ---")
try:
    # Attempting to assign incompatible type
    t.temperature = "hot"
except TypeError as e:
    print(f"Caught expected TypeError: {e}")

try:
    # Attempting to assign physically impossible temperature
    t.temperature = -300.0
except ValueError as e:
    print(f"Caught expected ValueError: {e}")
