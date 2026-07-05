###############################################################################
# TOPIC: Polymorphism - compile-time vs runtime, dynamic dispatch, and interfaces
#
# 1. DEFINITION & INTRODUCTION:
#    - Polymorphism: Derived from Greek, meaning "many forms". It refers to the ability of
#      different classes to respond to the exact same method signature or interface in their
#      own unique ways.
#
# 2. TYPES OF POLYMORPHISM:
#    - Compile-Time (Static) Polymorphism: Resolved during compilation.
#        - Python achieves compile-time polymorphism primarily through **Operator Overloading**
#          (defining dunder methods like `__add__` to change operator behavior based on types).
#    - Runtime (Dynamic) Polymorphism: Resolved during execution.
#        - Python achieves runtime polymorphism through **Method Overriding**.
#        - Dynamic Dispatch: When a method is called, Python looks up the method at runtime based
#          on the concrete class of the object receiving the call, resolving dynamically.
#
# 3. INTERFACE SUBSTITUTION:
#    - Dynamic typing makes polymorphism incredibly simple in Python. You do not need to explicitly
#      define a common interface class or inherit from a parent class for polymorphism to work;
#      as long as objects support the called method name, they can be substituted interchangeably
#      (a concept known as Duck Typing, covered next).
#
# 4. BEST PRACTICES:
#    - Leverage polymorphism to write generic functions that operate on parent interfaces (like abstract
#      base classes) rather than hardcoded concrete types, making the system modular and open for extension.
#
# 5. INTERVIEW QUESTIONS:
#    - Q: How does Python resolve which method to call at runtime?
#      A: CPython resolves attribute lookups dynamically using the object's type descriptor and
#         Method Resolution Order (MRO), picking the first match found in the class tree.
#    - Q: Can you achieve polymorphism in Python without using class inheritance?
#      A: Yes, because of Python's dynamic typing. Any two unrelated classes implementing a method
#         with the same name can be treated polymorphically by client code.
#
# 6. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement three distinct class types representing file readers
#      (CSVReader, JSONReader, TextReader), each implementing a `read_data` method, and execute
#      them polymorphically inside a single client runner loop.
#
###############################################################################

# 1. Base Class representing an Abstract Interface
class Document:
    def __init__(self, filename):
        self.filename = filename
        
    def show(self):
        raise NotImplementedError("Subclasses must implement show()!")

# 2. Concrete Polymorphic Subclasses
class PDFDocument(Document):
    def show(self):
        return f"Rendering PDF file layout: {self.filename}"

class WordDocument(Document):
    def show(self):
        return f"Rendering Word document text: {self.filename}"

class HTMLDocument(Document):
    def show(self):
        return f"Rendering HTML page elements: {self.filename}"

# 3. Polymorphic Client Code
# The display_document function accepts any object that supports the `.show()` interface contract
# and processes it dynamically at runtime.
def display_document(doc_object):
    # Dynamic Dispatch: Python resolves the target .show() method at runtime
    # based on the type of doc_object.
    render_output = doc_object.show()
    print(f"[Client Display] {render_output}")

print("--- Testing Polymorphic Dispatch ---")
docs = [
    PDFDocument("manual.pdf"),
    WordDocument("resume.docx"),
    HTMLDocument("index.html")
]

# Loop runs polymorphically
for doc in docs:
    display_document(doc)
    # Expected output shows different rendering descriptions for each class type
