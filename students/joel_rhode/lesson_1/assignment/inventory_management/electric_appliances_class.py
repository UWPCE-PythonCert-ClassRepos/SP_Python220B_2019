"""Provides classes for electric appliances."""
from inventory_class import Inventory


class ElectricAppliances(Inventory):
    """Class for standard electric appliance."""

    def __init__(self, product_code, description, market_price, rental_price,
                 brand, voltage):
        # Creates common instance variables from the parent class
        Inventory.__init__(self, product_code, description, market_price,
                           rental_price)

        self.brand = brand
        self.voltage = voltage

    def return_as_dictionary(self):
        """Return dictionary of appliance attributes."""
        output_dict = {}
        output_dict['productCode'] = self.product_code
        output_dict['description'] = self.description
        output_dict['marketPrice'] = self.market_price
        output_dict['rentalPrice'] = self.rental_price
        output_dict['brand'] = self.brand
        output_dict['voltage'] = self.voltage

        return output_dict
