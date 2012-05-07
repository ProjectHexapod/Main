#Adds two comparators for mox, Gt and Lt

from mox import Comparator

#Gt - Greater than - returns true if value is greater than the argument
class Gt (Comparator):
    
    def __init__(self, reference):
        self.reference = reference;

    def equals(self,testValue):
        return testValue > self.reference

    def __eq__(self, testValue):
        return self.equals(testValue)

    def __ne__(self, testValue):
        return not self.equals(testValue)

#Lt - Less than - returns true if value is less than the argument
class Lt (Comparator):
    
    def __init__(self, reference):
        self.reference = reference;

    def equals(self,testValue):
        return testValue < self.reference

    def __eq__(self, testValue):
        return self.equals(testValue)

    def __ne__(self, testValue):
        return not self.equals(testValue)


