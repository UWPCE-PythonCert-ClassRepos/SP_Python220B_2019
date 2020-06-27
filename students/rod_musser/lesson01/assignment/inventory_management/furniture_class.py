""" Furniture class """
from inventory_class import Inventory


class Furniture(Inventory):
    """Represents a furniture product in the inventory"""
    def __init__(self, product_code, description, market_price, rental_price, material, size):
        """Creates common instance variables from the parent class"""
        Inventory.__init__(self, product_code, description, market_price, rental_price)

        self.material = material
        self.size = size

    def return_as_dictionary(self):
        """Return Furniture attributes as a dict"""
        output_dict = super().return_as_dictionary()
        output_dict['material'] = self.material
        output_dict['size'] = self.size

        return output_dict
