###############################################################################
# TOPIC: Property Deleter - @name.deleter, attribute cleanup, and resource release
#
# 1. DEFINITION & INTRODUCTION:
#    - Property Deleter: A decorator syntax `@property_name.deleter` that enables defining
#      cleanup actions executed when an attribute is deleted using the `del` keyword:
#      `del instance.property_name`
#    - Motivation: Resource Cleanup. Allows cleaning up associated cache tables, releasing
#      file handles, deleting database records, or resetting dependencies when an attribute
#      reference is explicitly cleared.
#
# 2. SYNTAX & IMPLEMENTATION RULES:
#    - The deleter method MUST share the exact same name as the base `@property` getter.
#    - It receives only the `self` parameter.
#    - Under the hood, calling `@property_name.deleter` configures the descriptor's `__delete__`
#      magic method to point to the decorated deleter function.
#
# 3. INTERVIEW QUESTIONS:
#    - Q: When is a property deleter method triggered?
#      A: It is triggered when the `del` statement is executed on the property attribute of an
#         instance (e.g. `del user.profile_picture`).
#    - Q: How does a property deleter protect class backing fields?
#      A: By intercepting the raw delete call, preventing external code from deleting the underlying
#         backing variable directly, or allowing you to reset it to `None` instead of removing it.
#
# 4. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a `FileSession` class containing a cached list of data. Expose
#      the cache as a property, and write a deleter that clears and closes the cache resource.
#
###############################################################################

class FileCache:
    def __init__(self, filename):
        self.filename = filename
        self._cache = {}  # Backing cache dict
        
    @property
    def cache(self):
        print(" -> [Property Getter] Accessing file cache...")
        return self._cache
        
    # Deleter decorator
    @cache.deleter
    def cache(self):
        # Intercepts 'del obj.cache'
        print(f" -> [Property Deleter] Clearing cache file resources for: {self.filename}")
        self._cache.clear()  # Clear cache keys
        # We can also reset the field or remove it entirely
        # Let's delete the backing variable from the instance dict
        del self._cache

print("--- Initializing FileCache ---")
fc = FileCache("user_session.log")
fc.cache["session_id"] = "ABC_999"
print(f"Cache state: {fc.cache}")

print("\n--- Triggering Property Deleter ---")
# Executing del triggers the deleter method
del fc.cache

# Verify backing field was deleted
try:
    print(fc.cache)
except AttributeError as e:
    print(f"\nCaught expected AttributeError: {e}")
    # Expected: 'FileCache' object has no attribute '_cache' (since we deleted it inside the deleter)
