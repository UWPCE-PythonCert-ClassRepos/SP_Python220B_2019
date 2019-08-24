# Inventory class
"""Contains the inventory class."""


class Inventory:
    """Defines the inventory class."""

    def __init__(self, product_code, description, market_price, rental_price):
        self.product_code = product_code
        self.description = description
        self.market_price = market_price
        self.rental_price = rental_price

    def return_as_dictionary(self):
        """Returns the object as a dictionary."""
        output_dict = {}
        output_dict['productCode'] = self.product_code
        output_dict['description'] = self.description
        output_dict['marketPrice'] = self.market_price
        output_dict['rentalPrice'] = self.rental_price

        return output_dict
