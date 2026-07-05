# %% [markdown]
# # Topic: Coroutines - Generator-based consumers, priming decorators, and data pipelines
# 
# ## 1. DEFINITION: COROUTINES AS CONSUMERS
# - While standard generators are **producers** (they yield data to the caller), generator-based **Coroutines** operate primarily as **consumers** (they pull data pushed from the caller using `send()`).
# - **Structure**:
#   - Contain a loop that suspends execution at a `yield` expression to consume incoming values:
#     ```python
#     def consumer():
#         while True:
#             data = yield  # Suspends here, waiting for caller to push data via send(data)
#     ```
# 
# ## 2. AUTOMATIC PRIMING DECORATOR
# - Since coroutines must be primed before receiving a non-`None` value, writing `next(coro)` manually on every instantiation is error-prone.
# - **The Solution**: Create a `@coroutine` decorator that wraps the coroutine constructor, instantiates the generator, calls `next()` to advance it to the first `yield`, and returns the primed coroutine ready for immediate `.send()` actions.
# 
# ## 3. DATA PIPELINES
# - Coroutines can be linked together to build powerful, memory-efficient data processing pipelines (similar to UNIX pipes).
# - A source pushes values to a filter coroutine, which filters data and pushes it to a sink (final consumer).
# 
# ## 4. INTERVIEW QUESTIONS
# - **Q: What is the difference between a generator and a coroutine in Python?**
#   - *A*: A generator produces values for the caller using `yield value`. A coroutine consumes values sent by the caller using `value = yield`.
# - **Q: Why do coroutines require priming?**
#   - *A*: Because the execution must run from the start of the function body to the first `yield` expression where the coroutine suspends and becomes capable of receiving data.
# 
# ---

# %%
import functools

# 1. Automatic Priming Decorator
def coroutine(func):
    """Decorator that automatically primes a generator-based coroutine."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        coro = func(*args, **kwargs)
        next(coro)  # Prime the coroutine
        return coro
    return wrapper

# 2. Coroutine Consumer Definition
@coroutine
def print_logger(prefix):
    """Coroutine consumer that prints received log entries containing errors."""
    print(f"[{prefix}] Logger initialized and waiting for logs...")
    try:
        while True:
            # Suspend and consume incoming string
            log_line = yield
            if "ERROR" in log_line:
                print(f"[{prefix}] MATCH FOUND: {log_line}")
    except GeneratorExit:
        print(f"[{prefix}] Logger shutting down...")

print("--- Initializing Coroutine ---")
logger = print_logger("App-Monitor")
# Note: "Logger initialized" was printed immediately because of our priming decorator!

# %%
# 3. Pushing data to the coroutine
print("\n--- Sending Logs to Coroutine ---")
logger.send("INFO: User login successful")
logger.send("ERROR: Connection timed out")  # Expected: MATCH FOUND print
logger.send("WARN: CPU usage high")
logger.send("ERROR: Database write failed")  # Expected: MATCH FOUND print

# Shutdown the coroutine
logger.close()

# %%
# 4. Building a Pipeline: Source -> Filter -> Sink
@coroutine
def filter_even(target):
    """Filters even numbers and pushes them to target."""
    while True:
        num = yield
        if num % 2 == 0:
            target.send(num)

@coroutine
def sum_sink():
    """Aggregates and sums up all received numbers."""
    total = 0
    try:
        while True:
            num = yield
            total += num
            print(f" -> Current cumulative sum: {total}")
    except GeneratorExit:
        print(f" -> Pipeline Closed. Final sum: {total}")

print("\n--- Running a Data Processing Pipeline ---")
sink = sum_sink()
filter_coro = filter_even(sink)

# Feed numbers into the start of the pipeline
for val in [1, 2, 3, 4, 5, 6]:
    filter_coro.send(val)

# Close pipeline
filter_coro.close()
sink.close()
