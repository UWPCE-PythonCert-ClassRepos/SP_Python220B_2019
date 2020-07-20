#!/usr/bin/env python
""" Inventory class """


class Inventory:
    """ Inventory class """

    def __init__(self: object,
                 product_code: str,
                 description: str,
                 market_price: float,
                 rental_price: float):
        """
        Base class for all subclasses
        :rtype: Inventory
        """

        self.product_code = product_code
        self.description = description
        self.market_price = market_price
        self.rental_price = rental_price

    def return_as_dictionary(self):
        """ Return all keys as a dictionary.  self.__dict__ -> {...}"""
        # return self.__dict__
        return {k: v for k, v in self.__dict__.items() if '__' not in k}
