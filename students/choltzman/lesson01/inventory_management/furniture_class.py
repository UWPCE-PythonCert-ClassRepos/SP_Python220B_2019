# pylint: disable=too-few-public-methods, too-many-arguments
"""Furniture class file."""
from .inventory_class import Inventory


class Furniture(Inventory):
    """Furniture class."""

    def __init__(self, product_code, description, market_price, rental_price,
                 material, size):
        # Creates common instance variables from the parent class
        Inventory.__init__(self, product_code, description, market_price,
                           rental_price)

        self.material = material
        self.size = size

    def return_as_dict(self):
        """Returns class data as dictionary."""
        output_dict = Inventory.return_as_dict(self)
        output_dict['material'] = self.material
        output_dict['size'] = self.size

        return output_dict
