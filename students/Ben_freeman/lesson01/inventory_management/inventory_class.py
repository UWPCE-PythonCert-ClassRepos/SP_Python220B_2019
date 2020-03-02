# Inventory class
"""method docstring"""


class Inventory:
    """class docstring"""
    def __init__(self, productcode, description, marketprice, rentalprice):
        self.productcode = productcode
        self.description = description
        self.marketprice = marketprice
        self.rentalprice = rentalprice

    def returnasdictionary(self):
        """method docstring"""
        outputdict = {}
        outputdict['productcode'] = self.productcode
        outputdict['description'] = self.description
        outputdict['marketprice'] = self.marketprice
        outputdict['rentalprice'] = self.rentalprice

        return outputdict
