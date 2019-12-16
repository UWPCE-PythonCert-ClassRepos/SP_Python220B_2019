"""Provides classes for electric appliances."""
from inventory_class import Inventory


class ElectricAppliances(Inventory):
    """Class for standard electric appliance."""

    def __init__(self, brand, voltage, *args, **kwargs):
        # Creates common instance variables from the parent class
        super().__init__(*args, **kwargs)

        self.brand = brand
        self.voltage = voltage

    def return_as_dictionary(self):
        """Return dictionary of appliance attributes."""
        output_dict = super().return_as_dictionary()
        output_dict['brand'] = self.brand
        output_dict['voltage'] = self.voltage

        return output_dict
