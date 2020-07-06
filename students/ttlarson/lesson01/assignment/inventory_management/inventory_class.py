""" Inventory module """
# pylint: disable=too-many-arguments, too-few-public-methods


class Inventory:
    """ Class Inventory """
    def __init__(self, product_code, description, market_price, rental_price):
        """ constructor """
        self.product_code = product_code
        self.description = description
        self.market_price = market_price
        self.rental_price = rental_price

    def return_as_dictionary(self):
        """ return Inventory class attributes """
        output_dict = {}
        output_dict['product_code'] = self.product_code
        output_dict['description'] = self.description
        output_dict['market_price'] = self.market_price
        output_dict['rental_price'] = self.rental_price

        return output_dict
