###############################################################################
# TOPIC: Dunder Methods - Sequence emulation, Callables, and Hashing contracts
#
# 1. DEFINITION & INTRODUCTION:
#    - Dunder methods extend class objects to emulate native behaviors (making classes look like
#      lists, dicts, functions, or hashable keys).
#
# 2. SEQUENCE & CONTAINER EMULATION:
#    To make a class act as a container or list-like sequence, implement:
#    - `__len__(self)`: Called by `len(obj)`. Must return a non-negative integer.
#    - `__contains__(self, item)`: Called by `item in obj`. Returns a boolean.
#    - `__iter__(self)`: Called by `iter(obj)`. Should return an iterator object.
#    - `__next__(self)`: Called by `next(obj)` to retrieve the next element.
#
# 3. CALLABLE EMULATION:
#    - `__call__(self, *args, **kwargs)`: Allows object instances to be called exactly like
#      functions (e.g. `obj(arg1)`).
#      Use cases: Stateful functions, decorators (as seen in Decorators topic).
#
# 4. HASHING CONTRACTS:
#    - To use custom object instances as dictionary keys or set elements, the object must
#      be **hashable** (implementing `__hash__` and `__eq__`).
#    - Rules of Hashing:
#        1. If two objects compare equal (`a == b`), they MUST return the same hash value
#           (`hash(a) == hash(b)`).
#        2. If you override `__eq__` but do not define `__hash__`, Python automatically sets
#           `__hash__ = None` on your class, making instances unhashable.
#        3. Hash values should remain constant throughout the object's lifetime. Therefore,
#           only hash immutable attributes.
#
# 5. INTERVIEW QUESTIONS:
#    - Q: What happens if a class implements `__eq__` but not `__hash__`?
#      A: Python marks the class as unhashable, and attempting to add instances to a set or use
#         them as dictionary keys will raise a `TypeError: unhashable type`.
#    - Q: How can you make an object callable like a function?
#      A: By implementing the `__call__(self, *args, **kwargs)` magic method in its class.
#
# 6. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a custom class `TaskQueue` that emulates container length,
#      membership checks, allows calling the queue to execute tasks, and is hashable by name.
#
###############################################################################

# 1. Container & Callable Emulation
class NumberSeries:
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop
        self.current = start
        
    def __len__(self):
        # Emulate sequence length
        return max(0, self.stop - self.start + 1)
        
    def __contains__(self, item):
        # Emulate membership (in) operator
        return self.start <= item <= self.stop
        
    def __iter__(self):
        # Resets counter and returns self as iterator
        self.current = self.start
        return self
        
    def __next__(self):
        # Emulate iterator step
        if self.current > self.stop:
            raise StopIteration
        val = self.current
        self.current += 1
        return val
        
    def __call__(self, step):
        # Emulates function call: returns value at offset step
        print(f" -> Instance called as function with step offset: {step}")
        target = self.start + step
        if target in self:
            return target
        raise IndexError("Offset outside series bounds.")

series = NumberSeries(10, 15)

print("--- Container Emulation ---")
print(f"Length of series: {len(series)}")  # Expected: 6
print(f"Is 12 in series? {12 in series}")  # Expected: True
print(f"Is 20 in series? {20 in series}")  # Expected: False

print("\n--- Iteration ---")
print(f"Iterating series list: {list(series)}")  # Iterates 10, 11, 12, 13, 14, 15

print("\n--- Callable Emulation ---")
# Call object like a function
val = series(3)
print(f"Offset 3 value: {val}")  # Expected: 13 (10 + 3)

# 2. Hashing Contract Demonstration
# We will create a class representing a read-only database record.
class DatabaseRecord:
    def __init__(self, record_id, payload):
        self._record_id = record_id  # Immutable ID
        self.payload = payload
        
    def __eq__(self, other):
        if not isinstance(other, DatabaseRecord):
            return False
        return self._record_id == other._record_id
        
    def __hash__(self):
        # Hash value must correspond to equality attributes
        # Since record_id is immutable, we hash it
        return hash(self._record_id)
        
    def __repr__(self):
        return f"Record({self._record_id})"

# Verify hashability
r1 = DatabaseRecord(1001, "Data_A")
r2 = DatabaseRecord(1002, "Data_B")
r3 = DatabaseRecord(1001, "Data_A_Update")  # Same ID, different payload

print("\n--- Hashability Contract Verification ---")
print(f"r1 == r3: {r1 == r3}")  # Expected: True (Equal IDs)
print(f"r1 Hash: {hash(r1)} | r3 Hash: {hash(r3)} | Match? {hash(r1) == hash(r3)}")  # Expected: True

# Since they are hashable and equal, adding them to a set filters duplicates
records_set = {r1, r2, r3}
print(f"Records Set: {records_set}")  # Expected: contains only 2 items: {Record(1001), Record(1002)}
