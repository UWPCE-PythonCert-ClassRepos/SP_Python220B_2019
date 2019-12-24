"""Module for furniture"""

# pylint: disable=too-few-public-methods
# pylint: disable=too-many-arguments

from inventory_class import Inventory


class Furniture(Inventory):
    """Class for furniture"""

    def __init__(self, product_code, description,
                 market_price, rental_price, material, size):
        """Initializes furniture class"""
        Inventory.__init__(self, product_code, description,
                           market_price, rental_price)
        # Creates common instance variables from the parent class
        self.material = material
        self.size = size

    def return_as_dictionary(self):
        """Returns a dictionary with attributes"""
        output_dict = Inventory.return_as_dictionary(self)
        output_dict['material'] = self.material
        output_dict['size'] = self.size
        return output_dict
