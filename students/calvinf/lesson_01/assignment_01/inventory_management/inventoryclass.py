""" Inventory class """
class Inventory:
    """
        Class to create dictionary for storing inventory
    """

    def __init__(self, productcode, description, marketprice, rentalprice):
        """ Creates common instance variables from the parent class """
        self.productcode = productcode
        self.description = description
        self.marketprice = marketprice
        self.rentalprice = rentalprice

    def return_as_dictionary(self):
        """ Function that return dictionary object for Inventory.  """
        outputdict = {}
        outputdict['productCode'] = self.productcode
        outputdict['description'] = self.description
        outputdict['marketPrice'] = self.marketprice
        outputdict['rentalPrice'] = self.rentalprice

        return outputdict
