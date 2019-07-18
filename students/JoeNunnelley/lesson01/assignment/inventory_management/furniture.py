"""
Furniture Module
"""

from inventory import InventoryItem

class Furniture(InventoryItem):
    """ The Furniture Class """
    def __init__(self, product_code, description, market_price,
                 rental_price, material, size):
        # Creates common instance variables from the parent class
        InventoryItem.__init__(self, product_code, description,
                               market_price, rental_price)

        self.material = material
        self.size = size

    def return_as_dictionary(self):
        """ Function to return the Furniture item as a dictionary """
        return InventoryItem.return_as_dictionary
