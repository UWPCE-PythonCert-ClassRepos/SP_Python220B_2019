"""
Module for furniture class
"""
from inventory_management.inventory_class import Inventory

class Furniture(Inventory): #pylint: disable=too-few-public-methods
    """
    Class for furniture
    """

    def __init__(self, product_code, description,
                 market_price, rental_price, **kwargs):
        """
        Initializes furniture class
        """
        super().__init__(product_code, description,
                         market_price, rental_price)
        # Creates common instance variables from the parent class
        if 'material' in kwargs:
            self.material = kwargs['material']

        if 'size' in kwargs:
            self.size = kwargs['size']

    def return_as_dictionary(self):
        """
        Returns attributes of furniture class
        """
        output_dict = super().return_as_dictionary()

        output_dict['material'] = self.material
        output_dict['size'] = self.size

        return output_dict
