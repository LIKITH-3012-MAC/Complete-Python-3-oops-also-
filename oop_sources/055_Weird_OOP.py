###############################################################################
# TOPIC: Weird OOP - Dynamic class swaps, list comprehension scope traps, and workarounds
#
# 1. DEFINITION & INTRODUCTION:
#    - Python's OOP engine is highly dynamic, exposing internal bindings that are typically
#      locked in other languages. This flexibility enables advanced metaprogramming but
#      introduces subtle, weird quirks.
#
# 2. DYNAMIC CLASS POINTER SWAPS:
#    - You can dynamically change an object's type at runtime by writing directly to its class
#      pointer: `instance.__class__ = NewClass`.
#    - How CPython reacts:
#        - The interpreter updates the `ob_type` pointer in the object structure.
#        - On subsequent method lookups, Python matches methods in `NewClass` instead of the original
#          class.
#        - Warning: The target class must have compatible layouts (similar `__slots__` or memory struct).
#
# 3. THE super() LIST COMPREHENSION SCOPE TRAP:
#    - In Python 3, list comprehensions, dict comprehensions, and generator expressions are compiled
#      as separate nested function scopes.
#    - Calling `super()` with no arguments inside a list comprehension (e.g. `[super().work() for x in ...]`)
#      fails at runtime with `RuntimeError: super len=0; no arguments`.
#    - Why: Because the zero-argument `super()` lookup relies on compiler-inserted closure variables
#      `__class__` and `self` which are unavailable inside the nested list comprehension scope.
#    - Workaround: Bind a reference to `super()` to a local variable *outside* the comprehension,
#      and use that local variable reference inside:
#      `sup = super()`
#      `[sup.work() for x in ...]`
#
# 4. INTERVIEW QUESTIONS:
#    - Q: Why does calling `super()` fail inside a list comprehension?
#      A: In Python 3, list comprehensions compile as nested function scopes, which isolates them from
#         the method's class scope, preventing the compiler from resolving `__class__` closure bindings.
#    - Q: Can you change an object's class dynamically at runtime?
#      A: Yes, by assigning a new class object to its `__class__` property, provided the new class is
#         compatible in layout.
#
# 5. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a class where a method attempts `super()` inside a list comprehension,
#      capturing the error, and demonstrating the local variable workaround.
#
###############################################################################

# 1. Dynamic Class Swap Demonstration
class OfflineState:
    def execute(self):
        return "Offline: Processing deferred local queue tasks."

class OnlineState:
    def execute(self):
        return "Online: Pushing real-time synchronization updates to server."

state_context = OfflineState()
print("--- Dynamic Class Pointer Swap ---")
print(f"Initial State Class: {state_context.__class__.__name__}")
print(f"Action result:       {state_context.execute()}")

# Swap instance type dynamically!
state_context.__class__ = OnlineState
print(f"\nSwapped State Class: {state_context.__class__.__name__}")
# Action result resolves to OnlineState method now!
print(f"Action result:       {state_context.execute()}")

# =============================================================================
# 2. super() LIST COMPREHENSION TRAP
# =============================================================================
class Parent:
    def format_item(self, item):
        return f"Parent({item})"

class Child(Parent):
    def format_item(self, item):
        return f"Child({item})"
        
    def process_broken(self, items):
        # Calling super().format_item(x) inside list comprehension fails!
        try:
            # Python's compiler raises RuntimeError due to nested scope isolation
            return [super().format_item(x) for x in items]
        except RuntimeError as e:
            print(f" -> Caught expected listcomp super() error: {e}")
            return None
            
    def process_fixed(self, items):
        # Workaround: bind super() to a local variable outside the nested scope
        sup = super()
        return [sup.format_item(x) for x in items]

print("\n--- super() list comprehension scope trap ---")
ch = Child()
data = [10, 20, 30]

print("Running process_broken...")
ch.process_broken(data)

print("\nRunning process_fixed (workaround)...")
processed = ch.process_fixed(data)
print(f"Processed items: {processed}")
# Expected: ['Parent(10)', 'Parent(20)', 'Parent(30)']
