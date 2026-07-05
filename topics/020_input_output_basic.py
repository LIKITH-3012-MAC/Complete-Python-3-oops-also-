###############################################################################
# TOPIC: Input and Output Streams (print, input, and sys.stdout)
#
# 1. DEFINITION & INTRODUCTION:
#    - Python programs interact with the outer environment using standard input,
#      output, and error streams.
#    - `print()`: Built-in function to write text output to standard output (`sys.stdout`).
#    - `input()`: Built-in function to read a line of text from standard input (`sys.stdin`),
#      returning it as a string with the trailing newline character removed.
#
# 2. ADVANCED `print()` PARAMETERS:
#    The `print(*objects, sep=' ', end='\n', file=None, flush=False)` signature features:
#    - `sep`: String inserted between values, default is a space `' '`.
#    - `end`: String appended after the last value, default is a newline `'\n'`.
#    - `file`: A file-like object (stream); defaults to the current system standard output
#      (`sys.stdout`). You can pass any object implementing a `.write(string)` method.
#    - `flush`: Boolean. If `True`, the output stream is forcibly flushed immediately.
#      If `False`, output buffering may delay text appearing in the console/file.
#
# 3. BUFFERING & FLUSHING:
#    - Writing to streams is an expensive OS call. To optimize performance, output is typically
#      buffered (stored in memory and written in bulk).
#    - In interactive mode or when outputting to a terminal, stdout is line-buffered (flushes
#      on `\n`).
#    - When redirected to a pipe or file, stdout is block-buffered (flushes only when the buffer
#      fills up). Setting `flush=True` bypasses buffering.
#
# 4. RAW I/O STREAMS:
#    - `sys.stdin` and `sys.stdout` are text file-like streams.
#    - `sys.stdout.write(string)` writes text directly without appending spaces or newlines.
#      It returns the number of characters written.
#
# 5. BEST PRACTICES:
#    - Avoid calling `print()` repeatedly in tight performance-sensitive loops.
#      Instead, collect outputs and write them in chunks or use `sys.stdout.write()`.
#    - For logging progress bars or real-time status updates in CLI tools, use `flush=True`
#      with `end='\r'` (carriage return) to overwrite the current line.
#
# 6. INTERVIEW QUESTIONS:
#    - Q: How can you write to the standard error stream (`sys.stderr`) using `print`?
#      A: Pass `sys.stderr` to the `file` argument: `print("error", file=sys.stderr)`.
#    - Q: What does `sys.stdout.flush()` do?
#      A: It forces the internal memory buffer to write all pending output characters to
#         the operating system stream immediately.
#
# 7. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a basic progress-bar output loop that updates in-place on the
#      terminal using carriage returns, custom delays, and stream flushing.
#
###############################################################################

import sys  # standard library module to interact with system I/O streams
import time  # Module to introduce delay for progress bar simulation
import io  # Module to create custom in-memory string streams

# 1. Advanced print() Parameters
print("--- print() Customizations ---")
# Using sep and end arguments
print("Python", "Rust", "C++", sep=" | ", end=" [End of Line]\n")
# Expected Output: Python | Rust | C++ [End of Line]

# 2. Redirecting print() to an In-Memory String Stream
# We create a StringIO object, which mimics a file interface in memory.
string_stream = io.StringIO()
print("Secret data to redirect", file=string_stream)

# Retrieve the written content from our custom stream
redirected_content = string_stream.getvalue()
print(f"Captured content from stream: {repr(redirected_content)}")

# 3. Raw stdout Write vs print()
# sys.stdout.write does not add default spacing or newlines.
print("\n--- Raw Stream Write ---")
chars_written = sys.stdout.write("Direct stdout write without newline. ")
print(f"\nCharacters written: {chars_written}")

# 4. In-Place Terminal Updates (Carriage Return)
# Carriage return (\r) moves the cursor back to the start of the line.
print("\n--- Simulating Progress Bar ---")
for progress in range(1, 6):
    percent = progress * 20
    # Overwrite the line by starting with \r, and flush the stream immediately
    sys.stdout.write(f"\rDownloading Data: [{'#' * progress}{'.' * (5 - progress)}] {percent}%")
    sys.stdout.flush()  # Force flushing the buffer to render immediately
    time.sleep(0.1)  # Brief sleep to make the update visible
print("\nDownload Complete!")

# 5. Redirecting Standard Input (Simulating input() execution)
# To test input() without blocking the agent runtime, we temporarily redirect sys.stdin
# to an in-memory stream containing simulated user inputs.
original_stdin = sys.stdin
simulated_input_data = io.StringIO("Simulated User Response Line\n")
sys.stdin = simulated_input_data

try:
    print("\n--- Reading Simulated Input ---")
    user_response = input("Enter values: ")
    print(f"Received via input(): {repr(user_response)}")
finally:
    # Always restore original stdin stream
    sys.stdin = original_stdin
