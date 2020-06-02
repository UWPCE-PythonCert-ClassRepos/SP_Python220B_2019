"""Inventory class"""
# pylint:disable=R0913,R0903,W0613


class Inventory:
    """
    Inventory class
    """

    def __init__(self, product_code, description, market_price, rental_price):
        self.product_code = product_code
        self.description = description
        self.market_price = market_price
        self.rental_price = rental_price

    def return_as_dictionary(self):
        """
        :return: Inventory class as a dictionary
        """
        output_dict = {'product_code': self.product_code, 'description': self.description,
                       'market_price': self.market_price, 'rental_price': self.rental_price}

        return output_dict
