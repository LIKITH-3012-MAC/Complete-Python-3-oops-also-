###############################################################################
# TOPIC: Association - Cardinality, unidirectional vs bidirectional, and comparison summary
#
# 1. DEFINITION & INTRODUCTION:
#    - Association: A broad term representing any relationship or link between two completely
#      independent classes.
#    - Unlike inheritance (IS-A) or composition (Part-of), association simply means two objects
#      "know" about each other or cooperate to complete tasks.
#
# 2. CLASSIFICATIONS:
#    - Directionality:
#        - Unidirectional Association: Class A knows about Class B, but B does not know about A.
#          Example: `Customer` has a reference to `CreditCard`, but `CreditCard` does not keep a
#          reference to `Customer`.
#        - Bidirectional Association: Both classes hold references to each other.
#          Example: `Doctor` has a list of `Patient` instances, and `Patient` has a reference to
#          the `Doctor` instance.
#    - Cardinality:
#        - One-to-One (e.g. Employee and Cubicle).
#        - One-to-Many (e.g. Manager and Employees).
#        - Many-to-Many (e.g. Students and Courses).
#
# 3. RELATIONSHIP RELATIONSHIPS SUMMARY:
#    - Association: "Cooperates with". Independent lifecycles, loose link.
#    - Aggregation: "Has a" (weak). Independent lifecycles, container-member link.
#    - Composition: "Has a" (strong). Co-dependent lifecycles, owner-owned link.
#
# 4. INTERVIEW QUESTIONS:
#    - Q: What is Association in OOP?
#      A: A relationship where two independent objects cooperate. Neither owns the other, and
#         their lifecycles are completely decoupled.
#    - Q: How do you implement a bidirectional association safely in Python?
#      A: By updating references on both sides during association setup (e.g., adding patient to
#         doctor, and assigning doctor to patient).
#
# 5. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a Bidirectional Association between `Driver` and `Car` classes,
#      ensuring that binding a car to a driver updates references on both objects.
#
###############################################################################

# 1. Bidirectional Association Example (Driver <-> Car)
class Car:
    def __init__(self, model, license_plate):
        self.model = model
        self.plate = license_plate
        self.driver = None  # Reference to associated Driver
        
    def __repr__(self):
        return f"Car({self.model})"

class Driver:
    def __init__(self, name):
        self.name = name
        self.assigned_cars = []  # References to associated Cars (one-to-many)
        
    def __repr__(self):
        return f"Driver({self.name})"
        
    def associate_car(self, car_obj):
        # Prevent infinite loops during bidirectional setup
        if car_obj not in self.assigned_cars:
            self.assigned_cars.append(car_obj)
            # Bidirectional update: update the car's driver reference as well!
            car_obj.driver = self

print("--- Bidirectional Association ---")
driver_alice = Driver("Alice")
car1 = Car("Tesla Model 3", "ABC-123")
car2 = Car("Ford Mustang", "XYZ-789")

# Set up association
driver_alice.associate_car(car1)
driver_alice.associate_car(car2)

# Verify association on both sides
print(f"Driver Alice's cars: {driver_alice.assigned_cars}")
print(f"Car 1's driver:      {car1.driver}")  # Expected: Driver(Alice)
print(f"Car 2's driver:      {car2.driver}")  # Expected: Driver(Alice)

# 2. Unidirectional Association Example (User -> Logger)
class SystemLogger:
    def log_event(self, event):
        print(f" -> [LOG]: {event}")

class UserProfile:
    def __init__(self, username, logger_service):
        self.username = username
        self.logger = logger_service  # Unidirectional association (User knows logger, logger does not know User)
        
    def perform_action(self, action):
        # Cooperate with associated object
        self.logger.log_event(f"User '{self.username}' executed action: {action}")

print("\n--- Unidirectional Association ---")
sys_logger = SystemLogger()
user = UserProfile("likith", sys_logger)
user.perform_action("Database backup")
