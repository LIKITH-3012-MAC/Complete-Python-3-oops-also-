# %% [markdown]
# # Topic: Async/Await - Native coroutines (PEP 492), event loop scheduling, and cooperative multitasking
# 
# ## 1. NATIVE COROUTINES: async def & await
# - Introduced in PEP 492 (Python 3.5).
# - **Native Coroutines**: Defined using the `async def` keyword sequence. Calling a native coroutine function does NOT run its body; it returns a **native coroutine object**.
# - **await expression**: Can only be used inside `async def` functions. Suspends execution of the current native coroutine until the target **awaitable** resolves, returning control to the Event Loop.
# 
# ## 2. AWAITABLE OBJECTS
# - An object is **awaitable** if it implements the `__await__` magic method returning an iterator.
# - Primary awaitables:
#   1. **Native Coroutine Objects**: Created by calling an `async def` function.
#   2. **asyncio.Task**: Wraps a coroutine, scheduling it to run on the event loop concurrently.
#   3. **asyncio.Future**: Low-level object representing an eventual result of an asynchronous operation.
# 
# ## 3. THE EVENT LOOP MECHANICS
# - **Cooperative Multitasking**: Native coroutines yield control back to the scheduler voluntarily using `await`. There is no pre-emptive thread context switching.
# - **Event Loop**:
#   - A single-threaded infinite loop that multiplexes I/O events (using selectors like epoll/kqueue).
#   - It maintains queues of ready tasks and executes them.
#   - When a task awaits a blocking I/O operation (like fetching web data), the event loop registers a callback for that I/O completion, suspends the task, and executes other ready tasks in the queue.
# 
# ## 4. INTERVIEW QUESTIONS
# - **Q: What is the main difference between multithreading and async/await in Python?**
#   - *A*: Multithreading uses pre-emptive context switching managed by the OS kernel, which is limited by the GIL for CPU tasks. Async/await is single-threaded cooperative multitasking managed by the application event loop, offering massive scalability for I/O-bound tasks.
# - **Q: Can you call an async function directly from a synchronous scope?**
#   - *A*: No, calling it returns a coroutine object without running the code. It must be run on an active event loop using `asyncio.run()` or inside another awaited coroutine.
# 
# ---

# %%
import asyncio
import time

# 1. Defining a native coroutine
async def fetch_data(task_id, delay):
    print(f" -> Task {task_id}: Started fetching data...")
    # Suspend execution for 'delay' seconds, yielding control back to event loop
    await asyncio.sleep(delay)
    print(f" -> Task {task_id}: Completed fetching data!")
    return f"Data from Task {task_id}"

# 2. Coordinating multiple coroutines concurrently
async def main():
    print("--- Event Loop execution started ---")
    start_time = time.time()
    
    # Schedule two fetch coroutines to execute concurrently
    task1 = asyncio.create_task(fetch_data("A", 1.5))
    task2 = asyncio.create_task(fetch_data("B", 1.0))
    
    # Await results (task2 will finish first because delay is shorter)
    data1 = await task1
    data2 = await task2
    
    end_time = time.time()
    print("\n--- Summary ---")
    print(f"Result A: {data1} | Result B: {data2}")
    print(f"Total execution time: {end_time - start_time:.2f} seconds")
    # Expected total time: ~1.5 seconds (executed concurrently!)

# Run the event loop
asyncio.run(main())

# %%
# 3. Calling async function synchronously returns coroutine object
print("\n--- Synchronous Call Inspection ---")
coro_obj = fetch_data("Test", 1)
print(f"Type: {type(coro_obj).__name__}")
# Note: "Started fetching data..." was NOT printed.
# We must close the coroutine object to prevent warnings
coro_obj.close()
