###############################################################################
# TOPIC: Structural Pattern Matching (match-case)
#
# 1. DEFINITION & INTRODUCTION:
#    - Structural Pattern Matching (introduced in Python 3.10 via PEP 634/635/636) is a
#      control flow mechanism matching structural patterns of objects (lists, dictionaries,
#      custom objects) rather than just testing values.
#    - Syntax uses two keywords: `match` and `case`.
#
# 2. PATTERNS AND FEATURES:
#    - Wildcard Pattern (`_`): Serves as the fallback default case matching anything (similar
#      to `default:` in switch-case).
#    - Sequence Destructuring: Matches lists, tuples, or arrays, checking lengths and pulling out
#      sub-components.
#      Example: `case [first, *rest]` captures the head element and remaining tail slice.
#    - Mapping Destructuring: Matches dictionaries by verifying key existence and binding values.
#      Example: `case {"status": status_code, "data": content}`. Extra keys in the dict are ignored.
#    - Class Pattern Matching: Matches custom objects, extracts attributes, and binds variables
#      positionally or by keyword.
#      Example: `case Point(x=x_val, y=y_val)`.
#    - OR Patterns (`|`): Combines multiple patterns.
#      Example: `case 200 | 201:`.
#    - Guards: Adds an `if` expression to a case check.
#      Example: `case x if x > 0:`.
#    - AS Patterns (`x as name`): Binds a matched pattern structure to a variable.
#      Example: `case [int(), int()] as coord:`.
#
# 3. COMPILER MECHANICS (CPython Internals):
#    - Under the hood, match-case compiles to optimized decision-tree bytecodes, making it
#      faster than writing multiple consecutive `isinstance` and key-lookups, as lookups
#      and validations are structured sequentially in C-level evaluations.
#
# 4. BEST PRACTICES:
#    - Use match-case to parse incoming JSON payloads, command parameters, or syntax tokens
#      instead of writing complex nested `if isinstance(data, dict): ...` trees.
#
# 5. INTERVIEW QUESTIONS:
#    - Q: What makes match-case different from standard switch-case statements in Java or C?
#      A: Match-case in Python is structural; it can validate object structures, destructure
#         inner elements, match types, check key existence in dictionaries, and bind matched values
#         to variables dynamically in local scopes.
#    - Q: Does a dictionary matching pattern like `case {"id": x}` check for exact dictionary match?
#      A: No, it only checks if the keys in the pattern exist in the dictionary. If the target dict
#         contains extra keys (e.g., `{"id": 1, "name": "Alice"}`), it still matches.
#
# 6. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement an AST node evaluator that processes math operations
#      represented as nested tuples (e.g. `("+", 5, ("*", 2, 3))`) using match-case recursion.
#
###############################################################################

# 1. Sequence Pattern Matching (Destructuring lists/tuples)
def process_command(command_payload):
    # Match the structure of the input command list
    match command_payload:
        case ["quit"]:
            return "System shutting down."
        case ["show", ("users" | "groups") as target]:
            # OR pattern combined with AS binding
            return f"Retrieving display list for target: {target}"
        case ["login", username, password]:
            return f"Logging in user: {username} with password size: {len(password)}"
        case ["write", *messages] if len(messages) > 0:
            # Sequence capturing with rest (*) operator and an IF guard
            return f"Writing {len(messages)} messages: {messages}"
        case _:
            # Wildcard default fallback case
            return "Invalid command layout received."

print("--- Sequence matching results ---")
print(process_command(["quit"]))
print(process_command(["show", "users"]))
print(process_command(["login", "likith", "secret_pass"]))
print(process_command(["write", "msg1", "msg2", "msg3"]))
print(process_command(["show", "invalid_section"]))  # Expected: fallback default

# 2. Dictionary/Mapping Pattern Matching
# Matches dictionary contents. Notice that extra keys in the dictionary are ignored.
def parse_api_response(response_dict):
    match response_dict:
        case {"status": "error", "error_code": code, "msg": message}:
            return f"API Failed. Error code: {code} | Details: {message}"
        case {"status": "success", "data": {"items": [first_item, *rest]}}:
            # Deep nested matching
            return f"API Success. Received {1 + len(rest)} items. First item: {first_item}"
        case _:
            return "Unknown api response format."

print("\n--- Mapping matching results ---")
print(parse_api_response({"status": "error", "error_code": 404, "msg": "Page not found", "timestamp": 12345}))
# Expected: matches first case (timestamp ignored)

print(parse_api_response({"status": "success", "data": {"items": ["apples", "bananas", "grapes"]}}))
# Expected: matches second case

# 3. Class Pattern Matching
# Matches custom objects and binds attributes.
class Point:
    # __match_args__ defines positional binding order for class patterns
    __match_args__ = ("x", "y")
    def __init__(self, x, y):
        self.x = x
        self.y = y

def classify_coordinate(point_obj):
    match point_obj:
        case Point(0, 0):
            # Positional matching matching Point(x=0, y=0)
            return "Origin point (0, 0)"
        case Point(x, 0):
            # Positional matching binding x
            return f"On the X axis at x={x}"
        case Point(0, y):
            # Positional matching binding y
            return f"On the Y axis at y={y}"
        case Point(x, y) if x == y:
            # Keyword/Positional matching combined with guard
            return f"On the diagonal y = x = {x}"
        case Point(x=x_val, y=y_val):
            # Explicit keyword argument matching
            return f"Arbitrary coordinate Point(x={x_val}, y={y_val})"
        case _:
            return "Not a valid Point object."

print("\n--- Class matching results ---")
print(classify_coordinate(Point(0, 0)))
print(classify_coordinate(Point(5, 0)))
print(classify_coordinate(Point(7, 7)))
print(classify_coordinate(Point(3, 4)))
