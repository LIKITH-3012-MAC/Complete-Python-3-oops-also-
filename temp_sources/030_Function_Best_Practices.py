# %% [markdown]
# # Topic: Function Best Practices - PEP 8/257 standards, Single Responsibility, and parameter design limits
# 
# ## 1. PEP 8 AND PEP 257 STANDARDS
# - **PEP 8 Function Rules**:
#   - Name functions using lowercase words separated by underscores (`snake_case`).
#   - Separate function definitions in a module by exactly **two blank lines**.
#   - Use default spacing around parameter assignments only when type annotations are absent: `def func(x=10):` vs `def func(x: int = 10):`.
# - **PEP 257 Docstring Rules**:
#   - Always wrap docstrings in triple double quotes `"""`.
#   - Write a summary line ending in a period.
#   - For multi-line docstrings, write the summary, followed by a blank line, followed by detailed descriptions of parameters (Args), return values (Returns), and exceptions (Raises).
# 
# ## 2. ARCHITECTURAL DESIGN PATTERNS
# - **Single Responsibility Principle (SRP)**: A function should do exactly **one thing** and do it well. If a function is complex, break it into smaller helper functions.
# - **Parameter Count Limits**:
#   - Keep parameters to a minimum (ideally $\le 3$, maximum $5$).
#   - If a function requires more than 5 arguments, it is an anti-pattern showing the function is doing too much. Refactor by grouping related arguments into a data structure (like a `dataclass` or custom class).
# - **Purity & State Mutation**: Prefer pure functions. Avoid mutating global variables or caller objects unless explicitly intended by design.
# 
# ## 3. INTERVIEW QUESTIONS
# - **Q: What are the main recommendations of PEP 257?**
#   - *A*: Use triple double quotes for all docstrings, end the summary in a period, use a blank line after the summary to separate details, and document arguments, returns, and raised exceptions.
# - **Q: How do you handle functions that require too many arguments?**
#   - *A*: Group related arguments into structured objects (like a dictionary, namedtuple, or dataclass) to simplify signature interfaces and improve readability.
# 
# ---

# %%
from dataclasses import dataclass

# 1. Anti-Pattern: Monolithic function with too many arguments doing multiple tasks
def bad_register_user(username, email, password, address_line1, city, zipcode, country, send_email=True):
    # This violates SRP: it processes details, validates addresses, and dispatches notifications
    print("Processing registration...")
    print(f"Creating user {username} and sending email: {send_email}")
    return f"User {username} created."

# 2. Refactored Solution: Group arguments using Dataclasses & Separation of Concerns (SRP)
@dataclass
class Address:
    line1: str
    city: str
    zipcode: str
    country: str

@dataclass
class UserConfig:
    username: str
    email: str
    password: str
    address: Address

def send_welcome_email(email):
    """Sends welcome email alert to the user."""
    print(f" -> [SRP] Welcome email dispatched to {email}")

def create_user_profile(user_config: UserConfig):
    """Registers a new user profile database entry.
    
    Args:
        user_config: A UserConfig dataclass instance containing user info.
        
    Returns:
        str: A string summary of creation.
    """
    # Does exactly one thing: creates database record log
    print(f" -> [SRP] DB entry created for {user_config.username}")
    return f"User {user_config.username} Registered successfully."

print("--- Clean Code Execution (SRP) ---")
user_addr = Address("123 Main St", "Sunnyvale", "94085", "USA")
config = UserConfig("likith_naidu", "likith@example.com", "secure123", user_addr)

# Execute isolated SRP functions sequentially
db_result = create_user_profile(config)
send_welcome_email(config.email)
print(db_result)
