"""
Furniture
"""

# .pylintrc disable = duplicate-code, too-many-arguments, too-few-public-methods

from inventory_management.inventory_class import Inventory

class Furniture(Inventory):
    """ Furniture """
    def __init__(self, product_code, description, market_price, rental_price, material, size):
        """ init """
        Inventory.__init__(self, product_code, description, market_price, rental_price)
        self.material = material
        self.size = size

    def return_as_dictionary(self):
        """ return invent as dict """
        output_dict = {}
        output_dict['product_code'] = self.product_code
        output_dict['description'] = self.description
        output_dict['market_price'] = self.market_price
        output_dict['rental_price'] = self.rental_price
        output_dict['material'] = self.material
        output_dict['size'] = self.size

        return output_dict
