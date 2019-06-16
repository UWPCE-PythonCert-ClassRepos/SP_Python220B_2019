"""Furniture class"""
from inventory_class import Inventory


class Furniture(Inventory):
    """Creates the Furniture class"""
    def __init__(self, product_code, description, market_price, rental_price, material, size):
        """Creates a Furniture object"""
        # Creates common instance variables from the parent class
        Inventory.__init__(self, product_code, description, market_price, rental_price)

        self.material = material
        self.size = size

    def return_as_dictionary(self):
        """Returns as a dict"""
        output_dict = dict()
        output_dict['productCode'] = self.product_code
        output_dict['description'] = self.description
        output_dict['marketPrice'] = self.market_price
        output_dict['rentalPrice'] = self.rental_price
        output_dict['material'] = self.material
        output_dict['size'] = self.size

        return output_dict
