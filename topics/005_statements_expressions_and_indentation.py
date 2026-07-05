###############################################################################
# TOPIC: Statements, Expressions, and Indentation Rules
#
# 1. DEFINITION & INTRODUCTION:
#    - Expression: A unit of code that is evaluated by the interpreter to produce
#      a value. Every expression has a value and a type.
#      Examples: `5 + 3`, `len("hello")`, `x > 10`.
#    - Statement: A unit of code that performs an action or represents a structural
#      command. Statements do not necessarily evaluate to a value.
#      Examples: assignment statements (`x = 5`), control flow (`if x: pass`),
#      import statements (`import sys`).
#    - Python programs are constructed of statements, which are composed of expressions.
#
# 2. SIMPLE VS COMPOUND STATEMENTS:
#    - Simple Statements: Contained within a single logical line (e.g., assignment,
#      assert, return, break, continue, import, pass).
#    - Compound Statements: Contain other statements and span multiple lines. They
#      consist of one or more 'clauses' (e.g., `if`, `for`, `while`, `try`, `def`, `class`).
#      Each clause starts with a header line ending with a colon `:` and is followed
#      by an indented block of code (suite).
#
# 3. INDENTATION MECHANICS:
#    - Unlike languages that use curly braces `{}` or keywords (`begin`/`end`) to
#      delimit blocks, Python uses indentation (whitespace leading a line).
#    - Standard style: 4 spaces per indentation level.
#    - Tabs and spaces must not be mixed. Mixing them leads to a `TabError` at compile
#      time.
#
# 4. INTERNAL IMPLEMENTATION & CPYTHON LEXER:
#    - The CPython compiler tracks indentation using a stack during tokenization.
#    - When the lexer encounters an increase in indentation at the beginning of a
#      line, it pushes the new indentation level (number of spaces) onto the stack
#      and generates an `INDENT` token.
#    - When the indentation level decreases, the lexer pops values from the stack until
#      it matches the new level, generating a `DEDENT` token for each popped level.
#    - When the lexer reaches the end of the file, it generates `DEDENT` tokens for
#      any remaining levels on the stack.
#
# 5. LINE CONTINUATION:
#    - Python lines are usually terminated by a newline. However, you can write
#      multi-line statements using two methods:
#      1. Implicit Line Continuation: Statements inside parentheses `()`, brackets `[]`,
#         or braces `{}` can span multiple lines without explicit markers. This is the
#         recommended approach.
#      2. Explicit Line Continuation: Using a backslash `\` as the last character of
#         a line to continue the statement onto the next line.
#
# 6. TIME & SPACE COMPLEXITY:
#    - Lexing indentation is O(N) where N is the length of the source file.
#    - Indentation stack depth is bounded by the maximum nesting depth of compound
#      statements, which uses minimal memory (space complexity is O(D) where D is
#      nesting depth).
#
# 7. COMMON PITFALLS & CODE SMELLS:
#    - `IndentationError`: Caused by mismatched spaces or inconsistent indent levels.
#    - `TabError`: Triggered when tabs and spaces are mixed in the same file.
#    - Misusing explicit line continuation `\`. A single whitespace character after
#      the backslash will cause a `SyntaxError: unexpected character after line continuation character`.
#
# 8. INTERVIEW QUESTIONS:
#    - Q: What is the difference between an expression and a statement?
#      A: An expression evaluates to a value (e.g., `a + b`); a statement performs
#         an action or execution flow (e.g., `if a > b:`).
#    - Q: How does CPython tokenize indentation?
#      A: The lexer tracks leading whitespace levels using a stack, emitting `INDENT`
#         and `DEDENT` tokens as the indentation levels change.
#
# 9. EXERCISES & SOLUTIONS:
#    - Debugging challenge: Identify the error in a multi-line list definition containing
#      an accidental backslash whitespace.
#
###############################################################################

import token  # Module containing constants representing token numbers
import tokenize  # Module to perform lexical analysis on Python source files
import io  # Input/output streams to process strings as file streams

# 1. Expressions vs Statements Demonstration
# 'x = 10 + 20' is an assignment statement.
# '10 + 20' is an expression evaluated to 30.
x = 10 + 20  # Statement containing expression
print(f"Statement executed, x is {x}")

# 2. Line Continuation Methods
# Method A: Implicit Continuation (Preferred PEP 8)
# Parentheses allow clean formatting across lines.
implicit_list = [
    "element_one",
    "element_two",
    "element_three"
]
print(f"Implicit continuation list: {implicit_list}")

# Method B: Explicit Continuation (Using backslash)
# No characters, including comments or spaces, can follow the backslash.
explicit_string = "This is a long string that is split " \
                  "across multiple lines explicitly."
print(f"Explicit continuation string: {explicit_string}")

# 3. Simulate CPython Lexer Indentation Tokens
# We will tokenize a sample string of code containing blocks to observe INDENT/DEDENT tokens.
code_sample = """
def my_func():
    a = 1
    if a > 0:
        a += 1
"""

print("\n--- Lexer Tokenization of Indentation ---")
# Convert string to a bytes generator as required by tokenize.tokenize
code_bytes = io.BytesIO(code_sample.encode('utf-8'))

# Read tokens from the string
for tok in tokenize.tokenize(code_bytes.readline):
    # Filter only relevant tokens: INDENT, DEDENT, and NAME
    token_name = token.tok_name[tok.exact_type]
    if token_name in ("INDENT", "DEDENT", "NAME"):
        # Prints token type, the string value, and its line/column ranges
        print(f"Token: {token_name:<10} | Value: {repr(tok.string):<15} | Range: {tok.start} to {tok.end}")
