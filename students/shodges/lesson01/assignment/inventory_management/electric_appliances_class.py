"""
This module contains the electric_appliances class (which is a sub-class of inventory, found in
inventory_class.py)
"""

# Electric appliances class
from inventory_class import inventory

class electric_appliances(inventory):
    """
    Inventory sub-class to create more fine-grained attributes specific to furniture.
    """

    def __init__(self, productCode, description, marketPrice, rentalPrice, brand, voltage):
        inventory.__init__(self, productCode, description, marketPrice, rentalPrice) # Creates
            #common instance variables from the parent class


        self.brand = brand
        self.voltage = voltage

    def returnAsDictionary(self):
        """
        Return the current attributes of the instantiated class as a dictionary for processsing
        elsewhere.
        """
        outputDict = {}
        outputDict['productCode'] = self.productCode
        outputDict['description'] = self.description
        outputDict['marketPrice'] = self.marketPrice
        outputDict['rentalPrice'] = self.rentalPrice
        outputDict['brand'] = self.brand
        outputDict['voltage'] = self.voltage

        return outputDict
