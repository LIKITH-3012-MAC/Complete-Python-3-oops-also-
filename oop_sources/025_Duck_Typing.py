###############################################################################
# TOPIC: Duck Typing - Dynamic interface matching and file-like objects
#
# 1. DEFINITION & INTRODUCTION:
#    - Duck Typing: A programming concept associated with dynamic typing where an object's
#      suitability is determined by the presence of certain methods and properties, rather
#      than its actual inheritance pedigree or class type.
#    - Maxim: "If it walks like a duck and quacks like a duck, then it is a duck."
#
# 2. CONTRAST WITH STATIC TYPING:
#    - In statically typed languages (like Java or C#), to pass an object to a function, the
#      object's class must explicitly inherit from a parent class or implement a named Interface
#      declared in the function signature:
#      `public void fly(IFlyable flyer) { flyer.fly(); }`
#    - In Python, you just call the method on the object. If the object implements that method,
#      it works, regardless of inheritance:
#      `def fly(flyer): flyer.fly()`
#
# 3. REAL-WORLD EXAMPLE (File-like Objects):
#    - Python's standard library leverages duck typing extensively.
#    - Any custom object that implements `.read()`, `.write()`, and `.close()` methods is a
#      "file-like object" and can be passed to functions that read/write files (like compression
#      utilities or serializers), without inheriting from standard I/O classes.
#      Example: `io.StringIO` mimics a file in-memory using string payloads.
#
# 4. BEST PRACTICES:
#    - Design interfaces around behavior rather than inheritance hierarchy.
#    - To write clear code while keeping duck typing flexibility, use structural typing
#      via `typing.Protocol` (covered in the Protocols topic).
#
# 5. INTERVIEW QUESTIONS:
#    - Q: What is Duck Typing?
#      A: A style of typing where type suitability is evaluated based on what methods/properties
#         the object implements, rather than its class inheritance.
#    - Q: Give an example of duck typing in the standard library.
#      A: In-memory string streams `io.StringIO` behave as file-like objects because they implement
#         `.read()` and `.write()`, allowing them to be processed by any file-reading utility.
#
# 6. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement two completely unrelated classes (Duck and Person) that both
#      implement a `quack` method, and invoke them inside a function expecting quacking behavior.
#
###############################################################################

import io  # Standard module demonstrating file-like duck-typed streams

# 1. Unrelated classes implementing identical methods
class Duck:
    def quack(self):
        print(" -> Duck says: Quack, Quack!")
        
    def fly(self):
        print(" -> Duck is flying high.")

class Imitator:
    def quack(self):
        # Unrelated class, implements same method name
        print(" -> Imitator says: Quack (mimicking a duck)!")

# Client function expecting quacking behavior
# Notice there is no type constraint; it accepts any object supporting .quack()
def make_it_quack(any_object):
    # Duck typing: we simply call the method and let Python resolve it
    any_object.quack()

print("--- Testing Duck Typing ---")
d = Duck()
i = Imitator()

make_it_quack(d)  # Expected: Duck quacks
make_it_quack(i)  # Expected: Imitator quacks (works despite no shared parent!)

# 2. File-like Object demonstration in standard library
# Any function that parses file data can parse StringIO data due to Duck Typing.
def print_first_line(file_like_object):
    # Expects .readline() method
    line = file_like_object.readline()
    print(f"File Header: {line.strip()}")

# Test with a real file stream (simulated in memory)
print("\n--- StringIO Duck Typing ---")
string_file = io.StringIO("Configuration_Header\nDatabase_Port=5432\n")
print_first_line(string_file)  # Expected: "File Header: Configuration_Header"
