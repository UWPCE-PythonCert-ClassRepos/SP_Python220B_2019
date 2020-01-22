"""
This module provides common high-level class structures for individual pieces of inventory.
"""
import market_prices

class Inventory:
    """
    Super-class for inventory management.
    """

    def __init__(self, productCode, description):
        self.product_code = productCode
        self.description = description
        self.market_price = market_prices.get_latest_price(productCode)
        self.rental_price = (self.market_price * 1.2) / 36 # market price +20% spread over 3 years

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
