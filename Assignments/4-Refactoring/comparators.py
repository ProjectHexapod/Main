from math_utils import arraysAreEqual
from mox import Comparator

class ReturnTrue(Comparator):
    """Always returns True
    """
    def __init__(self, reference):
        self.reference = reference
        
    def equals(self, testValue):
        return True

    def __eq__(self, testValue):
        return self.equals(testValue)

    def __ne__(self, testValue):
        return not self.equals(testValue)

class ArraysEqual(Comparator):
    """Compares numpy arrays for equality.
    """
    def __init__(self, reference):
        self.reference = reference

    def equals(self, testValue):
        return arraysAreEqual(self.reference, testValue)

    def __eq__(self, testValue):
        return self.equals(testValue)

    def __ne__(self, testValue):
        return not self.equals(testValue)
        
    def __repr__(self):
        return str(self.reference)

class Gt (Comparator):
    """Greater Than.  Returns true iff the supplied value is greater than the argument.
    """
    
    def __init__(self, reference):
        self.reference = reference;

    def equals(self,testValue):
        return testValue > self.reference

    def __eq__(self, testValue):
        return self.equals(testValue)

    def __ne__(self, testValue):
        return not self.equals(testValue)

class Lt (Comparator):
    """Less Than.  Returns true iff the supplied value is less than the argument.
    """
    
    def __init__(self, reference):
        self.reference = reference;

    def equals(self,testValue):
        return testValue < self.reference

    def __eq__(self, testValue):
        return self.equals(testValue)

    def __ne__(self, testValue):
        return not self.equals(testValue)


