###############################################################################
# TOPIC: Access Modifiers - Public, Protected, and name Mangling mechanics
#
# 1. DEFINITION & NAMING CONVENTIONS:
#    Python does not have keyword-enforced access modifiers (like `public`, `private`,
#    or `protected` in Java or C++). Instead, it relies on naming conventions:
#    - Public Attributes: No leading underscore (e.g., `self.username`). Accessible
#      from outside the class.
#    - Protected Attributes: Single leading underscore (e.g., `self._status`).
#      Indicates an internal implementation detail. By convention, it should not be accessed
#      from outside the class, but Python does NOT block access at the language level.
#    - Private Attributes: Double leading underscores (e.g., `self.__password`).
#      Triggers Name Mangling.
#
# 2. NAME MANGLING MECHANICS (CPython compiler):
#    - When the CPython parser compiles a class statement, any identifier inside the class
#      starting with double underscores (and not ending with double underscores) is automatically
#      rewritten to include the class name prefix.
#    - Formula: `__variable` becomes `_ClassName__variable`.
#    - Purpose:
#        1. To prevent subclass name collision: If subclass B defines `__variable` and parent A
#           also has `__variable`, they will resolve as `_B__variable` and `_A__variable`
#           respectively, preventing overwrites.
#        2. To discourage direct external access.
#    - Note: Private variables are still accessible from outside the class if you use the
#      mangled name (e.g. `obj._ClassName__variable`).
#
# 3. BEST PRACTICES:
#    - Use single underscores `_` to denote attributes intended as internal. Respect this
#      convention when consuming third-party libraries.
#    - Use double underscores `__` only to prevent namespace collisions in complex inheritance
#      trees, not as a security/privacy mechanism.
#
# 4. INTERVIEW QUESTIONS:
#    - Q: Does Python support truly private attributes?
#      A: No. Double leading underscores trigger name mangling, but the attribute is still
#         accessible externally via its mangled name `_ClassName__attribute`.
#    - Q: What does name mangling do to an attribute `__secret` inside class `Bank`?
#      A: The compiler rewrites it to `_Bank__secret`.
#
# 5. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a parent class and subclass both defining a double-underscore
#      private variable, print the instance `__dict__` to view the mangled namespaces, and
#      verify that no collision occurred.
#
###############################################################################

class BaseAccount:
    def __init__(self, owner, secret_key):
        self.owner = owner            # Public
        self._status = "active"       # Protected (by convention)
        self.__secret = secret_key    # Private (triggers name mangling)
        
    def get_secret(self):
        # Accessible internally using direct name
        return self.__secret

class SubAccount(BaseAccount):
    def __init__(self, owner, secret_key, child_key):
        super().__init__(owner, secret_key)
        self.__secret = child_key     # Private in subclass, will not collide with parent!

# 1. Instantiate and Inspect Namespace Dict
acc = SubAccount("Alice", "Parent_Key_123", "Child_Key_999")

print("--- Instance Attribute Namespace (__dict__) ---")
# Let's inspect the __dict__ to see the actual keys stored
print(acc.__dict__)
# Expected output contains:
# 'owner': 'Alice'
# '_status': 'active'
# '_BaseAccount__secret': 'Parent_Key_123'
# '_SubAccount__secret': 'Child_Key_999'
# This proves name mangling prevented collision between the two '__secret' attributes!

# 2. Accessing Modifiers
print("\n--- Access Verification ---")
# Public access (works)
print(f"Public owner:    {acc.owner}")

# Protected access (works, but violates convention warning)
print(f"Protected status: {acc._status}")

# Private access (fails)
try:
    print(acc.__secret)
except AttributeError as e:
    print(f"Caught expected AttributeError accessing raw __secret: {e}")

# 3. Accessing Private Attribute via Mangled Name
# This proves private attributes are not truly hidden or secure; they are just renamed.
mangled_parent_key = acc._BaseAccount__secret
mangled_child_key = acc._SubAccount__secret

print(f"\nMangled Parent Key: {mangled_parent_key}")  # Expected: 'Parent_Key_123'
print(f"Mangled Child Key:  {mangled_child_key}")   # Expected: 'Child_Key_999'
