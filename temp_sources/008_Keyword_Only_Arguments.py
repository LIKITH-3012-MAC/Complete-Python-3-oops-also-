# %% [markdown]
# # Topic: Keyword-Only Arguments - PEP 3102, asterisk syntax (*), and configuration interfaces
# 
# ## 1. DEFINITION & SYNTAX
# - **Keyword-Only Arguments**: Parameters that can only be filled by keyword arguments during calls, preventing them from being filled positionally.
# - **Syntax (PEP 3102 - Python 3.0+)**:
#   - Defined using an asterisk `*` symbol in the parameter list.
#   - All parameters declared **after the asterisk `*`** (or after `*args`) must be passed strictly as keyword arguments.
#   - Example:
#     ```python
#     def write_log(message, *, level="INFO", formatter=None):
#         pass
#     ```
#     Here, `message` is positional/keyword, while `level` and `formatter` are keyword-only.
# 
# ## 2. WHY PYTHON INTRODUCED IT
# 1. **Preventing API Mistakes**: Ensures callers explicitly name configurations (like flags or mode strings) instead of passing raw booleans positionally (e.g. `send_data("data", True, False)` is hard to read; `send_data("data", secure=True, zip=False)` is highly readable).
# 2. **Refactoring Safety**: Allows developers to add configuration options to signatures without breaking positional compatibility for existing callers.
# 
# ## 3. INTERVIEW QUESTIONS
# - **Q: What is the purpose of the naked `*` in a Python function signature?**
#   - *A*: It acts as a barrier separator. Every parameter defined after `*` must be passed exclusively as a keyword argument.
# - **Q: What happens if you try to pass a keyword-only argument positionally?**
#   - *A*: Python raises a `TypeError: function() takes X positional arguments but Y were given` or specifically indicating positional mapping overflows.
# 
# ---

# %%
# 1. Defining a function with keyword-only parameters
def connect_db(hostname, port=5432, *, username, password):
    """hostname and port are positional/keyword, username and password are keyword-only."""
    return f"Connecting to {hostname}:{port} as {username} (PW: {'*' * len(password)})"

print("--- Valid Invocation ---")
# Passing username and password as keyword arguments
output1 = connect_db("localhost", username="root", password="super_secret_password")
print(output1)

# %%
# 2. Violating Keyword-Only constraint
print("\n--- Testing Violations ---")
try:
    # Attempting to pass username and password positionally!
    # CPython counts this as trying to pass 4 positional arguments to a function that only accepts 2 positionally.
    connect_db("localhost", 5432, "root", "super_secret_password")
except TypeError as e:
    print(f"Caught expected TypeError: {e}")
    # Expected: connect_db() takes from 1 to 2 positional arguments but 4 were given

# %%
# 3. Keyword-only parameters after *args packing
def aggregate_values(*args, multiplier=1):
    """multiplier is a keyword-only argument placed after variable positional argument *args."""
    total = sum(args) * multiplier
    return total

print("\n--- Keyword-only after *args execution ---")
# Pass positional numbers to *args, and multiplier by keyword
val1 = aggregate_values(1, 2, 3, 4, multiplier=10)
print(f"aggregate_values(1, 2, 3, 4, multiplier=10): {val1}")  # Expected: 100

val2 = aggregate_values(1, 2, 3, 4)
print(f"aggregate_values(1, 2, 3, 4) (default multiplier=1): {val2}")  # Expected: 10
