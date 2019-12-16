""" Inventory class
"""
class Inventory:
    """inventory"""

    def __init__(self, product_code, description, market_price,
                 rental_price):
        self.product_code = product_code
        self.description = description
        self.market_price = market_price
        self.rental_price = rental_price

    def return_as_dictionary(self):
        """returnasdictionary"""
        outputdict = {}
        outputdict['product_code'] = self.product_code
        outputdict['description'] = self.description
        outputdict['market_price'] = self.market_price
        outputdict['rental_price'] = self.rental_price

        return outputdict
