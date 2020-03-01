# Furniture class
"""module docstring"""
from inventory_management.inventory_class import Inventory


class Furniture(Inventory):
    """class docstring"""
    def __init__(self, productcode, description, marketprice, rentalprice, material, size):
        Inventory.__init__(self, productcode, description, marketprice, rentalprice)
        # Creates common instance variables from the parent class

        self.material = material
        self.size = size

    def returnasdictionary(self):
        """method docstring"""
        outputdict = Inventory.returnasdictionary(self)
        outputdict['material'] = self.material
        outputdict['size'] = self.size

        return outputdict
