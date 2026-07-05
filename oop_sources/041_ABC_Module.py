###############################################################################
# TOPIC: ABC Module - ABCMeta vs ABC class, combining decorators, and compiler validations
#
# 1. DEFINITION & INTRODUCTION:
#    - The standard library module `abc` (Abstract Base Classes) provides the infrastructure
#      to define interface contracts in Python.
#
# 2. ABCMETA METACLASS VS ABC HELPER:
#    - Historically, to define an abstract class, you had to assign the metaclass directly:
#      `class MyAbstract(metaclass=abc.ABCMeta):`
#    - Python 3.4 introduced the `abc.ABC` helper class.
#      It is defined internally simply as:
#      `class ABC(metaclass=ABCMeta): pass`
#    - Inheriting from `abc.ABC` is the modern, cleaner approach that avoids direct metaclass
#      boilerplate syntax.
#
# 3. COMBINING DECORATORS WITH ABSTRACTMETHOD:
#    - You can define abstract class methods, static methods, and properties:
#        - Abstract Property:
#          ```python
#          @property
#          @abc.abstractmethod
#          def value(self): pass
#          ```
#        - Abstract ClassMethod:
#          ```python
#          @classmethod
#          @abc.abstractmethod
#          def factory(cls): pass
#          ```
#    - Declaration Order Rule: `@abc.abstractmethod` must always be placed as the **innermost**
#      decorator (closest to the function definition line).
#
# 4. INSTANTIATION VERIFICATION TIMING:
#    - Python does NOT block the compilation of subclasses with missing abstract overrides.
#      The validation happens at **instantiation time**.
#    - When you call `SubClass()`, CPython checks if the type descriptor has any outstanding
#      abstract methods. If so, it raises a `TypeError` and prevents memory allocation.
#
# 5. INTERVIEW QUESTIONS:
#    - Q: What is the relationship between `abc.ABC` and `abc.ABCMeta`?
#      A: `abc.ABC` is a helper class that uses `abc.ABCMeta` as its metaclass. Inheriting from
#         `ABC` is a syntactically cleaner alternative to declaring `metaclass=ABCMeta`.
#    - Q: Where must `@abc.abstractmethod` be placed when combined with `@classmethod`?
#      A: It must be placed as the innermost decorator (closest to the method body, below classmethod).
#
# 6. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement an abstract class exposing an abstract read-write property
#      using `@property` and `@property.setter` combined with `@abstractmethod`.
#
###############################################################################

import abc  # Standard library module for Abstract Base Classes

# 1. Define Abstract Interface using modern abc.ABC
class AbstractWorker(abc.ABC):
    
    # Abstract read-write property
    @property
    @abc.abstractmethod
    def salary(self):
        """Getter for worker salary."""
        pass
        
    @salary.setter
    @abc.abstractmethod
    def salary(self, value):
        """Setter for worker salary."""
        pass

    # Abstract classmethod
    @classmethod
    @abc.abstractmethod
    def create_default(cls):
        """Factory method to construct default worker."""
        pass

# 2. Implement Concrete Subclass
class Engineer(AbstractWorker):
    def __init__(self, sal):
        self._salary = sal
        
    # Implementing Abstract Property Getter
    @property
    def salary(self):
        return self._salary
        
    # Implementing Abstract Property Setter
    @salary.setter
    def salary(self, value):
        if value < 0:
            raise ValueError("Salary cannot be negative.")
        self._salary = value
        
    # Implementing Abstract ClassMethod
    @classmethod
    def create_default(cls):
        # returns instantiated default Engineer
        return cls(5000)

print("--- Testing Concrete Implementation ---")
eng = Engineer.create_default()
print(f"Engineer initial salary: ${eng.salary}")

eng.salary = 7500
print(f"Engineer updated salary: ${eng.salary}")

# 3. Compile-time check verification
# We can define a broken subclass containing missing overrides.
class BrokenWorker(AbstractWorker):
    # This class compiles fine! No errors are raised during import/loading.
    pass

print("\n--- Instantiation Verification Check ---")
try:
    # Validation triggers at instantiation time, raising TypeError
    worker = BrokenWorker()
except TypeError as e:
    print(f"Caught expected TypeError at instantiation: {e}")
    # Expected: Can't instantiate abstract class BrokenWorker with abstract methods...
