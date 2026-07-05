###############################################################################
# TOPIC: Loops (for, while) and the Iterator Protocol & Loop Else
#
# 1. DEFINITION & INTRODUCTION:
#    - Loops execute blocks of code repeatedly. Python supports two loop constructs:
#        - `while`: Repeatedly executes as long as a boolean condition evaluates to True.
#        - `for`: Iterates over elements of an iterable (sequences, generators, collections).
#
# 2. THE ITERATOR PROTOCOL (How for loops work under the hood):
#    - Python `for` loops do not use simple index increment loop counters at the C level.
#      Instead, they rely entirely on the Iterator Protocol.
#    - When you execute `for item in iterable:`:
#        1. The interpreter calls the built-in function `iter(iterable)`. This delegates
#           internally to `iterable.__iter__()`, which must return an iterator object.
#        2. The interpreter repeatedly calls the built-in function `next(iterator)`. This delegates
#           to `iterator.__next__()` to retrieve the next element.
#        3. Once the iterator runs out of elements, `__next__()` raises a `StopIteration` exception.
#        4. The interpreter intercepts the `StopIteration` exception and terminates the loop
#           cleanly without exposing the exception to user space.
#
# 3. THE LOOP ELSE CLAUSE (Surprising Python Behavior):
#    - Both `for` and `while` loops support a trailing `else` clause.
#    - Execution Rule: The code inside the `else` block executes **ONLY if the loop terminates
#      naturally** (runs to completion).
#    - If the loop is terminated prematurely using a `break` statement, the `else` block is
#      skipped.
#    - Think of it as: "execute this block if NO matching item was found to trigger a break".
#
# 4. TIME & SPACE COMPLEXITY:
#    - Iterating over an array: O(N) time complexity.
#    - Memory: O(1) space complexity if iterating using an iterator/generator, as only the current
#      state/pointer is maintained in memory.
#
# 5. BEST PRACTICES:
#    - Prefer `for` loops over `while` loops when iterating collections or sequences; it is
#      safer and avoids accidental infinite loop conditions.
#    - Use the loop `else` clause for search loops to replace flag variables (e.g. `found = False`).
#
# 6. INTERVIEW QUESTIONS:
#    - Q: When does the `else` block of a loop execute?
#      A: It executes when the loop finishes all iterations naturally (reaches the end of the
#         sequence or the while condition becomes false) without hitting a `break` statement.
#    - Q: How does a `for` loop know when to stop?
#      A: It catches the `StopIteration` exception raised by the iterator's `__next__()` method.
#
# 7. EXERCISES & SOLUTIONS:
#    - Coding challenge: Write a custom iterable class from scratch implementing `__iter__` and
#      `__next__` to simulate a countdown timer, and iterate over it using a `for` loop.
#
###############################################################################

# 1. Iterator Protocol Emulation (Doing what a 'for' loop does under the hood)
target_list = [10, 20, 30]

print("--- Simulating 'for' loop using Iterator Protocol ---")
# Step A: Get iterator object
list_iterator = iter(target_list)  # equivalent to target_list.__iter__()
print(f"Iterator Object: {list_iterator}")

# Step B: Repeatedly call next() inside a try-except block to intercept StopIteration
while True:
    try:
        item = next(list_iterator)  # equivalent to list_iterator.__next__()
        print(f"Retrieved element: {item}")
    except StopIteration:
        # Loop terminates when StopIteration is raised
        print("StopIteration caught! Iteration complete.")
        break

# 2. Loop 'else' Clause Demonstration
# Search for prime numbers in a list to demonstrate loop-else utility
def search_even_numbers(numbers):
    print(f"\nSearching even numbers in: {numbers}")
    for num in numbers:
        if num % 2 == 0:
            print(f"  Found even number: {num}! Breaking loop.")
            break
    else:
        # This executes ONLY if the loop completed without hit 'break'.
        print("  Loop completed naturally. No even numbers found.")

# Case A: Contains even number (should break, loop-else skipped)
search_even_numbers([1, 3, 5, 6, 7])

# Case B: Does not contain even number (loop completes, loop-else executed)
search_even_numbers([1, 3, 5, 7, 9])

# 3. Custom Countdown Iterator Implementation
class Countdown:
    def __init__(self, start):
        self.count = start
        
    def __iter__(self):
        # An iterator must return itself from __iter__
        return self
        
    def __next__(self):
        if self.count <= 0:
            # Signal iteration completion
            raise StopIteration
        val = self.count
        self.count -= 1
        return val

print("\n--- Custom Iterator Loop ---")
counter_obj = Countdown(3)
for step in counter_obj:
    print(f"Count: {step}")
