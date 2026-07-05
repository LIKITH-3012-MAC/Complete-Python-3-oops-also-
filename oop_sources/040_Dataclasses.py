###############################################################################
# TOPIC: Dataclasses - Boilerplate reduction, mutable defaults, and frozen immutability
#
# 1. DEFINITION & INTRODUCTION:
#    - Dataclasses (introduced in Python 3.7 via PEP 557) provide a decorator `@dataclass`
#      that automatically generates common magic methods (`__init__`, `__repr__`, `__eq__`,
#      `__lt__`, etc.) based on variable type annotations declared in the class body.
#    - Purpose: Drastically reduces class boilerplate code for classes designed primarily
#      to hold data.
#
# 2. KEY ATTRIBUTES & POST-INIT:
#    - Type Annotations: You MUST specify type annotations for every class field (e.g. `name: str`);
#      otherwise, the field is ignored by the dataclass generator.
#    - Post-Initialization (`__post_init__(self)`): Called automatically at the end of the generated
#      `__init__` method. Used to calculate derived fields or validate parameters.
#
# 3. MUTABLE DEFAULTS HANDLING (field):
#    - Similar to the mutable default argument bug in functions, declaring a mutable default
#      (like `items: list = []`) directly in a dataclass is blocked and raises a `ValueError`.
#    - Solution: Use `field(default_factory=list)` to ensure a new list is instantiated for
#      each object instance.
#
# 4. IMMUTABILITY (frozen=True):
#    - Setting `@dataclass(frozen=True)` makes instances immutable.
#    - Any attempt to modify attribute values raises a `FrozenInstanceError`.
#    - Frozen dataclasses are automatically hashable, allowing them to be stored in sets or
#      used as dictionary keys.
#
# 5. INTERVIEW QUESTIONS:
#    - Q: Why is `field(default_factory=list)` used instead of `[]`?
#      A: Declaring `[]` as a default shared value would copy the same list reference across
#         all instances. `default_factory` runs the specified callable (e.g. list) to generate
#         a new object on every instantiation, preventing shared state bugs.
#    - Q: What does `frozen=True` do to a dataclass?
#      A: It makes the class instances immutable (read-only) and implements a stable `__hash__`
#         method, allowing instances to be used as dictionary keys.
#
# 6. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a `Product` dataclass (id, name, price, categories list),
#      making price read-only, validating categories using `__post_init__`, and sorting products.
#
###############################################################################

from dataclasses import dataclass, field  # standard dataclasses module
from typing import List  # Type hints helper

# 1. Standard Dataclass with default_factory and post_init
@dataclass(order=True)  # order=True automatically generates comparison dunders (__lt__, __gt__, etc.)
class UserSession:
    # Fields to sort by must be defined first to influence comparison dunder order
    session_id: int
    username: str
    # field(default_factory=...) generates new lists on instantiation
    login_history: List[str] = field(default_factory=list, compare=False)  # Excluded from comparisons
    # field(init=False) means this is not passed to constructor; calculated in post_init
    session_key: str = field(init=False)
    
    def __post_init__(self):
        # Executes after compiler-generated __init__ runs
        print(f" -> Running __post_init__ for user: {self.username}")
        self.session_key = f"{self.username.lower()}_{self.session_id}"

print("--- Instantiating Dataclass ---")
us1 = UserSession(session_id=1002, username="Alice")
print(f"Session 1 object: {us1}")
print(f"Generated session_key: {us1.session_key}")

# 2. Immutable (Frozen) Dataclass
# Useful for configuration records
@dataclass(frozen=True)
class AppConfig:
    host: str = "localhost"
    port: int = 8080

config = AppConfig()
print("\n--- Immutable Dataclass ---")
print(config)

# Attempting modification raises FrozenInstanceError
try:
    config.port = 9090
except Exception as e:
    # dataclasses raises FrozenInstanceError on modification attempts
    print(f"Caught expected error on frozen edit: {type(e).__name__} - {e}")

# 3. Sorting Dataclasses (order=True)
us2 = UserSession(session_id=1001, username="Bob")
# Comparison order is based on field order (session_id is compared first)
print("\n--- Dataclasses Sorting ---")
print(f"us1 ID: {us1.session_id} | us2 ID: {us2.session_id}")
print(f"Is us1 > us2? {us1 > us2}")  # Expected: True (1002 > 1001)

# Sorting a list of dataclasses
sessions = [us1, us2]
print(f"Sorted sessions: {sorted(sessions)}")
# Expected: Bob (1001) sorted before Alice (1002)
