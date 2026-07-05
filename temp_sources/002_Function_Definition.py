# %% [markdown]
# # Topic: Function Definition - Compilation mechanics, annotations, and MAKE_FUNCTION bytecode
# 
# ## 1. DEFINITION & SYNTAX
# - **def statement**: The keyword `def` initiates function definition, followed by function name, parameter list wrapped in parentheses, a colon, and an indented block of statements (the body).
# - **Syntax**:
#   ```python
#   def function_name(param1: type, param2: type) -> return_type:
#       """Docstring explaining interface."""
#       body statements
#   ```
# 
# ## 2. COMPILATION VS RUNTIME IN CPYTHON
# - **Compilation Stage**: When Python compiles a source file into bytecode:
#   1. The parser processes the function body statements.
#   2. It creates a static **Code Object** containing compiled bytecode, constants (`co_consts`), variables (`co_varnames`), and symbol references.
#   3. This code object is saved as a constant in the parent scope. No execution of the function body happens yet.
# - **Runtime Stage**: When execution path reaches the `def` statement line:
#   1. Python runs the `MAKE_FUNCTION` bytecode instruction.
#   2. This allocates a new **Function Object** wrapper on the heap.
#   3. It binds the compiled Code Object, namespace globals (`__globals__`), default arguments, annotations, and closure cell references to the function object.
#   4. The function name identifier is written into the local namespace dictionary, pointing to this newly created function object.
# 
# ## 3. DOCSTRINGS & ANNOTATIONS
# - **Docstrings**: String literal placed as the very first statement inside the function. Exposed as `func.__doc__`.
# - **Type Annotations**: Python 3.5+ (PEP 484) allows annotating parameters and return types. Python compiles these annotations into a dictionary exposed via `func.__annotations__`.
#   - *Note*: Python does NOT enforce type annotations at runtime; they are purely metadata consumed by static analysis tools (like MyPy) and IDEs.
# 
# ## 4. INTERVIEW QUESTIONS
# - **Q: What is the difference between a function object and a code object in CPython?**
#   - *A*: A Code Object is a static, read-only bytecode block compiled from the text. A Function Object is created dynamically at runtime when the `def` line is executed; it wraps the Code Object and links it to active execution contexts (globals, defaults, closures).
# - **Q: Does Python enforce type annotations at runtime?**
#   - *A*: No. Type annotations are metadata stored in `__annotations__` used for static inspection. The interpreter ignores them during execution.
# 
# ---

# %%
import dis  # standard library module to disassemble bytecode

# Define a simple annotated function
def add_numbers(a: int, b: int) -> int:
    """Returns the sum of two integers."""
    return a + b

print("--- Function Metadata Inspection ---")
# 1. Inspecting Docstring
print(f"Docstring: {add_numbers.__doc__}")  # Expected: 'Returns the sum of two integers.'

# 2. Inspecting Annotations
print(f"Annotations: {add_numbers.__annotations__}")
# Expected: {'a': <class 'int'>, 'b': <class 'int'>, 'return': <class 'int'>}

# %%
# 3. Code Object vs Function Object
# The function object wraps the code object in its __code__ attribute
code_obj = add_numbers.__code__
print("\n--- Code Object Internals ---")
print(f"Type of __code__: {type(code_obj)}")  # Expected: <class 'code'>
print(f"Co_varnames (variables): {code_obj.co_varnames}")  # Expected: ('a', 'b')
print(f"Co_consts (constants):   {code_obj.co_consts}")    # Expected: (None, 'Returns the sum of two integers.')

# %%
# 4. Bytecode Disassembly: Analyzing MAKE_FUNCTION
# Let's define a helper function containing a nested def, to inspect the MAKE_FUNCTION bytecode.
def parent_scope():
    def nested_func():
        return 42

print("\n--- Disassembling def statement compilation ---")
# Disassemble parent_scope to see nested_func instantiation bytecode
dis.dis(parent_scope)
# Expected bytecode shows:
# 1. LOAD_CONST (pointing to the nested_func code object)
# 2. MAKE_FUNCTION
# 3. STORE_FAST (saving nested_func to local name dictionary)
