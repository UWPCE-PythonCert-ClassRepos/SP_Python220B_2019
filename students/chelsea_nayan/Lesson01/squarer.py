# squarer.py

# A simple class with a single method (calc)
class Squarer(object):

    @staticmethod
    def calc(operand):
        # return operand*operand # OLD
        # return operand**operand # WRONG
        # return operand*operand # OlD
        return operand**2
