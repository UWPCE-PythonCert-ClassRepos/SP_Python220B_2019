"""
Module for electric appliances class
"""
from inventory_management.inventory_class import Inventory

class ElectricAppliances(Inventory): #pylint: disable=too-few-public-methods
    """
    Class for electric appliances
    """

    def __init__(self, product_code, description,
                 market_price, rental_price, **kwargs):
        """
        Initializes electric appliances class
        """
        super().__init__(product_code, description,
                         market_price, rental_price)
                           # Creates common instance variables from the parent class
        if 'brand' in kwargs:
            self.brand = kwargs['brand']

        if 'voltage' in kwargs:
            self.voltage = kwargs['voltage']

    def return_as_dictionary(self):
        """
        Returns several attributes of dictionary class
        """
        output_dict = super().return_as_dictionary()

        output_dict['brand'] = self.brand
        output_dict['voltage'] = self.voltage

        return output_dict
