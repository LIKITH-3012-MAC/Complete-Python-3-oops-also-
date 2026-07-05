###############################################################################
# TOPIC: Aggregation - Weak HAS-A relationships, independent lifecycles, and dependency pass
#
# 1. DEFINITION & INTRODUCTION:
#    - Aggregation: A design pattern modelling a weak **HAS-A** relationship between objects.
#    - Independent Lifecycles: Unlike Composition, the aggregated (child) object exists
#      independently of the container (parent) object.
#    - If the container object is destroyed, the aggregated objects are NOT destroyed. They survive
#      and remain accessible elsewhere in the program.
#    - Implementation: Aggregated objects are created outside the container and passed to it
#      (injected) as constructor arguments or properties.
#
# 2. COMPARISON:
#    - Composition: Part-of relationship. Child cannot exist without parent (e.g., Room has Walls).
#    - Aggregation: Has-a relationship. Child exists independently of parent (e.g., Department has Teachers.
#      If the Department is disbanded, the Teachers are not destroyed; they move to other departments).
#
# 3. INTERVIEW QUESTIONS:
#    - Q: How does Aggregation differ from Composition in code?
#      A: In Aggregation, components are created outside the container class and passed in as parameters.
#         In Composition, components are instantiated inside the container class constructor.
#    - Q: What happens to aggregated objects when their container is deleted?
#      A: They survive because they were instantiated in an external scope, meaning their reference
#         count remains greater than zero.
#
# 4. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a `Department` class that aggregate `Professor` objects.
#      Prove that deleting the `Department` instance keeps the `Professor` instances alive.
#
###############################################################################

# 1. Aggregated Class (Independent existence)
class Professor:
    def __init__(self, name):
        self.name = name
        
    def __del__(self):
        print(f" -> Professor '{self.name}' deallocated.")

# 2. Container Class
class Department:
    def __init__(self, dept_name):
        self.dept_name = dept_name
        self.professors = []  # Holds references to aggregated objects
        
    def add_professor(self, professor):
        # Aggregation: we pass the externally created object reference
        self.professors.append(professor)
        
    def list_staff(self):
        names = [p.name for p in self.professors]
        return f"Department '{self.dept_name}' staff: {', '.join(names)}"
        
    def __del__(self):
        print(f" -> Department '{self.dept_name}' composite container DESTROYED.")

# 3. Execution & Lifecycle Verification
print("--- Instantiating Aggregated Objects ---")
prof1 = Professor("Dr. Smith")
prof2 = Professor("Dr. Jones")

print("\n--- Creating Container ---")
dept = Department("Computer Science")
dept.add_professor(prof1)
dept.add_professor(prof2)
print(dept.list_staff())

print("\n--- Deleting Container (Aggregation Proof) ---")
# Deleting dept should NOT trigger deallocation of prof1 and prof2
# because they are referenced in the outer global scope (prof1, prof2 variables).
del dept
# Expected: Department destroyed message prints, but NO Professor deallocated prints appear yet!
print("Department deleted. Verify professors are still alive:")
print(f"  Professor 1 Name: {prof1.name}")  # Still accessible!

print("\n--- Deleting Professors globally ---")
del prof1
del prof2
# Now, their reference counts hit 0, triggering their destructors.
print("Finished execution.")
