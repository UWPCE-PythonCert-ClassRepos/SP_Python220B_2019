"""Inventory class"""


class Inventory:  # pylint: disable=too-few-public-methods
    """Inventory Class"""

    def __init__(self, product_code, description, market_price, rental_price):
        # pylint: disable=too-many-arguments
        self.product_code = product_code
        self.description = description
        self.market_price = market_price
        self.rental_price = rental_price

    def return_as_dictionary(self):
        """Returns self as dictionary"""
        output_dict = dict()
        output_dict['productCode'] = self.product_code
        output_dict['description'] = self.description
        output_dict['marketPrice'] = self.market_price
        output_dict['rentalPrice'] = self.rental_price

        return output_dict
