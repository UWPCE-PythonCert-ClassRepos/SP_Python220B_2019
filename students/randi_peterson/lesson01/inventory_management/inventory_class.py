"""Inventory class"""

class Inventory:
    """Class of object called Inventory"""

    def __init__(self, product_code, description, market_price, rental_price):
        """Creats the Inventory object"""
        self.product_code = product_code
        self.description = description
        self.market_price = market_price
        self.rental_price = rental_price

    def return_as_dictionary(self):
        """Creates a dict"""
        output_dict = dict()
        output_dict['product_code'] = self.product_code
        output_dict['description'] = self.description
        output_dict['market_price'] = self.market_price
        output_dict['rental_price'] = self.rental_price

        return output_dict
