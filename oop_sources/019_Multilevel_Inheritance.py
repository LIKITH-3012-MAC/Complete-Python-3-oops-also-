###############################################################################
# TOPIC: Multilevel Inheritance - Linear chains, method overrides, and constructor sequences
#
# 1. DEFINITION & INTRODUCTION:
#    - Multilevel Inheritance: An inheritance structure forming a linear hierarchy chain.
#      Class C inherits from Class B, which in turn inherits from Class A.
#      Example: Grandparent -> Parent -> Child.
#
# 2. KEY CHARACTERISTICS:
#    - Variable and Method Propagation: Class C inherits all attributes and methods defined
#      in both B and A automatically (unless overridden).
#    - Constructor Chaining: Each subclass must delegate constructor parameters up the chain
#      to its immediate parent using `super()`, ensuring properties at all levels are configured.
#
# 3. INTERMEDIATE METHOD OVERRIDES:
#    - An intermediate class (B) can override a method from class A. When class C calls the method:
#        - If C does not override it, it inherits B's overridden version, not A's original version.
#        - If C overrides it, C can still access B's version using `super().method()` or jump up
#          to A's version by calling `A.method(self)` explicitly.
#
# 4. BEST PRACTICES:
#    - Keep multilevel hierarchies shallow. Deep nesting chains (more than 3 levels) make the
#      codebase hard to follow, trace, and maintain.
#
# 5. INTERVIEW QUESTIONS:
#    - Q: If Class C inherits from B, and B inherits from A, and B overrides a method `info()`,
#         what does `super().info()` call inside Class C?
#      A: It calls Class B's implementation of `info()`, since B is the next ancestor in the
#         MRO list for C.
#    - Q: How can you check if an object is an instance of its grandparent class?
#      A: Using `isinstance(child_obj, Grandparent)`. It will return `True` because child inherits
#         from grandparent through the multilevel chain.
#
# 6. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a 3-level hierarchy: `Device` -> `Computer` -> `Laptop`,
#      override description methods at each level, and demonstrate constructor propagation.
#
###############################################################################

# 1. Grandparent Class (Level 1)
class Device:
    def __init__(self, brand):
        self.brand = brand
        print("Device initialized")
        
    def get_info(self):
        return f"Brand: {self.brand}"

# 2. Parent Class (Level 2 - Intermediate)
class Computer(Device):
    def __init__(self, brand, ram_size):
        # Delegate to Device
        super().__init__(brand)
        self.ram_size = ram_size
        print("Computer initialized")
        
    # Override get_info
    def get_info(self):
        parent_info = super().get_info()
        return f"{parent_info} | RAM: {self.ram_size}GB"

# 3. Child Class (Level 3 - Leaf)
class Laptop(Computer):
    def __init__(self, brand, ram_size, battery_life):
        # Delegate to Computer (which delegates to Device)
        super().__init__(brand, ram_size)
        self.battery_life = battery_life
        print("Laptop initialized")
        
    # Override get_info
    def get_info(self):
        parent_info = super().get_info()
        return f"{parent_info} | Battery: {self.battery_life} hours"

print("--- Instantiating leaf class (Laptop) ---")
# Creates instance, running all 3 initializers sequentially
my_laptop = Laptop("Apple", 16, 18)

print("\n--- Executing Multilevel Overridden Method ---")
print(my_laptop.get_info())
# Expected Output: Brand: Apple | RAM: 16GB | Battery: 18 hours

# 4. Runtime checks
print("\n--- Type Check Verifications ---")
print(f"Is laptop a Computer? {isinstance(my_laptop, Computer)}")  # Expected: True
print(f"Is laptop a Device?   {isinstance(my_laptop, Device)}")    # Expected: True
print(f"Laptop MRO:           {Laptop.__mro__}")
# Expected MRO: (Laptop, Computer, Device, object)
