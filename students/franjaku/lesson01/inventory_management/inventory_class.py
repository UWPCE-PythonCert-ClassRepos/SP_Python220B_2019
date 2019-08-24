# Inventory class
"""Contains the inventory class."""


class Inventory:
    """Defines the inventory class."""

    def __init__(self, product_code, description, market_price, rental_price):
        self.product_code = product_code
        self.description = description
        self.market_price = market_price
        self._rental_price = rental_price

    def return_as_dictionary(self):
        """Returns the object as a dictionary."""
        output_dict = {}
        output_dict['product_code'] = self.product_code
        output_dict['description'] = self.description
        output_dict['market_price'] = self.market_price
        output_dict['rental_price'] = self.rental_price

        return output_dict

    @ property
    def rental_price(self):
        """Return the rental price..."""
        return self._rental_price
