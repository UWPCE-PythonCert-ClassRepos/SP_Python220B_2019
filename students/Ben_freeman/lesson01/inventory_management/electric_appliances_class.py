# Electric appliances class
"""doc string"""
from inventory_management.inventory_class import Inventory


class ElectricAppliances(Inventory):
    """class docstring"""
    def __init__(self, productcode, description, marketprice, rentalprice, brand, voltage):
        Inventory.__init__(self, productcode, description, marketprice, rentalprice)
        # Creates common instance variables from the parent class
        self.brand = brand
        self.voltage = voltage

    def returnasdictionary(self):
        """docstring method"""
        outputdict = {}
        outputdict['productcode'] = self.productcode
        outputdict['description'] = self.description
        outputdict['marketprice'] = self.marketprice
        outputdict['rentalprice'] = self.rentalprice
        outputdict['brand'] = self.brand
        outputdict['voltage'] = self.voltage

        return outputdict
