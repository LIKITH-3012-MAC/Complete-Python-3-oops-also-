###############################################################################
# TOPIC: Coroutines, async/await, Event Loop, and Cooperative Multitasking
#
# 1. DEFINITION & INTRODUCTION:
#    - Native Coroutines: Declared using the `async def` syntax. They are designed for
#      cooperative multitasking and non-blocking asynchronous operations.
#    - `await`: Suspends execution of the enclosing coroutine until the awaited task/future
#      completes, releasing control back to the event loop.
#
# 2. CONCURRENCY VS PARALLELISM:
#    - Concurrency (Cooperative Multitasking): Multiple tasks make progress in overlapping
#      timeframes, but only one runs at any given microsecond on a single CPU core.
#    - Parallelism: Multiple tasks run at the exact same physical time on multiple CPU cores.
#    - Asyncio achieves concurrency, NOT parallelism. It is ideal for I/O-bound tasks
#      (network requests, database queries), not CPU-bound tasks (heavy arithmetic).
#
# 3. THE EVENT LOOP MECHANISM:
#    - The Event Loop is the heart of an asynchronous program.
#    - It is a single-threaded loop that monitors pending I/O operations and tasks.
#    - When a coroutine yields control (via `await non_blocking_io()`), the event loop
#      registers the operation and switches to run other ready tasks.
#    - This avoids thread context-switching overhead, allowing Python to handle thousands
#      of concurrent network connections on a single thread.
#
# 4. TASKS AND GATHERING:
#    - `asyncio.create_task(coro)`: Wraps a coroutine into a `Task` object and registers it
#      with the event loop to execute concurrently.
#    - `asyncio.gather(*tasks)`: Runs multiple asynchronous operations concurrently and blocks
#      until all complete, returning a list of results in the order they were supplied.
#
# 5. THE BLOCKING CALL PITFALL:
#    - Never execute synchronous blocking calls (like `time.sleep(5)` or blocking database reads)
#      inside a coroutine.
#    - Doing so blocks the single thread running the event loop, freezing all other concurrent
#      tasks. Always use asynchronous equivalents (like `asyncio.sleep()`) or run blocking tasks
#      in a thread pool executor.
#
# 6. INTERVIEW QUESTIONS:
#    - Q: What happens if you run `time.sleep(5)` inside an `async def` function?
#      A: It freezes the entire event loop thread for 5 seconds, preventing any other concurrent
#         coroutines from executing, defeating the purpose of asynchronous concurrency.
#    - Q: Does `asyncio` speed up CPU-bound operations (like image processing)?
#      A: No. Asyncio is single-threaded, so CPU-bound tasks will lock the thread and block progress.
#         Use `multiprocessing` for parallel CPU workloads.
#
# 7. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement two mock network fetch tasks running concurrently using
#      `asyncio.gather`, measuring total elapsed time to prove concurrency.
#
###############################################################################

import asyncio  # Standard module for asynchronous concurrency
import time  # Module to measure overall execution times

# 1. Define Asynchronous Tasks
async def mock_fetch_api(service_name, delay):
    print(f" -> [Fetch {service_name}] Starting API call...")
    # asyncio.sleep yields control back to the event loop, allowing other tasks to run
    await asyncio.sleep(delay)
    print(f" -> [Fetch {service_name}] Completed after {delay}s!")
    return f"{service_name}_data_payload"

# 2. Main Coordinator Coroutine
async def main_async_flow():
    print("--- Starting Concurrent Asynchronous Execution ---")
    start_time = time.perf_counter()
    
    # We schedule two tasks to run concurrently.
    # task_1 takes 2 seconds; task_2 takes 1 second.
    # Running them concurrently should take max(2, 1) = 2 seconds (plus tiny loop overhead),
    # rather than 2 + 1 = 3 seconds in a serial execution!
    task_1 = mock_fetch_api("UserDB", 2)
    task_2 = mock_fetch_api("PaymentGateway", 1)
    
    print("Gathering tasks concurrently...")
    # asyncio.gather schedules both and waits for their results
    results = await asyncio.gather(task_1, task_2)
    
    end_time = time.perf_counter()
    duration = end_time - start_time
    
    print("\n--- Execution Finished ---")
    print(f"Results list: {results}")
    print(f"Total time elapsed: {duration:.4f} seconds")  # Should be close to 2.0s

# 3. Run the Event Loop
# asyncio.run() creates the event loop, executes the passed coroutine, and shuts down the loop.
# Note: We run it using the standard interface.
asyncio.run(main_async_flow())

# 4. Demonstrating Task Scheduling (Fire and Forget concurrency)
async def task_scheduling_demo():
    print("\n--- Task Scheduling Demo ---")
    
    async def helper_task(num):
        await asyncio.sleep(0.5)
        print(f"Helper task {num} complete.")
        
    start = time.perf_counter()
    # create_task schedules execution in the background immediately
    t1 = asyncio.create_task(helper_task(1))
    t2 = asyncio.create_task(helper_task(2))
    
    print("Background tasks created, doing other work...")
    await asyncio.sleep(0.1)  # Doing other work
    print("Waiting for background tasks to complete...")
    
    # Await them to ensure they finish before function returns
    await t1
    await t2
    print(f"Total scheduling demo time: {time.perf_counter() - start:.4f}s")

# Execute task demonstration
asyncio.run(task_scheduling_demo())
