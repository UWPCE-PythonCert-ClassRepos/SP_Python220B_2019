"""
This module contains the furniture class (which is a sub-class of inventory, found in
inventory_class.py)
"""

# pylint: disable=too-few-public-methods

# Furniture class
from inventory_class import Inventory

class Furniture(Inventory):
    """
    Inventory sub-class to create more fine-grained attributes specific to furniture.
    """

    def __init__(self, **kwargs):
        Inventory.__init__(self, **kwargs)
            # Creates common instance variables from the parent class

        self.material = kwargs['material']
        self.size = kwargs['size']

    def return_as_dictionary(self):
        """
        Return the current attributes of the instantiated class as a dictionary for processsing
        elsewhere.
        """
        output_dict = Inventory.return_as_dictionary(self)
        output_dict['material'] = self.material
        output_dict['size'] = self.size

        return output_dict
