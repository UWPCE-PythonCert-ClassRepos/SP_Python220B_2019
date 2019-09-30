""" inventory module

Class:
    Inventory
"""


# pylint: disable=too-few-public-methods
class Inventory:
    """ Base class for products. All attributes must be supplied to the constructor.

    Methods:
        return_as_dictionary

    Attributes:
        product_code
        description
        market_price
        rental_price
    """

    def __init__(self, **kwargs):
        self.product_code = kwargs["product_code"]
        self.description = kwargs["description"]
        self.market_price = kwargs["market_price"]
        self.rental_price = kwargs["rental_price"]

    def return_as_dictionary(self):
        """ Return class attributes in a dict."""
        output_dict = {}
        output_dict['product_code'] = self.product_code
        output_dict['description'] = self.description
        output_dict['market_price'] = self.market_price
        output_dict['rental_price'] = self.rental_price

        return output_dict
