###############################################################################
# TOPIC: Method Resolution Order (MRO) and C3 Linearization details
#
# 1. DEFINITION & INTRODUCTION:
#    - Method Resolution Order (MRO): The path list Python traverses to search for
#      attributes or methods on an object instance.
#    - Python uses the **C3 Linearization Algorithm** (introduced in Python 2.3 for new-style
#      classes) to construct this list for every class.
#
# 2. C3 LINEARIZATION ALGORITHM STEP-BY-STEP:
#    - The MRO of a class `C` inheriting from parents `B1, B2, ..., BN` is defined as:
#      `L[C(B1...BN)] = [C] + merge(L[B1], L[B2], ..., L[BN], [B1, B2, ..., BN])`
#    - The `merge` operation works by picking the first head of the lists that does not appear in
#      the tail (any position except the first) of any other lists.
#    - Definitions:
#        - Head of a list: The first element (e.g. `B1` in `[B1, B2, B3]`).
#        - Tail of a list: Remaining elements (e.g. `[B2, B3]` in `[B1, B2, B3]`).
#    - Process:
#        1. Look at the head of the first merge input list.
#        2. If this head is NOT in the tail of any other input list, append it to the MRO and
#           remove it from all input lists.
#        3. If it is in the tail of another list, move to the next list's head and check again.
#        4. Repeat until all lists are empty. If you get stuck (circular constraint), MRO compilation
#           fails with a `TypeError`.
#
# 3. TRACING MRO:
#    - Inspect using `ClassName.__mro__` (returns a tuple of class objects).
#    - Inspect using `ClassName.mro()` (returns a list of class objects).
#
# 4. INTERVIEW QUESTIONS:
#    - Q: Explain how the C3 Linearization algorithm handles MRO merges.
#      A: It merges the MROs of parent classes and the list of parents themselves by picking heads
#         that do not appear in the tails of any other lists, maintaining local precedence and
#         monotonicity.
#    - Q: What does `D.mro()` return?
#      A: It returns a list of class objects representing the attribute lookup search order for D.
#
# 5. EXERCISES & SOLUTIONS:
#    - Coding challenge: Trace the MRO of a custom multiple inheritance diamond structure manually
#      using the C3 formula, then verify your calculation using `class.mro()`.
#
###############################################################################

# 1. Manual C3 Linearization Tracing Example
# Let's define the following structure:
# class O: pass
# class A(O): pass
# class B(O): pass
# class C(A, B): pass
#
# Let's trace L[C(A, B)] using the C3 formula:
# L[O] = [O, object]
# L[A] = [A] + merge(L[O], [O]) = [A] + merge([O, object], [O]) = [A, O, object]
# L[B] = [B] + merge(L[O], [O]) = [B, O, object]
#
# L[C] = [C] + merge(L[A], L[B], [A, B])
#      = [C] + merge([A, O, object], [B, O, object], [A, B])
#
# Step 1: Head 'A' of [A, O, object] is not in tails of [B, O, object] or [A, B].
#         -> Add A. Remove A from merge lists.
#      = [C, A] + merge([O, object], [B, O, object], [B])
#
# Step 2: Head 'O' of [O, object] is in the tail of [B, O, object] (since it is after B).
#         -> We cannot pick O. Skip to next list [B, O, object], head is B.
#         -> Head 'B' is not in tail of [O, object] or [B].
#         -> Add B. Remove B from lists.
#      = [C, A, B] + merge([O, object], [O, object])
#
# Step 3: Head 'O' is not in tail.
#         -> Add O. Remove O.
#      = [C, A, B, O] + merge([object], [object])
#
# Step 4: Add object.
#      = [C, A, B, O, object]
#
# Let's verify this using Python execution!

class O: pass
class A(O): pass
class B(O): pass
class C(A, B): pass

print("--- Tracing MRO of Class C ---")
computed_mro = C.mro()

# Convert list to class name strings for display
mro_names = [cls.__name__ for cls in computed_mro]
print(f"Computed MRO list: {mro_names}")
# Expected: ['C', 'A', 'B', 'O', 'object'] (Matches manual tracing!)

# 2. Resolving MRO Conflict Errors (The C3 violation)
# If a subclass tries to define parents that conflict with their inheritances order:
# e.g., class X(A, C) -> Conflict because C inherits A, so C should be searched before A,
# but the declaration X(A, C) specifies A should be searched before C!
try:
    # Dynamically compile the conflict class to capture TypeError
    type("MroConflictClass", (A, C), {})
except TypeError as e:
    print(f"\nCaptured MRO Conflict TypeError: {e}")
    # Expected: Cannot create a consistent method resolution order (MRO) for bases A, C
