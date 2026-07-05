###############################################################################
# TOPIC: Method Overriding - Redefinition, super() lookups, and Liskov substitution (LSP)
#
# 1. DEFINITION & INTRODUCTION:
#    - Method Overriding: An OOP feature where a child subclass redefines a method
#      inherited from a parent class to provide a specialized implementation.
#    - Polymorphic Resolution: When the method is invoked on a subclass instance, Python's
#      runtime lookup executes the child's overridden version.
#
# 2. RUNTIME LOOKUP & super() OVERRIDES:
#    - In CPython, when `instance.method()` is evaluated, Python resolves the attribute via MRO.
#      The child class redefines the method name key in its local `__dict__`, shadowing the parent.
#    - To invoke the parent's overridden method from the child class, use `super().method()`.
#      This locates the next class after the current class in the MRO list, executing its method.
#
# 3. LISKOV SUBSTITUTION PRINCIPLE (LSP) CONTEXT:
#    - LSP (one of the SOLID design principles) states that objects of a superclass should be
#      replaceable with objects of its subclasses without breaking the application.
#    - Overriding Rules to conform to LSP:
#        - Keep parameter compatibility: The overridden child method signature should accept the
#          same arguments as the parent. If you add arguments, they must be optional (have default values).
#        - Return Type covariance: The child method should return the same type or a subclass of the type
#          returned by the parent.
#        - Exception safety: The child method should not raise exceptions that are not part of the parent
#          method's contract.
#
# 4. BEST PRACTICES:
#    - When overriding methods, preserve signature compatibility.
#    - Add annotations to check parameters.
#
# 5. INTERVIEW QUESTIONS:
#    - Q: What is method overriding?
#      A: Redefining an inherited parent method inside a child subclass to implement child-specific behavior.
#    - Q: How can you access the parent method from within the overridden child method?
#      A: By calling `super().method_name(*args, **kwargs)`.
#
# 6. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a base `Report` class and a `JSONReport` subclass, overriding
#      the format method and verifying LSP compliance.
#
###############################################################################

# 1. Parent Class conforming to LSP
class Report:
    def __init__(self, title, content):
        self.title = title
        self.content = content
        
    def generate(self) -> str:
        # Base method returns standard text representation
        return f"=== {self.title} ===\n{self.content}"

# 2. Subclass overriding methods (LSP-compliant)
class HTMLReport(Report):
    # Overriding __init__ (calling super)
    def __init__(self, title, content, style_class="default"):
        super().__init__(title, content)
        self.style = style_class
        
    # Overriding generate method
    # Signature remains compatible: returns str
    def generate(self) -> str:
        # We can call the parent's method internally using super()
        base_text = super().generate()
        print(f" -> [HTMLReport] Customizing output using style: {self.style}")
        return f"<div class='{self.style}'>\n  <p>{base_text}</p>\n</div>"

print("--- Standard Report ---")
rep = Report("System Status", "All services operational.")
print(rep.generate())

print("\n--- Overridden HTML Report ---")
html_rep = HTMLReport("Database Alert", "Disk usage exceeding 90%.", "warning-box")
print(html_rep.generate())

# 3. Liskov Substitution Verification
# Client code that takes any Report and prints its length
def print_report_length(report_instance: Report):
    # This function expects report_instance to support .generate() returning a string.
    # Because HTMLReport is LSP-compliant, passing it does not break this code!
    rendered = report_instance.generate()
    print(f"Report character length: {len(rendered)}")

print("\n--- Testing Liskov Substitution ---")
print_report_length(rep)       # Works with Parent
print_report_length(html_rep)  # Works with Subclass (Substituted safely)
