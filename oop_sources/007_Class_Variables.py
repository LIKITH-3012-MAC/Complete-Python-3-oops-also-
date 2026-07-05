###############################################################################
# TOPIC: Class Variables - Shared state, Mutability bugs, and Shadowing traps
#
# 1. DEFINITION & INTRODUCTION:
#    - Class Variables: Variables defined inside the class body but outside any methods.
#      They belong to the class itself rather than any individual instance.
#    - Shared State: A single copy of the class variable is stored in memory, shared by
#      all instances of that class.
#
# 2. THE SHADOWING TRAP (Writing via Instance):
#    - Reading a class variable: You can read it via the class name (`Class.var`) or via an
#      instance (`instance.var`). If accessed via an instance, Python searches the instance
#      `__dict__` first. If missing, it looks up the class `__dict__` and returns the value.
#    - Mutating/Writing a class variable (The trap):
#        - If you execute `instance.class_var = new_value`, Python does NOT modify the class
#          variable.
#        - Instead, it inserts a new key-value pair `"class_var": new_value` into the instance's
#          local `__dict__`, creating a new instance variable that shadows the class variable.
#        - To modify the class variable for all instances, you must update it explicitly via
#          the class name: `Class.class_var = new_value`.
#
# 3. MUTABLE CLASS VARIABLES (Common Bug Source):
#    - If a class variable is a mutable collection (like a list `[]` or dictionary `{}`):
#        - Executing `instance.class_var.append(item)` retrieves the reference to the shared list
#          and mutates it in-place.
#        - This updates the list contents for all instances, since the reference itself is shared,
#          often leading to unexpected data leakage bugs.
#
# 4. BEST PRACTICES:
#    - Access and modify class variables using the class name (e.g., `ClassName.variable`)
#      to make your intent explicit and prevent shadowing bugs.
#    - Avoid using mutable objects (lists, dicts) as class variables unless you explicitly
#      intend to build a shared cache or registry.
#
# 5. INTERVIEW QUESTIONS:
#    - Q: What happens when you assign a value to a class variable via an instance
#         (e.g., `self.class_var = 10`)?
#      A: It creates a new instance variable with that name in the instance's `__dict__`,
#         shadowing the class variable. The actual class variable remains unchanged.
#    - Q: How can you mutate a shared list class variable across all instances?
#      A: By modifying it in-place using methods (like `.append()`) via the instance or class name,
#         since all references point to the same shared heap list.
#
# 6. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a class tracking active session counts using class variables,
#      demonstrating correct updates and showing the shadowing trap.
#
###############################################################################

class ServerNode:
    # Class variables
    ACTIVE_CONNECTIONS = 0  # Immutable class variable (int)
    CONNECTED_IPS = []       # Mutable class variable (list)
    
    def __init__(self, node_id):
        self.node_id = node_id
        
    def connect_client(self, ip_address):
        # Correctly update class variables via class name
        ServerNode.ACTIVE_CONNECTIONS += 1
        # Mutating shared mutable class variable (list)
        self.CONNECTED_IPS.append(ip_address)

# Create Server Nodes
node1 = ServerNode("Node_Alpha")
node2 = ServerNode("Node_Beta")

# 1. Shared state demonstration
print("--- Class Variable Shared State ---")
node1.connect_client("192.168.1.1")
node2.connect_client("10.0.0.1")

print(f"ServerNode.ACTIVE_CONNECTIONS: {ServerNode.ACTIVE_CONNECTIONS}")  # Expected: 2
print(f"node1.ACTIVE_CONNECTIONS:      {node1.ACTIVE_CONNECTIONS}")       # Expected: 2 (read fallback)
print(f"Shared IPs List:               {ServerNode.CONNECTED_IPS}")       # Expected: both IPs

# 2. The Shadowing Trap
print("\n--- The Shadowing Trap ---")
# Attempting to modify ACTIVE_CONNECTIONS via instance node1
node1.ACTIVE_CONNECTIONS = 100  # Shadowing occurs!

print(f"node1.ACTIVE_CONNECTIONS:      {node1.ACTIVE_CONNECTIONS}")       # Expected: 100 (read from instance dict)
print(f"node2.ACTIVE_CONNECTIONS:      {node2.ACTIVE_CONNECTIONS}")       # Expected: 2 (still falls back to class value)
print(f"ServerNode.ACTIVE_CONNECTIONS: {ServerNode.ACTIVE_CONNECTIONS}")  # Expected: 2 (class variable remains unchanged!)

# Verify namespaces
print(f"node1.__dict__: {node1.__dict__}")  # Expected: {'node_id': ..., 'ACTIVE_CONNECTIONS': 100}
print(f"node2.__dict__: {node2.__dict__}")  # Expected: {'node_id': ...} (No ACTIVE_CONNECTIONS key)

# 3. Mutable Class Variable Trap (Mutating without assignment)
# We can also modify the list via node1 directly without explicit assignment, mutating the class variable.
print("\n--- Mutable Class Variable In-Place Mutation ---")
node1.CONNECTED_IPS.append("172.16.0.1")  # Appending via instance reference
print(f"node2.CONNECTED_IPS:           {node2.CONNECTED_IPS}")
# Expected: includes "172.16.0.1" because both instances point to the same list object in memory!

# 4. Modifying Class Variable Correctly
ServerNode.ACTIVE_CONNECTIONS = 10
print(f"\nAfter updating via Class Name:")
print(f"node1.ACTIVE_CONNECTIONS:      {node1.ACTIVE_CONNECTIONS}")       # Expected: 100 (Still shadowed!)
print(f"node2.ACTIVE_CONNECTIONS:      {node2.ACTIVE_CONNECTIONS}")       # Expected: 10 (Updated to new class value)
