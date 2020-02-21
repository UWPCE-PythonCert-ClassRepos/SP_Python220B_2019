#!/usr/bin/env python
"""
This is the inventory class module.
"""
# Inventory class

class Inventory:
    """Define a base class from which appliances and furniture will subclass."""

    def __init__(self, product_code, description, market_price, rental_price):
        self.product_code = product_code
        self.description = description
        self.market_price = market_price
        self.rental_price = rental_price

    def return_as_data_struct(self):
        """Create a data structure from the product attributes."""
        output_data = {}
        output_data['productCode'] = self.product_code
        output_data['description'] = self.description
        output_data['marketPrice'] = self.market_price
        output_data['rentalPrice'] = self.rental_price

        return output_data
