"""Furniture class"""
# pylint:disable=R0913,R0903,W0613
from inventory_class import Inventory


class Furniture(Inventory):
    """
    Furniture class
    """
    def __init__(self, product_code, description, market_price, rental_price, material, size):
        Inventory.__init__(self, product_code, description, market_price, rental_price)
        # Creates common instance variables from the parent class
        self.material = material
        self.size = size

    def return_as_dictionary(self):
        """
        :return: Furniture class as a dictionary
        """
        output_dict = {'product_code': self.product_code, 'description': self.description,
                       'market_price': self.market_price, 'rental_price': self.rental_price,
                       'material': self.material, 'size': self.size}

        return output_dict
