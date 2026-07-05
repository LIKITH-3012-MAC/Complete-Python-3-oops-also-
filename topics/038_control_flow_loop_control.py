###############################################################################
# TOPIC: Loop Control Statements (break, continue, pass) and nested Loop Exits
#
# 1. DEFINITION & INTRODUCTION:
#    - Python provides control statements to interrupt or alter loop execution flow:
#        - `break`: Instantly terminates the loop, jumping to the first line after the loop.
#        - `continue`: Skips the remaining statements in the current iteration block,
#          jumping back to the loop header to evaluate the next item or condition.
#        - `pass`: A null operation. It does nothing and acts as a syntax placeholder
#          where statement blocks are grammatically required but no action is needed.
#
# 2. COMPILER & CPYTHON MECHANICS:
#    - When CPython compiles `break` and `continue`, it emits jumps in bytecode.
#    - `break` compiles to jump offsets directing control out of the loop block.
#    - `continue` compiles to jump offsets returning to the loop condition evaluation segment.
#    - `pass` is completely ignored by the byte compiler (it generates no execution bytecode).
#
# 3. EXITING NESTED LOOPS (The Outer Exit Problem):
#    - Python does not support labeled breaks (e.g. `break label_name` like in Java or JavaScript).
#      A `break` statement only exits the innermost loop containing it.
#    - Strategies to break out of nested loops:
#        1. Boolean Flag Variables: Check a flag (e.g. `exit_flag`) in both loop headers.
#        2. Function Encapsulation: Put the nested loop in a function and use `return` to exit
#           both loops instantly. This is the cleanest approach.
#        3. Raising Exceptions: Define a custom exception (e.g., `NestedLoopExit`) and catch it
#           outside the nested block.
#        4. Loop Else Clause: Check condition states using loop-else cooperatively.
#
# 4. BEST PRACTICES:
#    - Use `continue` to filter out negative or irrelevant conditions early in loop blocks
#      (guard clause style) to avoid deep nesting of statements inside the loop.
#    - Prefer helper functions over complex boolean flag checks for nested loops.
#
# 5. INTERVIEW QUESTIONS:
#    - Q: Does the `pass` statement consume CPU cycles?
#      A: No. The compiler optimizes `pass` out, producing no runtime bytecode instructions.
#         It is strictly a structural syntactic placeholder.
#    - Q: How can you break out of a nested loop in Python without helper functions?
#      A: You can use a boolean flag updated in the inner loop and checked in the outer loop,
#         or raise a custom exception that is caught immediately outside the outer loop.
#
# 6. EXERCISES & SOLUTIONS:
#    - Coding challenge: Search for a specific target number inside a 2D grid matrix and
#      exit all loops immediately when found, demonstrating multiple exit strategies.
#
###############################################################################

# 1. break, continue, and pass Demonstration
print("--- Loop Control Statements ---")
for i in range(1, 6):
    if i == 2:
        # pass does nothing, code execution continues normally
        pass
        print("  [pass executed for i=2]")
        
    if i == 3:
        # continue skips the remaining lines for i=3 and moves to i=4
        print("  [continue executed for i=3: skipping print]")
        continue
        
    if i == 5:
        # break terminates the loop
        print("  [break executed for i=5: terminating loop]")
        break
        
    print(f"Loop index: {i}")

# 2. Exiting Nested Loops: Method 1 (Boolean Flag)
grid = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
target = 5
found_flag = False

print("\n--- Nested Loop Exit: Boolean Flag ---")
for row_idx, row in enumerate(grid):
    for col_idx, val in enumerate(row):
        if val == target:
            print(f"Found target {target} at ({row_idx}, {col_idx})")
            found_flag = True
            break  # Exits inner loop
    if found_flag:
        break  # Exits outer loop
print("Exited loops using boolean flag.")

# 3. Exiting Nested Loops: Method 2 (Function Encapsulation - Recommended)
# Returning from a helper function terminates execution instantly, cleaner than flags.
def find_in_grid(grid_matrix, search_val):
    for row_idx, row in enumerate(grid_matrix):
        for col_idx, val in enumerate(row):
            if val == search_val:
                return row_idx, col_idx  # Exits all loops and returns coordinate
    return None

print("\n--- Nested Loop Exit: Function Return ---")
coords = find_in_grid(grid, 5)
print(f"Found target coords via function: {coords}")

# 4. Exiting Nested Loops: Method 3 (Custom Exception)
class LoopExitException(Exception):
    pass

print("\n--- Nested Loop Exit: Exception ---")
try:
    for row_idx, row in enumerate(grid):
        for col_idx, val in enumerate(row):
            if val == target:
                print(f"Found target {target} at ({row_idx}, {col_idx})")
                raise LoopExitException  # Raise exception to jump out of both loops
except LoopExitException:
    print("Exited loops using raise LoopExitException.")
