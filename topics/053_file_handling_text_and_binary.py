###############################################################################
# TOPIC: File I/O - Text and Binary modes, Buffering, and seek/tell pointers
#
# 1. DEFINITION & INTRODUCTION:
#    - Python handles files by creating file-like streams using the built-in `open()` function.
#    - Open Modes:
#        - `r`: Read (default). Error if file missing.
#        - `w`: Write. Truncates file. Creates file if missing.
#        - `a`: Append. Writes to the end. Creates file if missing.
#        - `x`: Exclusive creation. Fails if the file already exists (preventing overwrite).
#        - `+`: Open for updating (read/write).
#        - `t`: Text mode (default). Automatically decodes bytes using specified encoding.
#        - `b`: Binary mode. Returns raw bytes objects; no encoding or newline normalization.
#
# 2. TEXT I/O VS BINARY I/O:
#    - Text Mode (`t`): Translates platform-specific line endings (e.g., Windows `\r\n` vs Unix `\n`)
#      to simple `\n` (Universal Newlines).
#    - Binary Mode (`b`): Leaves data completely unaltered. Essential for image, audio, zip,
#      or serialized data files.
#
# 3. BUFFERING:
#    - You can configure the `buffering` argument of `open()`:
#        - `0`: Unbuffered (valid in binary mode only). Writing instantly calls the OS write.
#        - `1`: Line-buffered (valid in text mode only). Flushes when a newline is written.
#        - `> 1`: Block-buffered with the specified buffer size in bytes.
#
# 4. FILE OFFSET NAVIGATION (`seek` and `tell`):
#    - `tell()`: Returns an integer indicating the current file pointer position in bytes
#      from the beginning of the file.
#    - `seek(offset, whence=0)`: Moves the file pointer offset:
#        - `whence=0` (default): Offset relative to start of file.
#        - `whence=1`: Offset relative to current pointer position.
#        - `whence=2`: Offset relative to end of file (e.g. `seek(-5, 2)` goes back 5 bytes from end).
#      Note: In text mode, seeking relative to current or end positions (`whence=1` or `2`) is
#      restricted to offset 0; otherwise, it raises an error due to multibyte character alignments.
#
# 5. BEST PRACTICES:
#    - Always close files using context managers (`with`) to guarantee file descriptor cleanup
#      even if exceptions occur.
#    - Explicitly specify the text encoding (e.g. `encoding="utf-8"`) since default platform
#      encodings can vary across OS environments (Windows might use CP-1252; macOS/Linux use UTF-8).
#
# 6. INTERVIEW QUESTIONS:
#    - Q: What does the `x` mode do in `open()`?
#      A: It opens a file for exclusive creation. If the file already exists, it raises a
#         `FileExistsError`, protecting existing data from accidental overwrites.
#    - Q: Can you seek relative to the end of a file in text mode?
#      A: No, in text mode seeking with `whence=2` (or `whence=1`) is invalid unless the offset
#         is exactly 0. This is because multibyte encoding schemes (like UTF-8) map single
#         characters to variable byte widths, making byte-relative index predictions unreliable.
#
# 7. EXERCISES & SOLUTIONS:
#    - Coding challenge: Write a binary file with custom floats, use `seek` to navigate directly
#      to a specific byte offset, read it, and print the resulting values.
#
###############################################################################

import os  # Standard library to clean up temporary files

# Let's define a temporary file path for operations
temp_file_name = "io_temp_sandbox.txt"

# 1. Writing and Reading Text Mode (with Universal Newlines)
print("--- Text Mode File I/O ---")
# Open in write-text mode
with open(temp_file_name, "w", encoding="utf-8") as f:
    f.write("Line 1: Python programming\n")
    f.write("Line 2: High performance IO\n")

# Open in read-text mode
with open(temp_file_name, "r", encoding="utf-8") as f:
    content = f.read()
    print("Read content:")
    print(content)

# 2. File Pointer Navigation (seek & tell)
print("\n--- File Pointer Navigation ---")
with open(temp_file_name, "r", encoding="utf-8") as f:
    # Initially, pointer is at the start (offset 0)
    print(f"Initial tell() pointer: {f.tell()}")  # Expected: 0
    
    # Read first 6 characters
    head = f.read(6)
    print(f"Read(6) output: '{head}'")
    print(f"Pointer position after read(6): {f.tell()}")  # Expected: 6
    
    # Seek back to start of file
    f.seek(0)
    print(f"Pointer position after seek(0): {f.tell()}")  # Expected: 0
    print(f"Read(6) output again: '{f.read(6)}'")

# 3. Binary Mode & Relative Seek
# We will create a binary file and write bytes to it.
temp_binary_name = "io_temp_binary.bin"

print("\n--- Binary Mode and Relative Seek ---")
with open(temp_binary_name, "wb") as f:
    # Write 10 bytes: 0 to 9
    f.write(bytes([0, 10, 20, 30, 40, 50, 60, 70, 80, 90]))

with open(temp_binary_name, "rb") as f:
    # Seek to end of file, then move back 3 bytes
    # whence=2 means seek relative to the end of the file.
    f.seek(-3, 2)
    print(f"Binary pointer after seek(-3, 2): {f.tell()}")  # Expected: 7 (10 - 3)
    
    # Read the remaining bytes
    remaining_bytes = f.read()
    print(f"Read remaining bytes: {list(remaining_bytes)}")  # Expected: [70, 80, 90]
    
    # Seek relative to current position
    # whence=1 means seek relative to current position.
    f.seek(-2, 1)  # Move back 2 bytes from end (pointer was at 10, now at 8)
    print(f"Binary pointer after seek(-2, 1): {f.tell()}")  # Expected: 8
    print(f"Read from offset 8: {list(f.read())}")  # Expected: [80, 90]

# Clean up files from workspace
if os.path.exists(temp_file_name):
    os.remove(temp_file_name)
if os.path.exists(temp_binary_name):
    os.remove(temp_binary_name)
print("\nTemporary test files cleaned up.")
