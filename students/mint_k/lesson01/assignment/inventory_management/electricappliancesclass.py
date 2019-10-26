""" Electric appliances class
this is docstring for the Electric appliance class
"""

from .inventory_class import Inventory

class ElectricAppliances(Inventory):
    """ Electric appliances class
this is docstring for the Electric appliance class
"""

    def __init__(self, product_code, description, market_price,
                 rental_price, brand, voltage):
        Inventory.__init__(self, product_code, description,
                           market_price, rental_price)
        # Creates common instance variables from the parent class


        self.brand = brand
        self.voltage = voltage

    def return_as_dictionary(self):
        """docstring"""
        outputdict = Inventory.return_as_dictionary(self)
        outputdict['brand'] = self.brand
        outputdict['voltage'] = self.voltage

        return outputdict
