"""Module docstring"""
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-arguments

# Furniture class
from inventory_class import Inventory


class Furniture(Inventory):
    """Creates common instance variables from the parent class"""
    def __init__(self, product_code, description, market_price, rental_price, material, size):
        Inventory.__init__(self, product_code, description, market_price, rental_price)
        self.material = material
        self.size = size

    def return_as_dictionary(self):
        """method docstring"""
        output_dict = {}
        output_dict = Inventory.return_as_dictionary(self)
        output_dict['material'] = self.material
        output_dict['size'] = self.size

        return output_dict
