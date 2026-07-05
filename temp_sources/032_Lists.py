# %% [markdown]
# # Topic: Lists - Dynamic arrays, CPython list_resize over-allocation, and amortized execution complexity
# 
# ## 1. DEFINITION: DYNAMIC ARRAYS
# - **Python list**: Under the hood, Python lists are implemented as **Dynamic Arrays** of references (pointers) to Python objects.
# - **Dynamic resizing**: Unlike static arrays, they can grow and shrink dynamically.
# 
# ## 2. CPYTHON RESIZING MECHANICS: list_resize
# - When a list is appended to and the underlying array capacity is exceeded, CPython resizes the array:
#   1. It allocates a new, larger block of contiguous memory.
#   2. It copies the object references from the old block to the new block.
#   3. It deletes the old pointer array block.
# - **Over-Allocation Strategy**:
#   - To avoid resizing on every single append, CPython overallocates space.
#   - The growth formula in CPython source code (`listobject.c`):
#     $$\text{allocated\_slots} = \text{newsize} + (\text{newsize} \gg 3) + (\text{newsize} < 9 \;?\; 3 \;:\; 6)$$
#   - This produces growth patterns like: 0, 4, 8, 16, 25, 35, 46, 58, 72, 88...
# 
# ## 3. AMORTIZED TIME COMPLEXITY
# - **$O(1)$ Amortized Append**:
#   - Most append calls execute in $O(1)$ time because there are empty pre-allocated slots.
#   - Occasionally, a call triggers a resize ($O(N)$ copy cost).
#   - Averaged over $N$ insertions, the total time is $O(N)$, meaning the average (amortized) cost per append is **$O(1)$**.
# 
# ## 4. INTERVIEW QUESTIONS
# - **Q: What is the average time complexity of appending an element to a Python list?**
#   - *A*: It is $O(1)$ amortized. Most appends occur in empty overallocated slots. Only occasionally does a resize copy trigger, distributing the cost.
# - **Q: Why does a Python list use more memory than a raw array of the same size?**
#   - *A*: First, it overallocates slots to support dynamic growth. Second, it is an array of pointers (references) to boxed Python objects, introducing pointer memory costs.
# 
# ---

# %%
import sys

# 1. Tracking CPython list overallocation behavior
print("--- Tracking CPython List Memory Resizing ---")
lst = []

# Print initial size and capacity
print(f"Empty list memory size: {sys.getsizeof(lst)} bytes")

previous_size = sys.getsizeof(lst)
for i in range(30):
    lst.append(i)
    current_size = sys.getsizeof(lst)
    # Check if a resize event occurred (change in bytes allocated)
    if current_size != previous_size:
        print(f"Length: {len(lst):>2} | Memory Size: {current_size:>3} bytes | Resize Triggered!")
        previous_size = current_size

# %%
# 2. Visualizing overallocation slots
# In 64-bit systems, each reference pointer takes 8 bytes.
# We can calculate the allocated capacity slot counts.
# base size of empty list is 56 bytes.
def get_allocated_slots(l):
    return (sys.getsizeof(l) - 56) // 8

print("\n--- Visualizing allocated slots capacity vs size ---")
test_list = []
for i in range(12):
    test_list.append(i)
    slots = get_allocated_slots(test_list)
    excess = slots - len(test_list)
    print(f"Elements: {len(test_list):>2} | Allocated Slots: {slots:>2} | Spare slots: {excess:>2}")
    # You will observe capacity increments: 4 -> 8 -> 16 -> 25 ...
