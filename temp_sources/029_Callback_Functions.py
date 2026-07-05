# %% [markdown]
# # Topic: Callback Functions - Event-driven callbacks, asynchronous notifications, and success/error handlers
# 
# ## 1. DEFINITION: CALLBACKS
# - **Callback Function**: A function reference passed as an argument to another function, which is designed to be invoked (called back) inside the receiving function when a specific event occurs.
# - **Patterns**:
#   - **Synchronous Callbacks**: Called immediately during the host function's execution (e.g., custom sorting key functions).
#   - **Asynchronous Callbacks**: Called later when a background operation (like network download, file read, or timer) finishes.
# 
# ## 2. SUCCESS/ERROR HANDLERS
# - A common pattern in networking and backend systems is passing distinct success and error callback functions to handle outcomes asynchronously.
# 
# ## 3. INTERVIEW QUESTIONS
# - **Q: What is a callback function in Python?**
#   - *A*: A function reference passed to another function that is executed automatically when a task completes or an event is fired.
# - **Q: What is the main difference between synchronous and asynchronous callbacks?**
#   - *A*: Synchronous callbacks block execution and run immediately before the host function returns. Asynchronous callbacks are registered and executed later, when a background event resolves.
# 
# ---

# %%
# 1. Asynchronous Task execution simulation with Callbacks
import time

def process_file_async(filename, on_success, on_error):
    """Simulates loading a file, invoking on_success or on_error callbacks."""
    print(f" -> Starting background process for {filename}...")
    # Simulate dynamic checks
    if not filename.endswith(".json"):
        # Trigger error callback
        on_error(ValueError("Unsupported file format! Must be a .json file."))
    else:
        # Simulate success processing
        dummy_data = {"status": "success", "lines": 42}
        # Trigger success callback
        on_success(dummy_data)

# Define callbacks
def handle_success(data):
    print(f" -> [CALLBACK] Success! Loaded data: {data}")

def handle_error(error):
    print(f" -> [CALLBACK] Error! Failed to load: {error}")

print("--- Testing Success Callback ---")
process_file_async("data.json", handle_success, handle_error)

print("\n--- Testing Error Callback ---")
process_file_async("image.png", handle_success, handle_error)

# %%
# 2. Event Dispatcher (Event-driven callback pattern)
class EventDispatcher:
    def __init__(self):
        self.listeners = {}

    def register(self, event_name, callback):
        """Registers a callback to listen to a specific event name."""
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(callback)

    def dispatch(self, event_name, event_data):
        """Dispatches an event, invoking all registered callbacks."""
        if event_name in self.listeners:
            for callback in self.listeners[event_name]:
                callback(event_data)

# Instantiate dispatcher
dispatcher = EventDispatcher()

# Register callbacks
dispatcher.register("on_user_login", lambda username: print(f" -> [EVENT] Update DB: {username} logged in"))
dispatcher.register("on_user_login", lambda username: print(f" -> [EVENT] Send email alert to {username}"))

print("\n--- Dispatching User Login Event ---")
dispatcher.dispatch("on_user_login", "alice_99")
# Expected: Both registered lambda callbacks are executed sequentially!
