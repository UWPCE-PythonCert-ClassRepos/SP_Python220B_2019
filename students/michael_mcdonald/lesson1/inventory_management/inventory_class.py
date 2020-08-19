"""Inventory class"""


class Inventory:
    """ Inventory class """

    def __init__(self, product_code, description, market_price, rental_price):
        """init class"""
        self.product_code = product_code
        self.description = description
        self.market_price = market_price
        self.rental_price = rental_price

    def return_as_dictionary(self):
        """ build dictionary """
        output_dict = {'product_code': self.product_code, 'description': self.description,
                       'market_price': self.market_price, 'rental_price': self.rental_price}

        return output_dict
