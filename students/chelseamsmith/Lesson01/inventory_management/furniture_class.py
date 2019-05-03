"""Furniture class"""
from inventory_management.inventory_class import Inventory
# pylint: disable=too-many-arguments,too-few-public-methods


class Furniture(Inventory):
    """furniture class. holds product information.
    also has method to return product info in a dictionary"""
    def __init__(self, product_code, description, market_price, rental_price,
                 material, size):
        Inventory.__init__(self, product_code, description, market_price,
                           rental_price)

        self.material = material
        self.size = size

    def return_as_dictionary(self):
        """returns a dictionary containing product information"""
        output_dict = Inventory.return_as_dictionary(self)
        output_dict['material'] = self.material
        output_dict['size'] = self.size

        return output_dict
