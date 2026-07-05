###############################################################################
# TOPIC: Modules & Packages and the CPython import System
#
# 1. DEFINITION & INTRODUCTION:
#    - Module: A single Python file containing statements and definitions.
#    - Package: A directory containing Python modules and a special file (historically
#      `__init__.py`) indicating that the directory represents a package structure.
#
# 2. THE IMPORT SUBSYSTEM (CPython Internals):
#    - When you run `import module_name`, Python executes a multi-stage import process:
#        1. sys.modules Check: Python first looks up `module_name` in the dictionary `sys.modules`.
#           If the module is already cached there, the cached module object is returned,
#           skipping loading. This prevents duplicate executions.
#        2. Finding: If not cached, Python searches for the module using "finders" configured in
#           `sys.meta_path`. Finders scan file locations (directories in `sys.path`, built-ins,
#           zipped modules).
#        3. Loading: Once located, a "loader" compile-executes the module's source code in a new,
#           isolated module-level namespace and inserts the module object into `sys.modules`.
#
# 3. CIRCULAR IMPORTS (The Dependency Loop Pitfall):
#    - Circular imports occur when module A imports module B, and module B imports module A.
#    - Why it fails:
#        1. Executing `import A` starts loading module A.
#        2. While compiling A, it encounters `import B`. A halts compilation and starts loading B.
#        3. While compiling B, it encounters `import A`. Since A is not yet completely loaded and
#           cached in `sys.modules` (or its attributes are not yet initialized), B cannot find A's
#           properties, raising an `AttributeError` or `ImportError`.
#    - Solutions:
#        1. Deferred/Local Import: Move the import statement inside a function or method rather
#           than declaring it at the module top-level. This delays import execution until call time.
#        2. Bottom Imports: Place the import statement at the bottom of the file (highly discouraged).
#        3. Refactoring: Move the shared dependencies into a separate, third helper module.
#
# 4. TIME & SPACE COMPLEXITY:
#    - First-time import: O(N) where N is source code size (compiles and executes).
#    - Subsequent imports: O(1) dictionary key lookup inside `sys.modules`.
#
# 5. BEST PRACTICES:
#    - Avoid relative imports (`from . import sibling`) where possible; prefer absolute imports
#      for clarity and compatibility with diverse execution directories.
#    - Avoid top-level circular imports. If unavoidable, use local imports inside functions.
#
# 6. INTERVIEW QUESTIONS:
#    - Q: Where does Python check first when executing an import statement?
#      A: In `sys.modules`, which acts as a cache storing all currently imported module objects.
#    - Q: How do you resolve a circular import error in Python?
#      A: By using local imports inside functions/methods to defer execution, or refactoring the
#         shared dependencies into a third module.
#
# 7. EXERCISES & SOLUTIONS:
#    - Coding challenge: Inspect the contents of `sys.modules` to locate loaded built-ins,
#      and write a simulated circular import load and trace.
#
###############################################################################

import sys  # Standard library to inspect imported modules cache
import importlib  # Standard module to dynamically import modules

# 1. Inspecting sys.modules Cache
# sys.modules is a dictionary mapping module names to loaded module objects.
print("--- sys.modules Inspection ---")
print(f"Is 'sys' in sys.modules? {'sys' in sys.modules}")  # Expected: True
print(f"Is 'json' in sys.modules? {'json' in sys.modules}")  # Checks if currently imported

# Import json dynamically at runtime
import json
print(f"Is 'json' in sys.modules after import? {'json' in sys.modules}")  # Expected: True

# 2. Dynamic Import using importlib
# Useful when module names are only known at runtime (e.g. plugin architectures)
math_module = importlib.import_module("math")
print(f"\nDynamically imported module: {math_module}")
print(f"Calling math.sqrt(16) via dynamic import: {math_module.sqrt(16)}")  # Expected: 4.0

# 3. Simulating Circular Import Mechanics and Local Import Resolution
# We will simulate how a circular dependency is bypassed using function-local imports.
# Suppose ModuleA and ModuleB depend on each other.
# We mimic ModuleA's dependency logic here:
class ModuleAClass:
    def __init__(self, value):
        self.value = value
        
    def interact_with_b(self):
        # Instead of importing ModuleB at the top of the file (which would cause a circular loop
        # if ModuleB also imported ModuleA at its top-level), we import it locally here.
        # This works because both classes are fully parsed and cached before this method is ever called!
        import math  # Simulate local import of dependency
        print(f"ModuleAClass interacts using math.ceil: {math.ceil(self.value)}")

a_instance = ModuleAClass(12.3)
a_instance.interact_with_b()
