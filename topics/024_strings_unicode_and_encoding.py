###############################################################################
# TOPIC: Strings, Unicode, Encoding/Decoding, and PEP 393 memory Representation
#
# 1. DEFINITION & INTRODUCTION:
#    - Python's `str` represents a sequence of Unicode characters. It is immutable.
#    - Characters vs Bytes:
#        - String (`str`): An abstract sequence of characters (e.g., text like "hello", "résumé", "🐍").
#        - Bytes (`bytes`): An immutable sequence of raw 8-bit integers (0-255) representing
#          binary data.
#
# 2. ENCODING AND DECODING:
#    - Encoding: Translating a string (characters) into a bytes object using a codec (e.g., UTF-8).
#      `string.encode(encoding, errors)`
#    - Decoding: Translating a bytes object back into a string.
#      `bytes.decode(encoding, errors)`
#    - Popular codecs:
#        - ASCII: Limited to 128 characters (0-127). Cannot represent non-English symbols.
#        - UTF-8: A variable-length encoding (1 to 4 bytes per character). Backward compatible
#          with ASCII. The de facto standard for web and Python 3 source code.
#        - UTF-16 / UTF-32: Fixed/variable double-byte and quad-byte systems.
#
# 3. CODEC ERROR HANDLERS:
#    When encoding or decoding incompatible characters, you can choose an error policy:
#    - `strict` (default): Raises a `UnicodeEncodeError` or `UnicodeDecodeError`.
#    - `ignore`: Discards the invalid characters and continues.
#    - `replace`: Replaces invalid characters with a marker (e.g., `?` or Unicode replacement character `\ufffd`).
#    - `backslashreplace`: Replaces invalid bytes with backslashed hex escape sequences.
#
# 4. CPYTHON PEP 393 FLEXIBLE STRING REPRESENTATION (Crucial Internals):
#    - In Python 3.0-3.2, Python used a build option for Unicode: UCS-2 (2 bytes per character)
#      or UCS-4 (4 bytes per character). This was highly inefficient (e.g., "abc" took 12 bytes of character storage).
#    - Python 3.3 introduced PEP 393, optimizing string memory layout dynamically.
#    - Under PEP 393, CPython uses 3 distinct structures depending on the maximum code point in the string:
#        1. ASCII / Latin-1 (1 byte per char): If all characters are < 256.
#           Example: `"hello"` uses 1 byte per character.
#        2. UCS-2 (2 bytes per char): If the maximum code point is between 256 and 65535.
#           Example: `"résumé"` containing 'é' (code point 233) fits in Latin-1, but if it has Cyrillic `"привет"` it uses 2 bytes per character.
#        3. UCS-4 (4 bytes per char): If the maximum code point is >= 65536 (e.g., emojis).
#           Example: `"hello 🐍"` containing '🐍' (code point 128013) promotes the entire string storage to 4 bytes per character.
#    - A string is unified; checking its length `len()` always returns the number of logical characters,
#      not byte length!
#
# 5. TIME & SPACE COMPLEXITY:
#    - Slicing: O(K) where K is slice size.
#    - Length check: O(1) time complexity. CPython caches the string length inside the header struct.
#
# 6. INTERVIEW QUESTIONS:
#    - Q: Explain CPython PEP 393 string layout optimization.
#      A: CPython dynamically alters the byte width of characters in a string object header
#         to be 1, 2, or 4 bytes, depending on the highest Unicode code point in that string,
#         drastically reducing memory usage for Western languages while still supporting full Unicode.
#    - Q: What is the difference between `encode()` and `decode()`?
#      A: `encode()` is called on a `str` to produce binary `bytes`.
#         `decode()` is called on `bytes` to produce a Unicode `str`.
#
# 7. EXERCISES & SOLUTIONS:
#    - Coding challenge: Write a function that takes a string, reports its unicode character
#      count, its UTF-8 byte length, and its estimated CPython PEP 393 byte width per character.
#
###############################################################################

import sys  # Standard library to inspect string memory sizes and internals

# 1. Bytes vs Str Comparison
unicode_str = "hello 🐍"
utf8_bytes = unicode_str.encode("utf-8")

print("--- Str vs Bytes ---")
print(f"str representation: {unicode_str} | len (characters): {len(unicode_str)}")
print(f"bytes representation: {utf8_bytes} | len (bytes): {len(utf8_bytes)}")
# Emojis like 🐍 occupy 4 bytes in UTF-8. Total UTF-8 bytes: 6 (hello ) + 4 (snake) = 10 bytes.

# 2. Codec Error Handling Policies
print("\n--- Codec Error Policies ---")
bad_str = "résumé"
# ASCII cannot represent 'é'
try:
    bad_str.encode("ascii", errors="strict")
except UnicodeEncodeError as e:
    print(f"strict error: {e}")

print(f"ignore:          {bad_str.encode('ascii', errors='ignore')}")  # Returns b'rsum'
print(f"replace:         {bad_str.encode('ascii', errors='replace')}")  # Returns b'r?sum?'
print(f"backslashreplace: {bad_str.encode('ascii', errors='backslashreplace')}")  # Returns b'r\\xe9sum\\xe9'

# 3. PEP 393 Flexible String Representation Proof
# We will create strings of identical length but containing characters of different code points,
# then inspect their sizes using sys.getsizeof() to see character size expansion.
# The base overhead of a compact string header on 64-bit platforms is around 48-80 bytes.
str_latin1 = "abcdefghij"  # 10 characters, maximum code point < 256 (Latin-1)
str_ucs2 = "abcпривеth"    # 10 characters, contains Russian letters (maximum code point < 65536)
str_ucs4 = "abc🐍fghij"    # 10 characters, contains an emoji (maximum code point >= 65536)

size_latin1 = sys.getsizeof(str_latin1)
size_ucs2 = sys.getsizeof(str_ucs2)
size_ucs4 = sys.getsizeof(str_ucs4)

print("\n--- PEP 393 Memory Footprint Proof ---")
print(f"Latin-1 string size (1 byte/char):  {size_latin1} bytes")
print(f"UCS-2 string size (2 bytes/char):   {size_ucs2} bytes")
print(f"UCS-4 string size (4 bytes/char):   {size_ucs4} bytes")
# Notice how the size increments. UCS-2 is larger than Latin-1, and UCS-4 is larger than UCS-2.

# 4. Characters to Code Points
print("\n--- Code Point Inspection ---")
for char in ["a", "é", "п", "🐍"]:
    # ord(char) returns the integer code point value
    # chr(code_point) converts code point back to character
    print(f"Character: '{char}' | Code Point: {ord(char):<7} | Hex: {hex(ord(char))}")
