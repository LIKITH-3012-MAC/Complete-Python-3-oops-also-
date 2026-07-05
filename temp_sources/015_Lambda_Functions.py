# %% [markdown]
# # Topic: Lambda Functions - Anonymous definitions, single-expression constraints, and lexical binding
# 
# ## 1. DEFINITION & SYNTAX
# - **Lambda Function**: An anonymous (unnamed) inline function defined using the `lambda` keyword.
# - **Syntax**:
#   `lambda param1, param2: expression`
# - **Evaluation**: Evaluates the expression and implicitly returns the resulting value.
# 
# ## 2. COMPILATION & CONSTRAINTS
# - **CPython Mechanics**:
#   - Under the hood, lambda expressions compile to a standard **Code Object** and create a **Function Object** at runtime, identical to functions defined using `def`.
#   - Their name identifier is statically set to `<lambda>`.
# - **Syntax Constraints**:
#   1. **Single Expression**: Can only contain a single logical expression. Statements (e.g. `pass`, `assert`, assignments like `x = 5`, or print statements in Python 2) are syntax violations.
#   2. **No Multi-line Blocks**: Cannot span multiple statements or contain loops/conditionals (except for conditional expressions like `x if condition else y`).
# 
# ## 3. LEXICAL BINDING & SCOPE
# - Lambdas capture variables from their enclosing scope at runtime, adhering to standard LEGB scope resolution rules.
# - **Late Binding**: Just like regular functions, variables inside lambda expressions are resolved when the lambda is called, not when it is defined.
# 
# ## 4. PEP 8 AND ANTI-PATTERNS
# - **PEP 8 Guideline**: Do not assign lambdas directly to variables (e.g., `square = lambda x: x * x` is an anti-pattern). Use a named `def` instead.
# - *Reason*: Named `def` statements provide clean stack traces with proper function names during debugging, whereas lambdas appear anonymously as `<lambda>`.
# 
# ## 5. INTERVIEW QUESTIONS
# - **Q: Can a lambda function contain multiple statements?**
#   - *A*: No. The Python parser strictly restricts lambdas to a single returnable expression.
# - **Q: What is the main difference between a lambda and a def function in Python?**
#   - *A*: Syntactically, lambdas are inline anonymous expressions restricted to a single expression. Under the hood, they generate standard function objects identical to `def` definitions.
# 
# ---

# %%
# 1. Standard Lambda vs def Comparison
# Regular def
def multiply(x, y):
    return x * y

# Equivalent lambda (Note: assigning to variable is for demo only!)
multiply_lambda = lambda x, y: x * y

print("--- Calling Lambda vs def ---")
print(f"multiply(5, 6):        {multiply(5, 6)}")
print(f"multiply_lambda(5, 6): {multiply_lambda(5, 6)}")

# Names comparison
print(f"Def function name:    {multiply.__name__}")        # Expected: 'multiply'
print(f"Lambda function name: {multiply_lambda.__name__}") # Expected: '<lambda>'

# %%
# 2. Sorting using Lambda: The primary valid use-case
users = [
    {"name": "Alice", "score": 88},
    {"name": "Bob", "score": 95},
    {"name": "Charlie", "score": 78}
]

print("\n--- Sorting using Lambda keys ---")
# Sort dict items by the 'score' key inline
users.sort(key=lambda u: u["score"])
print(f"Sorted users: {users}")

# %%
# 3. Late Binding Trap in Lambdas
print("\n--- Late Binding demonstration ---")
# Create a list of lambda functions returning i
funcs = [lambda: i for i in range(3)]

# What will these lambdas return?
# Because 'i' is resolved at call time (late binding), and 'i' finished at 2:
print(f"Lambda 0: {funcs[0]()}")  # Expected: 2 (Not 0!)
print(f"Lambda 1: {funcs[1]()}")  # Expected: 2
print(f"Lambda 2: {funcs[2]()}")  # Expected: 2

# The Fix: Use default arguments to bind value immediately at definition time
fixed_funcs = [lambda x=i: x for i in range(3)]
print(f"Fixed Lambda 0: {fixed_funcs[0]()}")  # Expected: 0
print(f"Fixed Lambda 1: {fixed_funcs[1]()}")  # Expected: 1
print(f"Fixed Lambda 2: {fixed_funcs[2]()}")  # Expected: 2
