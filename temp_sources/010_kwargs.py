# %% [markdown]
# # Topic: **kwargs - Keyword packing, CPython dictionary wrapping, and call-site unpacking
# 
# ## 1. DEFINITION & SYNTAX
# - **\*\*kwargs**: The double asterisk syntax prefixing a parameter name inside a function definition allows the function to accept an arbitrary number of keyword (named) arguments.
# - **Naming**: The identifier `kwargs` is a standard naming convention; any valid variable identifier prefixed by `**` operates identical (e.g. `**metadata`, `**options`).
# 
# ## 2. CPYTHON INTERNALS: DICTIONARY PACKING
# - When a function containing a `**kwargs` parameter is invoked with extra keyword arguments:
#   1. CPython captures all named arguments whose keys do not match any formal positional or keyword parameters.
#   2. It creates a new **mutable Dictionary object** on the heap.
#   3. It writes the argument names as string keys and their values as dictionary values.
#   4. The local variable `kwargs` is bound to this Dictionary object.
#   5. If no extra keyword arguments are passed, `kwargs` is bound to an empty dictionary `{}`.
# 
# ## 3. CALL-SITE UNPACKING
# - The `**` operator can be used at the **call site** of any function to unpack a dictionary mapping into distinct keyword arguments:
#   `configure(**{"port": 80, "host": "localhost"})` is equivalent to `configure(port=80, host="localhost")`.
# 
# ## 4. INTERVIEW QUESTIONS
# - **Q: What is the underlying type of the `kwargs` parameter inside the function?**
#   - *A*: It is a standard Python `dict` containing string keys corresponding to argument names.
# - **Q: What happens if you unpack a dictionary containing non-string keys using `**`?**
#   - *A*: Python raises a `TypeError: function() keywords must be strings`, since parameter names must be valid identifiers.
# 
# ---

# %%
# 1. Defining a function with **kwargs packing
def register_student(name, **kwargs):
    """Packs any extra keyword parameters into the 'kwargs' dict."""
    print(f"kwargs type: {type(kwargs).__name__} | values: {kwargs}")
    print(f"Student: {name}")
    for key, value in kwargs.items():
        print(f" -> {key}: {value}")

print("--- Calling with varying keyword arguments ---")
register_student("Alice", age=20, major="Computer Science")
# age and major are packed into the kwargs dict

print()
register_student("Bob")  # kwargs is empty dict: {}

# %%
# 2. Call-Site Dictionary Unpacking
def create_connection(ip, port, timeout=10):
    return f"Connecting to {ip}:{port} (timeout={timeout}s)"

config_map = {
    "ip": "10.0.0.1",
    "port": 8080,
    "timeout": 30
}

print("\n--- Call-Site Dictionary Unpacking ---")
# Unpacks config_map keys and values into the parameters
connection_str = create_connection(**config_map)
print(connection_str)  # Expected: "Connecting to 10.0.0.1:8080 (timeout=30s)"

# %%
# 3. Invalid Dictionary Keys (Non-string keys)
print("\n--- Testing Invalid Keyword Unpacking ---")
invalid_map = {
    "ip": "10.0.0.1",
    123: "port_value"  # Non-string key!
}

try:
    # Attempting to unpack dictionary with integer keys
    create_connection(**invalid_map)
except TypeError as e:
    print(f"Caught expected TypeError: {e}")
    # Expected: create_connection() keywords must be strings
