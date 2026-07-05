###############################################################################
# TOPIC: Hybrid Inheritance - Combining hierarchies, C3 Linearization, and resolution maps
#
# 1. DEFINITION & INTRODUCTION:
#    - Hybrid Inheritance: A combination of two or more types of inheritance structures
#      (e.g., combining Multilevel, Multiple, and Hierarchical patterns).
#    - Graph Structure: It forms a Directed Acyclic Graph (DAG) of classes rather than a
#      simple tree structure.
#
# 2. C3 LINEARIZATION (CPython Internals):
#    - Complex hybrid graphs can lead to ambiguous method lookup orders.
#    - To guarantee predictability, CPython compiles the inheritance graph into a flat search
#      list (MRO) using the C3 Linearization Algorithm.
#    - Three Core Constraints of C3 Linearization:
#        1. Subclass search priority: Subclasses are always searched before their parents.
#        2. Parent order consistency: Parents are searched in the order they are defined in the
#           subclass declaration line (from left to right).
#         3. Monotonicity: If class A is searched before class B in one context, it should not be
#            searched after B in another context.
#    - If C3 Linearization cannot resolve a valid linear order satisfying these constraints, Python
#      raises a `TypeError: Cannot create a consistent method resolution order (MRO)`.
#
# 3. BEST PRACTICES:
#    - Avoid deep hybrid graphs in production code; they introduce significant debugging overhead
#      and make tracking variable scopes extremely difficult.
#
# 4. INTERVIEW QUESTIONS:
#    - Q: What algorithm does Python use to calculate the Method Resolution Order?
#      A: The C3 Linearization Algorithm.
#    - Q: What causes a "Cannot create a consistent MRO" TypeError?
#      A: This occurs when C3 Linearization detects a circular dependency constraint in the inheritance
#         declaration (e.g. subclassing two classes that have conflicting order constraints).
#
# 5. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a hybrid inheritance structure combining Hierarchical,
#      Multilevel, and Multiple patterns, print its MRO list, and execute cooperative initializations.
#
###############################################################################

# 1. Hybrid Hierarchy Setup
# We define a hybrid structure:
#        Root (Device)
#       /     \
#   Camera   Computer
#      \     /      \
#    SmartPhone     Server
#
# SmartPhone combines Multiple (Camera, Computer) and Multilevel (Device -> Computer -> SmartPhone)
# Server combines Single (Computer -> Server)

class Device:
    def __init__(self, brand, **kwargs):
        print(" -> Device.__init__ entered")
        self.brand = brand
        super().__init__(**kwargs)
        print(" -> Device.__init__ exited")

class Camera(Device):
    def __init__(self, megapixels, **kwargs):
        print(" -> Camera.__init__ entered")
        super().__init__(**kwargs)
        self.megapixels = megapixels
        print(" -> Camera.__init__ exited")

class Computer(Device):
    def __init__(self, processor, **kwargs):
        print(" -> Computer.__init__ entered")
        super().__init__(**kwargs)
        self.processor = processor
        print(" -> Computer.__init__ exited")

class SmartPhone(Camera, Computer):
    def __init__(self, brand, megapixels, processor, screen_size):
        print(" -> SmartPhone.__init__ entered")
        # Call cooperatively passes parameters using kwargs
        super().__init__(brand=brand, megapixels=megapixels, processor=processor)
        self.screen_size = screen_size
        print(" -> SmartPhone.__init__ exited")

# 2. Inspect MRO of Hybrid Class
print("--- SmartPhone Method Resolution Order ---")
for idx, cls in enumerate(SmartPhone.__mro__):
    print(f"[{idx}] Class: {cls.__name__}")
# Expected C3 Order:
# 1. SmartPhone
# 2. Camera (first parent in definition)
# 3. Computer (second parent in definition)
# 4. Device (common ancestor)
# 5. object

print("\n--- Cooperative Initialization trace ---")
phone = SmartPhone(
    brand="Google",
    megapixels=50,
    processor="Tensor G3",
    screen_size="6.2 inches"
)

# 3. Invalid MRO compilation attempt (MRO Conflict Error)
# We will show how a class declaration can violate C3 Linearization.
# Suppose:
# class X(object): pass
# class Y(X): pass
# class Z(X, Y): pass # TypeError! Y is a subclass of X, but X appears before Y in Z's declaration!
try:
    # Executing dynamic type creation to test compile error without crashing the script parser
    type("ConflictClass", (object, Base), {})
except TypeError as e:
    # C3 detects that 'object' is a parent of 'Base' but is specified before 'Base' in parent listing.
    print(f"\nCaught expected MRO conflict TypeError: {e}")
