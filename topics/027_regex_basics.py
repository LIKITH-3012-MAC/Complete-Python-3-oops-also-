###############################################################################
# TOPIC: Text Processing - Regular Expressions (re)
#
# 1. DEFINITION & INTRODUCTION:
#    - Regular Expressions (regex) provide a powerful language for pattern matching and
#      text manipulation.
#    - Python implements regex through the built-in standard library module `re`.
#
# 2. CORE REGEX SYNTAX:
#    - Meta-characters:
#        - `.`: Matches any single character except newline.
#        - `^`: Matches start of the string (or line in MULTILINE mode).
#        - `$`: Matches end of the string.
#        - `*`: Matches 0 or more repetitions.
#        - `+`: Matches 1 or more repetitions.
#        - `?`: Matches 0 or 1 repetition (or makes quantifiers non-greedy/lazy).
#    - Character Classes:
#        - `\d`: Matches any digit (0-9). Equivalent to `[0-9]`.
#        - `\w`: Matches any alphanumeric character + underscore. Equivalent to `[a-zA-Z0-9_]`.
#        - `\s`: Matches whitespace characters (spaces, tabs, newlines).
#        - `[abc]`: Matches any character inside the set. `[^abc]` matches any character NOT in the set.
#    - Grouping:
#        - `(...)`: Captures a match group.
#        - `(?P<name>...)`: Captures a named group.
#
# 3. CORE re MODULE FUNCTIONS:
#    - `re.match(pattern, string)`: Checks for a match ONLY at the beginning of the string.
#      Returns a Match object or `None`.
#    - `re.search(pattern, string)`: Scans the entire string for the first match location.
#    - `re.findall(pattern, string)`: Returns all non-overlapping matches as a list of strings.
#    - `re.finditer(pattern, string)`: Returns an iterator yielding Match objects for all matches.
#    - `re.sub(pattern, replacement, string)`: Replaces matches with a specified string.
#    - `re.compile(pattern)`: Compiles a regex pattern into a reusable RegexObject.
#      Crucial for performance when reusing the same pattern repeatedly.
#
# 4. REGEX FLAGS:
#    - `re.IGNORECASE` (or `re.I`): Case-insensitive matching.
#    - `re.MULTILINE` (or `re.M`): Makes `^` and `$` match start/end of lines instead of string boundaries.
#    - `re.DOTALL` (or `re.S`): Makes the dot `.` match any character, including newlines.
#
# 5. TIME COMPLEXITY:
#    - Regex matching engines can run in O(N) time but can experience exponential O(2^N)
#      complexity (Catastrophic Backtracking) if a pattern contains nested, overlapping
#      quantifiers (e.g. `(a+)+$`) and is run against a long mismatching string.
#
# 6. BEST PRACTICES:
#    - Always define regex patterns using raw string literals (e.g. `r"\d+"`) to prevent
#      Python's compiler from parsing backslashes as string escape sequences.
#    - Pre-compile patterns using `re.compile()` if they are called inside loops.
#
# 7. INTERVIEW QUESTIONS:
#    - Q: What is the difference between `re.match()` and `re.search()`?
#      A: `re.match()` only checks if the pattern matches at the start of the string.
#         `re.search()` scans the entire string for a match anywhere.
#    - Q: How do you perform non-greedy (lazy) matching?
#      A: Append a `?` to the quantifier (e.g., `.*?` instead of `.*`).
#
# 8. EXERCISES & SOLUTIONS:
#    - Coding challenge: Parse an email address string, extract the username and domain
#      separately using capturing groups, and validate the format.
#
###############################################################################

import re  # Standard library module for regular expressions

# 1. re.match() vs re.search()
text = "The price of the item is 42 dollars."
pattern = r"\d+"  # Matches one or more digits

print("--- match() vs search() ---")
match_result = re.match(pattern, text)
print(f"re.match() result: {match_result}")  # Expected: None (Digits are not at the start of the string)

search_result = re.search(pattern, text)
print(f"re.search() result: {search_result}")  # Expected: Match object
if search_result:
    print(f"  Matched text: '{search_result.group()}' at range: {search_result.span()}")

# 2. Compiling Patterns & findall()
# We compile the pattern for optimal reuse.
email_text = "Contacts: info@example.com, support@company.org, admin@domain.net"
email_regex = re.compile(r"([a-zA-Z0-9._%+-]+)@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})")

print("\n--- Compile & findall() ---")
# findall returns list of tuples representing match groups
emails = email_regex.findall(email_text)
print(f"Found email groups: {emails}")

# 3. Using Named Groups and finditer()
# Named groups improve code readability when retrieving captured fields.
html_text = "<div class='container'>Hello World</div><span id='label'>Label text</span>"
html_regex = re.compile(r"<(?P<tag>\w+)[^>]*>(?P<content>[^<]+)</(?P=tag)>")

print("\n--- Named Groups and finditer() ---")
for match in html_regex.finditer(html_text):
    tag_name = match.group("tag")
    tag_content = match.group("content")
    print(f"Tag: <{tag_name}> | Content: '{tag_content}'")

# 4. Substitution (re.sub)
phone_text = "Phone numbers: 123-456-7890, 987-654-3210"
# Replace all digits with 'X' using re.sub
censored_text = re.sub(r"\d", "X", phone_text)
print("\n--- Substitution (re.sub) ---")
print(f"Original: {phone_text}")
print(f"Censored: {censored_text}")

# 5. Regex Flags (re.IGNORECASE and re.DOTALL)
multiline_text = "first line\nsecond line"
# Without DOTALL, the dot character '.' stops at the newline
print("\n--- Regex Flags ---")
print(f"Without DOTALL: {re.findall(r'line.second', multiline_text)}")  # Expected: []
print(f"With DOTALL:    {re.findall(r'line.second', multiline_text, flags=re.DOTALL)}")  # Expected: ['line\nsecond']
