"""
This module contains the furniture class (which is a sub-class of inventory, found in
inventory_class.py)
"""

# Furniture class
from inventory_class import inventory

class furniture(inventory):
    """
    Inventory sub-class to create more fine-grained attributes specific to furniture.
    """

    def __init__(self, productCode, description, marketPrice, rentalPrice, material, size):
        inventory.__init__(self, productCode, description, marketPrice, rentalPrice) # Creates
            #common instance variables from the parent class

        self.material = material
        self.size = size

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
        outputDict['material'] = self.material
        outputDict['size'] = self.size

        return outputDict
