# %% [markdown]
# # Topic: Keyword Arguments - Name mapping, order rules, and duplicate assignment errors
# 
# ## 1. DEFINITION & SYNTAX
# - **Keyword Arguments**: Arguments passed to a function call prefixed by parameter name identifiers:
#   `describe_user(age=25, status="active")`
# - **Name Mapping**: Python maps arguments to parameters by matching strings, allowing arguments to be passed in any order.
# 
# ## 2. PARAMETER ORDER CONSTRAINTS
# - **Ordering Rule**: Positional arguments must always be specified **before** keyword arguments in the function invocation line.
#   - Writing `describe_user(age=25, "Alice")` raises a `SyntaxError: positional argument follows keyword argument`.
# - **No Duplicate Assignment**: A keyword argument cannot duplicate a parameter value that has already been filled positionally.
#   - Writing `describe_user("Alice", name="Bob")` raises a `TypeError: describe_user() got multiple values for argument 'name'`.
# 
# ## 3. INTERVIEW QUESTIONS
# - **Q: What happens if you specify a positional argument after a keyword argument in a function call?**
#   - *A*: Python's compiler parser raises a `SyntaxError: positional argument follows keyword argument` before execution starts.
# - **Q: Can you pass a keyword argument that maps to a positional-only parameter?**
#   - *A*: In modern Python, no. Doing so raises a `TypeError` (covered in detail in the Positional-Only Arguments topic).
# 
# ---

# %%
# 1. Standard Function with multiple parameters
def configure_device(device_id, ip_address, port=80, secure=True):
    """Prints configuration summary."""
    return f"Device {device_id} | IP: {ip_address} | Port: {port} | SSL: {secure}"

print("--- Calling using Keyword Arguments ---")
# Order does not matter when using keyword arguments
output1 = configure_device(port=443, ip_address="192.168.1.1", device_id="Alpha")
print(f"Keyword Order A: {output1}")

output2 = configure_device(device_id="Beta", secure=False, ip_address="10.0.0.5")
print(f"Keyword Order B: {output2}")

# %%
# 2. Syntax Violations: Positional follows Keyword
print("\n--- Syntax Violation (Positional follows Keyword) ---")
# We compile this via eval or dynamic string execution to capture SyntaxError without crashing compilation
try:
    exec("configure_device(device_id='Alpha', '192.168.1.1')")
except SyntaxError as e:
    print(f"Caught expected SyntaxError: {e}")

# %%
# 3. Type Violations: Duplicate Assignment
print("\n--- Type Violation (Duplicate Assignment) ---")
try:
    # 'Alpha' occupies the first parameter position (device_id)
    # Then we explicitly assign device_id again using keyword notation!
    configure_device("Alpha", "192.168.1.1", device_id="Beta")
except TypeError as e:
    print(f"Caught expected TypeError: {e}")
    # Expected: got multiple values for argument 'device_id'
