""" divider module

Classes:
    Divider
"""

class Divider():
    """ Class for dividing two numbers. """

    @staticmethod
    def calc(operand_1, operand_2):
        """ Divide two numbers. """
        # Handle the case where operand_2 == 0 (divide by 0).
        # OLD return operand_1/operand_2
        try:
            result = operand_1 / operand_2
        except ZeroDivisionError:
            raise ZeroDivisionError
        else:
            return result
