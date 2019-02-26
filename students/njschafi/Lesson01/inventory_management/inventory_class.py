"""Inventory Class: Creates an instance of an object with attributes
inputted by user. Object has following attributes: product_code, description,
market_price, rental_price"""
# pylint: disable=too-few-public-methods

class Inventory:
    """Creates inventory item instance."""

    def __init__(self, product_code, description, market_price, rental_price):
        """Creates instance of inventory object."""
        self.product_code = product_code
        self.description = description
        self.market_price = market_price
        self.rental_price = rental_price

    def return_as_dictionary(self):
        """Returns a dict of the inventory attributes of an instance."""
        output_dict = {}
        output_dict['product_code'] = self.product_code
        output_dict['description'] = self.description
        output_dict['market_price'] = self.market_price
        output_dict['rental_price'] = self.rental_price
        return output_dict
