# Furniture class
# pylint: disable=too-few-public-methods
"""
docstring
"""
from inventory_class import Inventory


class Furniture(Inventory):
    """
    docstring
    """

    def __init__(self, material, size, **kwargs):
        # Creates common instance variables from the parent class
        Inventory.__init__(self, **kwargs)
        self.material = material
        self.size = size

    def return_as_dictionary(self):
        """
        Does a thing
        :return:
        """
        furniture_dict = {'product_code': self.product_code,
                          'description': self.description,
                          'market_price': self.market_price,
                          'rental_price': self.rental_price,
                          'material': self.material,
                          'size': self.size}

        return furniture_dict
