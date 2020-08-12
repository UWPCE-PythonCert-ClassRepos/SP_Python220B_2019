#!/usr/bin/env python
""" Electric appliances class"""
from inventory_management.inventory_class import Inventory


class ElectricAppliances(Inventory):
    """ Electric appliances class"""
    def __init__(self: Inventory,
                 product_code: str,
                 description: str,
                 market_price: float,
                 rental_price: float,
                 brand: str,
                 voltage: str):
        """
        Creates common instance variables from the parent class
        :rtype: ElectricAppliances
        """

        super().__init__(product_code, description, market_price, rental_price)

        self.brand = brand
        self.voltage = voltage
