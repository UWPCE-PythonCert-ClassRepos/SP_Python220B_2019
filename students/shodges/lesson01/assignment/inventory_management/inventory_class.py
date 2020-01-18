"""
This module provides common high-level class structures for individual pieces of inventory.
"""

# Inventory class
class inventory:
    """
    Super-class for inventory management.
    """

    def __init__(self, productCode, description, marketPrice, rentalPrice):
        self.product_code = productCode
        self.description = description
        self.market_price = marketPrice
        self.rental_price = rentalPrice

    def return_as_dictionary(self):
        """
        Return inventory attributes as a dictionary.
        """
        output_dict = {}
        output_dict['productCode'] = self.product_code
        output_dict['description'] = self.description
        output_dict['marketPrice'] = self.market_price
        output_dict['rentalPrice'] = self.rental_price

        return output_dict
