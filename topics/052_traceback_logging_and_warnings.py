###############################################################################
# TOPIC: Traceback Inspection, standard logging, and the warnings Framework
#
# 1. DEFINITION & INTRODUCTION:
#    - Traceback: A report detailing the active stack frames during an exception trace.
#    - Logging: Standardized diagnostic recording (`logging` module), replacing print statements
#      with severity levels, structured routing, and file exports.
#    - Warnings: Non-fatal signals highlighting developer issues (e.g. deprecation notices)
#      without terminating execution. Managed via the `warnings` module.
#
# 2. TRACEBACK INSPECTION (`traceback` module):
#    - Allows capturing, formatting, and printing exception stack traces programmatically.
#    - Useful when writing custom crash log files or sending diagnostic reports.
#
# 3. STANDARD LOGGING SYSTEM:
#    - Severity Levels (increasing order): `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`.
#    - Components:
#        - Loggers: The application interface (e.g. `logging.getLogger()`).
#        - Handlers: Direct logs to destinations (console via `StreamHandler`, files via `FileHandler`).
#        - Formatters: Layout styling of logs (adding timestamps, line numbers, log levels).
#    - Logging Exceptions: Calling `logger.error("msg", exc_info=True)` automatically extracts
#      the active exception and appends its complete traceback trace to the log message.
#
# 4. WARNINGS FRAMEWORK:
#    - Warnings highlight code smells or API deprecations.
#    - Unlike exceptions, warnings do not halt program flow by default.
#    - Categories: `DeprecationWarning`, `UserWarning`, `SyntaxWarning`, `RuntimeWarning`.
#    - Filter actions (configurable via command-line `-W` or `warnings.filterwarnings()`):
#        - `default`: Print warning.
#        - `ignore`: Silent warning.
#        - `error`: Promote warning to an exception, raising it and halting execution.
#
# 5. INTERVIEW QUESTIONS:
#    - Q: How do you log an exception along with its stack traceback?
#      A: By calling a logging method (like `logger.error()`) and passing `exc_info=True`
#         or calling `logger.exception("message")` which has `exc_info=True` set implicitly.
#    - Q: How do you configure warnings to raise exceptions and fail tests?
#      A: Run Python with the `-W error` command-line switch or execute `warnings.filterwarnings("error")`
#         inside the application startup code.
#
# 6. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a function that triggers a warning, catch it using a warnings
#      filter, log it as an error to an in-memory stream, and print the resulting traceback.
#
###############################################################################

import traceback  # Standard module to inspect stack traces
import logging  # Standard logging framework
import warnings  # Standard warning controls
import io  # In-memory text stream helper

# 1. Traceback Inspection Demonstration
def function_c():
    raise KeyError("Target key missing from database records")

def function_b():
    function_c()

def function_a():
    function_b()

print("--- Traceback Formatting & Capture ---")
try:
    function_a()
except KeyError as e:
    # Capture the exception traceback
    tb_string = traceback.format_exc()
    print("Formatted Stack Traceback:")
    print(tb_string)

# 2. Standard Logging Setup & Handler routing
# We configure a logger that writes to a memory buffer to inspect the output.
log_stream = io.StringIO()
logger = logging.getLogger("AppDiagnosticLogger")
logger.setLevel(logging.DEBUG)

# Create stream handler targeting our log_stream buffer
stream_handler = logging.StreamHandler(log_stream)
# Define formatting layout
formatter = logging.Formatter("[%(levelname)s] [%(name)s] - %(message)s")
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

print("--- Logging Demonstration ---")
logger.info("Application successfully initialized.")
logger.warning("Resource utilization exceeding 80%.")

try:
    # Force a failure and log it
    1 / 0
except ZeroDivisionError:
    # logger.exception automatically captures active traceback (exc_info=True)
    logger.exception("An arithmetic error occurred!")

# Flush and display log output
stream_handler.flush()
print("\nLogged Records inside buffer:")
print(log_stream.getvalue())

# 3. Warnings Framework (User Warnings and Deprecations)
def legacy_calculation_api(x):
    # Warn the user that this API is outdated
    warnings.warn(
        "legacy_calculation_api is deprecated. Use math_utils.calculate instead.",
        category=DeprecationWarning,
        stacklevel=2  # Reports warning location from caller's stack frame
    )
    return x * 10

print("--- Warnings Behavior ---")
# Configure warnings filter to display DeprecationWarning (often ignored by default in REPLs)
warnings.filterwarnings("default", category=DeprecationWarning)
legacy_calculation_api(5)  # Expected: prints warning message

# Promotes warnings to exceptions
warnings.filterwarnings("error", category=DeprecationWarning)
try:
    print("\nAttempting to call legacy API with warning promoted to exception:")
    legacy_calculation_api(5)
except DeprecationWarning as e:
    print(f"Caught warning promoted to exception: {e}")

# Restore warnings default state
warnings.resetwarnings()
