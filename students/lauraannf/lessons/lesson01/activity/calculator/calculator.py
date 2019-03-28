""" calculator """


from .exceptions import InsufficientOperands


class Calculator(object):
    """ calculator """

    def __init__(self, adder, subtracter, multiplier, divider):
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """ adds a new number """
        self.stack.insert(0, number)

    def _do_calc(self, operator):
        """ does the operation """
        try:
            result = operator.calc(self.stack[1], self.stack[0])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """ adds """
        return self._do_calc(self.adder)

    def subtract(self):
        """ subtracts """
        return self._do_calc(self.subtracter)

    def multiply(self):
        """ multiplies """
        return self._do_calc(self.multiplier)

    def divide(self):
        """ divides """
        return self._do_calc(self.divider)
