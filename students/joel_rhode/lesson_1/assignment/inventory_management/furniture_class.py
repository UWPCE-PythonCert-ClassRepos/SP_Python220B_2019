"""This module provides a class for tracking furniture in inventory."""
from inventory_class import inventory


class Furniture(inventory):
    """Creats a furniture class for furniture in inventory."""
    def __init__(self, product_code, description, market_price, rental_price,
                 material, size):
        # Creates common instance variables from the parent class
        inventory.__init__(self, product_code, description, market_price,
                           rental_price)

        self.material = material
        self.size = size

    def return_as_dictionary(self):
        """Returns a dictionary of attributes for furniture in inventory."""
        output_dict = {}
        output_dict['product_code'] = self.product_code
        output_dict['description'] = self.description
        output_dict['market_price'] = self.market_price
        output_dict['rental_price'] = self.rental_price
        output_dict['material'] = self.material
        output_dict['size'] = self.size

        return output_dict
