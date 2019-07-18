"""
Electric appliances Module
"""

from inventory import InventoryItem

class ElectricAppliances(InventoryItem):
    """ The ElectricAppliances class """
    def __init__(self, product_code, description, market_price,
                 rental_price, brand, voltage):
        """ Creates common instance variables from the parent class """
        InventoryItem.__init__(self, product_code, description, market_price,
                               rental_price)

        self.brand = brand
        self.voltage = voltage

    def return_as_dictionary(self):
        """ Function to return appliance as a dictionary """
        return InventoryItem.return_as_dictionary
