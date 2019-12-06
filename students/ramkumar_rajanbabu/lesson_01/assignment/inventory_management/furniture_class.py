"""Module for furniture"""

from inventory_class import Inventory


class Furniture(Inventory):
    """Class for furniture"""

    def __init__(self, product_code, description, market_price, rental_price, material, size):
        """Initializes furniture class"""
        Inventory.__init__(self,
                           product_code,
                           description,
                           market_price,
                           rental_price)  # Creates common instance variables from the parent class

        self.material = material
        self.size = size

    def return_as_dictionary(self):
        """Returns a dictionary with attributes"""
        output_dict = {}
        output_dict['product_code'] = self.product_code
        output_dict['description'] = self.description
        output_dict['market_price'] = self.market_price
        output_dict['rental_price'] = self.rental_price
        output_dict['material'] = self.material
        output_dict['size'] = self.size
        return output_dict
