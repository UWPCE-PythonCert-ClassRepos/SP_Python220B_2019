#!/usr/bin/env python
""" Furniture class"""
from inventory_management.inventory_class import Inventory


class Furniture(Inventory):
    """ Furniture class"""
    def __init__(self: Inventory,
                 product_code: str,
                 description: str,
                 market_price: float,
                 rental_price: float,
                 material="",
                 size=""):
        """
        Creates common instance variables from the parent class
        :rtype: Furniture
        """

        super().__init__(product_code, description, market_price, rental_price)

        self.material = material
        self.size = size
