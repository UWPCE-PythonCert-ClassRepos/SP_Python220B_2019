# Furniture class
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-arguments
"""
Everything to do with dealing with furniture
"""
from inventory_class import Inventory


class Furniture(Inventory):
    """
    The furniture class to end all furniture classes
    """

    def __init__(self, product_code, description, market_price,
                 rental_price, material, size):
        # Creates common instance variables from the parent class
        Inventory.__init__(self, product_code, description, market_price,
                           rental_price)
        self.material = material
        self.size = size

    def return_as_dictionary(self):
        """
        Returns furniture data as a dictionary
        """
        furniture_dict = {'product_code': self.product_code,
                          'description': self.description,
                          'market_price': self.market_price,
                          'rental_price': self.rental_price,
                          'material': self.material,
                          'size': self.size}

        return furniture_dict
