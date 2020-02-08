""" Electric appliances class """

from inventoryclass import Inventory


class ElectricAppliances(Inventory):
    """ Electric appliances class  """
    def __init__(self, brand, voltage, *args):
        # Creates common instance variables from the parent class
        Inventory.__init__(self, *args)
        self.brand = brand
        self.voltage = voltage

    def return_as_dictionary(self):
        """ Function that return dictionary object for applicances. """
        outputdict = {}
        outputdict = Inventory.return_as_dictionary(self)
        outputdict['brand'] = self.brand
        outputdict['voltage'] = self.voltage

        return outputdict
