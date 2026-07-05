###############################################################################
# TOPIC: Composition - HAS-A relationships, lifecycle bindings, and design alternatives
#
# 1. DEFINITION & INTRODUCTION:
#    - Composition: A design pattern modelling a strong **HAS-A** relationship between objects.
#    - Lifecycle Binding (Ownership): Under composition, the owned (component) object cannot
#      exist independently of the owner (composite) object.
#    - If the owner object is destroyed, the owned objects are also immediately destroyed in memory.
#    - Implementation: The component objects are typically instantiated directly inside the owner's
#      constructor (`__init__`).
#
# 2. FAVOR COMPOSITION OVER INHERITANCE:
#    - A fundamental software design principle.
#    - Inheritance forms tight coupling: changes in the base class propagate down subclass trees,
#      often breaking subclass behaviors (Fragile Base Class problem).
#      Inheritance is static and cannot be changed at runtime.
#    - Composition forms loose coupling: components interact through public APIs. We can swap
#      components dynamically at runtime, creating highly flexible systems.
#
# 3. TIME & SPACE COMPLEXITY:
#    - Overhead is minimal: standard object allocation costs.
#
# 4. INTERVIEW QUESTIONS:
#    - Q: What characterizes "Composition" compared to "Aggregation"?
#      A: In Composition, the owned object's lifecycle is bound to the owner (if parent dies,
#         child dies). In Aggregation, the owned object exists independently and can survive
#         the destruction of the parent container.
#    - Q: Why is it recommended to "favor composition over inheritance"?
#      A: Composition creates loosely coupled systems where classes can delegate tasks to other
#         specialized components. This avoids deep, rigid, and fragile inheritance trees.
#
# 5. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a `Computer` class composed of a `CPU` and `HardDrive`,
#      demonstrating matched lifecycles using print trackers.
#
###############################################################################

# 1. Component Classes (Cannot exist logically or lifecycle-wise without the composite container)
class CPU:
    def __init__(self, cores):
        self.cores = cores
        
    def execute(self):
        return f"Executing instructions on {self.cores}-core CPU."
        
    def __del__(self):
        print(" -> CPU component deallocated.")

class HardDrive:
    def __init__(self, capacity):
        self.capacity = capacity
        
    def read_data(self):
        return f"Reading data from {self.capacity}GB HardDrive."
        
    def __del__(self):
        print(" -> HardDrive component deallocated.")

# 2. Composite Class (Owner)
class Computer:
    def __init__(self, brand, cpu_cores, hd_capacity):
        self.brand = brand
        # Composition: we instantiate components DIRECTLY inside the container constructor
        # This binds their lifetimes to the Computer instance!
        self.cpu = CPU(cpu_cores)
        self.hard_drive = HardDrive(hd_capacity)
        
    def boot(self):
        print(f"\nBooting {self.brand} computer:")
        print(f"  {self.cpu.execute()}")
        print(f"  {self.hard_drive.read_data()}")
        
    def __del__(self):
        print(f" -> Computer '{self.brand}' composite DESTROYED.")

print("--- Creating Composite Object ---")
my_pc = Computer("Dell XPS", 8, 1000)
my_pc.boot()

print("\n--- Deleting Composite Object (Lifecycle Bindings Proof) ---")
# Deleting my_pc should immediately trigger deallocation of CPU and HardDrive
# because they are owned exclusively by my_pc and have no other references.
del my_pc
# Expected console print:
# CPU deallocated, HardDrive deallocated, Computer destroyed.
print("Deletion statement complete.")
