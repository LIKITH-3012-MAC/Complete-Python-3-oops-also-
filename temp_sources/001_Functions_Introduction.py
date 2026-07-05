# %% [markdown]
# # Topic: Functions Introduction - Functional paradigms, First-Class citizens, and Callables
# 
# ## 1. DEFINITION & MATHEMATICAL MAPPINGS
# - **Function**: A self-contained block of statements that performs a specific cohesive task.
# - **Mathematical mapping**: A function models a mapping from a set of inputs (Domain) to a set of outputs (Codomain/Range):
#   $$f: X \rightarrow Y$$
#   Where $X$ is the input domain and $Y$ is the range of output mappings.
# - **Determinism vs Side Effects**:
#   - **Pure Function**: Given the same input, it always returns the same output, and does not modify external state (no side effects).
#   - **Impure Function**: Modifies external states (writes to database, prints to console, changes global variables) or returns different results based on outside factors.
# 
# ## 2. WHY FUNCTIONS EXIST
# - **Modularity**: Breaking complex systems into small, independent, and testable components.
#   - *Fragility reduction*: Localizing bugs to single scopes.
# - **DRY (Don't Repeat Yourself)**: Eliminating redundant code blocks.
# - **Abstraction**: Hiding complex execution internals behind clean interfaces.
# 
# ## 3. PYTHON SPECIFIC: FUNCTIONS AS FIRST-CLASS CITIZENS
# - In Python, **everything is an object**, including functions!
# - "First-Class Citizen" means functions can be:
#   1. Assigned to variables (passed around as references).
#   2. Passed as arguments to other functions.
#   3. Returned from other functions.
#   4. Stored in container data structures (lists, dicts).
#   5. Augmented with custom attributes (since function instances have a `__dict__` dictionary!).
# 
# ## 4. TIME & SPACE COMPLEXITY
# - Calling a function introduces stack frame allocation overhead:
#   - **Time Complexity**: $O(1)$ constant overhead to create and pop a stack frame.
#   - **Space Complexity**: $O(1)$ frame memory cost, unless calling recursively ($O(N)$ stack space).
# 
# ## 5. INTERVIEW QUESTIONS
# - **Q: What does "First-Class Citizen" mean in Python?**
#   - *A*: It means functions are objects. They can be assigned to variables, passed as arguments, returned, and dynamically assigned attributes at runtime.
# - **Q: What is a pure function?**
#   - *A*: A function that has no side effects and always returns the exact same value for the same input arguments.
# 
# ---

# %%
# 1. Functions as First-Class Citizens: Variable Assignment
def greet(name):
    """Simple greeting function."""
    return f"Hello, {name}!"

# Assign function reference to another variable
say_hello = greet

print("--- Function Reference Assignment ---")
print(f"Calling say_hello('Alice'): {say_hello('Alice')}")
print(f"Id of greet:      {id(greet)}")
print(f"Id of say_hello: {id(say_hello)} | Match? {id(greet) == id(say_hello)}")

# %%
# 2. Passing Functions as Arguments (Higher-Order behavior)
def process_user(username, formatting_function):
    """Applies a formatting function to a username."""
    # Execute passed function reference
    formatted_name = formatting_function(username)
    return f"User processed: {formatted_name}"

def upper_case(text):
    return text.upper()

print("\n--- Passing Function as Argument ---")
# Pass 'upper_case' function reference as argument
output = process_user("likith", upper_case)
print(output)  # Expected: "User processed: LIKITH"

# %%
# 3. Dynamic Function Attributes (Functions have __dict__)
def calculate_area(width, height):
    return width * height

# Since functions are objects, we can attach attributes dynamically!
calculate_area.author = "Google Team"
calculate_area.calls_count = 0

def tracked_area(w, h):
    tracked_area.calls_count += 1
    return w * h

tracked_area.calls_count = 0

print("\n--- Dynamic Function Attributes ---")
print(f"calculate_area.author: {calculate_area.author}")
print(f"Function Namespace Dict: {calculate_area.__dict__}")

# Run tracked function
tracked_area(5, 5)
tracked_area(10, 20)
print(f"Total invocations tracked: {tracked_area.calls_count}")  # Expected: 2
