###############################################################################
# TOPIC: Function Arguments, modern Constraints, and the Mutable Default Trap
#
# 1. DEFINITION & INTRODUCTION:
#    - Python supports highly flexible parameters mapping systems: positional, keyword,
#      arbitrary length (`*args`, `**kwargs`), positional-only (`/`), and keyword-only (`*`).
#
# 2. PARAMETER CONSTRAINTS (PEP 570 & PEP 3102):
#    - Positional-only parameters (`/`): Any parameters defined before `/` must be passed
#      strictly as positional arguments, not as keywords.
#    - Keyword-only parameters (`*`): Any parameters defined after `*` must be passed
#      strictly as keyword arguments.
#    - Variable arguments (`*args`): Captures excess positional arguments as a tuple.
#    - Keyword variable arguments (`**kwargs`): Captures excess keyword arguments as a dictionary.
#    - Parameter declaration order rule:
#      `def func(positional_only, /, positional_or_keyword, *args, keyword_only, **kwargs):`
#
# 3. MUTABLE DEFAULT ARGUMENT TRAP (Critical Bug):
#    - Default parameter values are evaluated **exactly once** when the function is defined
#      (compile time), not every time the function is called (execution time).
#    - If you specify a mutable default argument (like a list `[]` or dictionary `{}`), all
#      subsequent function calls share the exact same default object reference.
#    - Modifying that mutable default inside the function will accumulate updates across
#      separate function calls, causing bugs.
#    - Fix: Use `None` as the default value, and instantiate the mutable structure inside the
#      function body.
#
# 4. TIME COMPLEXITY:
#    - Argument binding at function call: O(1) overhead.
#
# 5. BEST PRACTICES:
#    - Never use mutable types (lists, dicts, sets) as default arguments. Always default to `None`.
#    - Use keyword-only arguments to make function calls explicit and self-documenting,
#      preventing positional parameter shifts.
#
# 6. INTERVIEW QUESTIONS:
#    - Q: What is the output of successive calls to `def f(x=[]): x.append(1); return x`?
#      A: First call returns `[1]`. Second call returns `[1, 1]`. The default list is instantiated
#         once at definition time and shared across all calls.
#    - Q: What does the `/` marker represent in a function signature?
#      A: It denotes the boundary of positional-only parameters. All arguments defined to the
#         left of `/` must be passed positionally.
#
# 7. EXERCISES & SOLUTIONS:
#    - Coding challenge: Write a function illustrating positional-only, keyword-only,
#      and arbitrary variable arguments in a single signature, demonstrating execution bounds.
#
###############################################################################

# 1. The Mutable Default Argument Bug (Demonstration)
def bug_append_to(element, target_list=[]):
    # The default target_list is evaluated once at definition time
    target_list.append(element)
    return target_list

print("--- Mutable Default Argument Trap ---")
print(f"Call 1: {bug_append_to('a')}")  # Expected: ['a']
print(f"Call 2: {bug_append_to('b')}")  # Expected: ['a', 'b'] (Shared reference modification!)
print(f"Call 3: {bug_append_to('c')}")  # Expected: ['a', 'b', 'c']

# The proper fix:
def safe_append_to(element, target_list=None):
    # Check if None, then instantiate locally at execution time
    if target_list is None:
        target_list = []
    target_list.append(element)
    return target_list

print(f"Safe Call 1: {safe_append_to('a')}")  # Expected: ['a']
print(f"Safe Call 2: {safe_append_to('b')}")  # Expected: ['b'] (Clean new list)

# 2. Modern Parameter Constraints (Positional-only & Keyword-only)
# Signature parameters map:
# a, b: Positional-only (left of /)
# c: Positional-or-keyword
# *args: Captures excess positional args
# d: Keyword-only (right of *)
# **kwargs: Captures excess keyword args
def complex_signature(a, b, /, c, *args, d, **kwargs):
    print(f"\nPositional-only: a={a}, b={b}")
    print(f"Positional-or-keyword: c={c}")
    print(f"Extra positional (*args): {args}")
    print(f"Keyword-only: d={d}")
    print(f"Extra keyword (**kwargs): {kwargs}")

# Execute complex signature correctly
complex_signature(1, 2, 3, 4, 5, d=6, extra_key="value")

# Violating Positional-only restriction:
try:
    # Attempting to pass 'a' as keyword (invalid)
    complex_signature(a=1, b=2, c=3, d=6)
except TypeError as e:
    print(f"\nCaught expected TypeError (violating positional-only): {e}")

# Violating Keyword-only restriction:
try:
    # Attempting to pass 'd' positionally (invalid)
    complex_signature(1, 2, 3, 4, 5, 6)
except TypeError as e:
    print(f"Caught expected TypeError (violating keyword-only): {e}")
