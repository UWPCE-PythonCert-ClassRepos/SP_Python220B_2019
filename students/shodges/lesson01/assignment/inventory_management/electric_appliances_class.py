"""
This module contains the electric_appliances class (which is a sub-class of inventory, found in
inventory_class.py)
"""

# pylint: disable=too-few-public-methods

# Electric appliances class
from inventory_class import Inventory

class ElectricAppliances(Inventory):
    """
    Inventory sub-class to create more fine-grained attributes specific to furniture.
    """

    def __init__(self, **kwargs):
        Inventory.__init__(self, **kwargs)
            # Creates common instance variables from the parent class

        self.brand = kwargs['brand']
        self.voltage = kwargs['voltage']

    def return_as_dictionary(self):
        """
        Return the current attributes of the instantiated class as a dictionary for processsing
        elsewhere.
        """
        output_dict = Inventory.return_as_dictionary(self)
        output_dict['brand'] = self.brand
        output_dict['voltage'] = self.voltage

        return output_dict
