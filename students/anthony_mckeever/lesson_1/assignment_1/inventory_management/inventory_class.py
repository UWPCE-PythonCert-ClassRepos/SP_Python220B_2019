# Inventory class

"""
Inventory Module

Classes:
    Inventory
"""


class Inventory():
    """ A class representing an inventory item. """

    def __init__(self, product_code, description, market_price, rental_price):
        """
        Initializes the inventory class

        :self:          The Class
        :product_code:  The Product Code of the inventory item
        :description:   The Description of the inventory item
        :market_price:  The Market Price of the inventory item
        :rental_price:  The Rental Price of the inventory item
        """
        self.product_code = product_code
        self.description = description
        self.market_price = market_price
        self.rental_price = rental_price

    def return_as_dictionary(self):
        """
        Return a dictionary representing the Inventory object
        """
        output_dict = {}
        output_dict['product_code'] = self.product_code
        output_dict['description'] = self.description
        output_dict['market_price'] = self.market_price
        output_dict['rental_price'] = self.rental_price

        return output_dict
