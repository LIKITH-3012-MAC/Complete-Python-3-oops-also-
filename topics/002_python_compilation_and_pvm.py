###############################################################################
# TOPIC: Python Compilation Process, Bytecode, and the Python Virtual Machine (PVM)
#
# 1. DEFINITION & INTRODUCTION:
#    When you execute a Python script, it is not executed directly as machine code.
#    Instead, Python compiles the source code into an intermediate format called
#    bytecode (instructions represented as bytes). This bytecode is then executed
#    by the Python Virtual Machine (PVM), which acts as an interpreter loop.
#
# 2. THE COMPILATION PIPELINE:
#    The transition from source file (`.py`) to running program happens in 4 stages:
#    - Tokenization (Lexical Analysis): The raw source code string is broken down
#      into a stream of logical tokens (keywords, identifiers, operators, indents).
#    - Parsing (Syntactic Analysis): The tokens are organized into a tree structure
#      representing the grammatical structure of the program, called the Abstract
#      Syntax Tree (AST).
#    - Bytecode Compilation: The AST is traversed by the compiler to generate
#      bytecode. The compiled bytecode is stored in CPython object structures
#      representing code blocks (`code` objects).
#    - PVM Execution: The PVM runs a giant loop (historically a switch-case statement
#      in C, though highly optimized in modern CPython) that fetches, decodes,
#      and executes each bytecode instruction sequentially.
#
# 3. HISTORY & MOTIVATION:
#    - Compilation to bytecode is performed to optimize subsequent runs. By compiling
#      once and caching bytecode to disk (in `.pyc` files inside the `__pycache__`
#      directory), Python avoids repeating the slow lexical and syntax analysis steps.
#    - If a module is imported and its source file has not changed, Python loads
#      the cached `.pyc` file directly, accelerating startup.
#
# 4. INTERNAL IMPLEMENTATION & CPYTHON INTERNALS:
#    - Bytecode instructions are represented as integer opcodes (operation codes).
#      For instance, `LOAD_CONST` has an integer value, and `BINARY_OP` (or `BINARY_ADD`
#      in older versions) is another opcode.
#    - Code objects: A compiled function has a `__code__` attribute. This object contains
#      the actual bytecode string (`co_code`), names of constants used (`co_consts`),
#      variable names (`co_varnames`), and other structural data.
#    - PVM Frame Stack: Each function call pushes a new execution frame (`frame` object)
#      onto the PVM's call stack. The frame contains the local variables namespace,
#      a reference to the global namespace, and an evaluation stack where intermediate
#      calculations are performed.
#
# 5. MEMORY LAYOUT & MANAGEMENT:
#    - Frame objects are allocated on the heap, which is why Python recursion is
#      relatively slow compared to compiled languages where frames are allocated
#      on the thread stack.
#    - The frame stack is garbage collected like other Python structures.
#
# 6. TIME & SPACE COMPLEXITY:
#    - Compilation time is O(N) where N is the size of the source code.
#    - Compilation happens at import time. Execution of bytecode by the PVM has
#      an interpreter loop overhead, meaning each instruction has an administrative cost
#      of fetching the next opcode, incrementing the instruction pointer, and dispatching.
#
# 7. PERFORMANCE IMPLICATIONS:
#    - Python is historically slower than JIT-compiled languages (like JavaScript or Java)
#      because CPython's PVM does not compile bytecode to native assembly on-the-fly.
#      However, PyPy (an alternative Python implementation) uses a JIT compiler.
#      Modern CPython (3.11+) features the "Faster CPython" initiative, including
#      PEP 659 "Specializing Adaptive Interpreter" which optimizes repetitive bytecode
#      opcodes dynamically during execution.
#
# 8. THE `dis` MODULE:
#    - Python standard library provides the `dis` module, allowing developers to
#      disassemble Python code objects and view their bytecode instructions.
#
# 9. BEST PRACTICES:
#    - Compile Python source files using `compileall` in production deployments
#      (e.g., Docker containers) to ensure all errors are caught at compile-time and
#      to accelerate container startup.
#
# 10. COMMON MISTAKES & PITFALLS:
#     - Modifying code files at runtime expecting Python to reload them automatically.
#       Python caches imported modules; changes are not parsed unless `importlib.reload()`
#       is explicitly called.
#     - Thinking `.pyc` files are native machine executables. They are platform-independent
#       bytecode that requires a matching PVM to execute.
#
# 11. INTERVIEW QUESTIONS:
#     - Q: What are `.pyc` files and when are they created?
#       A: They contain compiled bytecode. They are created when a module is imported.
#          Running a script directly (e.g., `python script.py`) doesn't write a `.pyc`
#          for that script unless configured, but importing it does.
#     - Q: How does the PVM store local variables?
#       A: They are stored in an array inside the frame object, accessed via fast index-based
#          opcodes like `LOAD_FAST` and `STORE_FAST`, making local lookup faster than globals.
#
# 12. EXERCISES & SOLUTIONS:
#     - Coding challenge: Inspect the `__code__` object of a custom function, list
#       its local variables, constants, and disassemble its execution bytecode.
#
###############################################################################

import dis  # Python built-in disassembler library to view bytecode
import ast  # Python built-in module for manipulating Abstract Syntax Trees
import types  # Module containing helper definitions for code/frame types

# 1. Define a simple mathematical function to inspect
def calculate_hypotenuse(a, b):
    # This is a basic mathematical operation to demonstrate PVM evaluation stack
    c_squared = a**2 + b**2  # Local assignments use STORE_FAST
    return c_squared ** 0.5   # Returns the square root

# 2. Inspect Code Object Attributes
# The function contains a __code__ object which is the compiled C-level struct.
code_obj = calculate_hypotenuse.__code__

print(f"Function Name: {code_obj.co_name}")  # The name of the function
print(f"Constants (co_consts): {code_obj.co_consts}")  # All constants used (None, 2, 0.5)
print(f"Local variables (co_varnames): {code_obj.co_varnames}")  # Local parameters and variables

# 3. Disassemble the Function Bytecode
# dis.dis() shows the virtual machine instructions (opcodes) and how they manipulate the stack.
print("\n--- Bytecode Disassembly ---")
dis.dis(calculate_hypotenuse)
# Expected Output contains commands like:
# LOAD_FAST (loads parameter 'a' onto the stack)
# LOAD_CONST (loads constant 2 onto the stack)
# BINARY_OP or BINARY_POWER (computes a**2)
# STORE_FAST (stores result in 'c_squared')
# RETURN_VALUE (pops top of stack and returns it to the caller)

# 4. Demonstrate Dynamic AST Compilation
# We can dynamically parse a string into an AST, compile it into a code object, and execute it.
source_code = """
x = 10
y = 20
result = x * y
print(f"Dynamic execution result: {result}")
"""

# Parse the source code string into an Abstract Syntax Tree
parsed_ast = ast.parse(source_code, filename="<dynamic>", mode="exec")

# Compile the AST into a code object
compiled_code = compile(parsed_ast, filename="<dynamic>", mode="exec")

# Execute the compiled code block in local namespace context
print("\n--- Running compiled AST ---")
exec(compiled_code)
