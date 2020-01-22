"""
This module contains the electric_appliances class (which is a sub-class of inventory, found in
inventory_class.py)
"""

# Electric appliances class
from inventory_class import Inventory

class ElectricAppliances(Inventory):
    """
    Inventory sub-class to create more fine-grained attributes specific to furniture.
    """

    def __init__(self, productCode, description, rental_price, brand, voltage):
        Inventory.__init__(self, productCode, description, rental_price) # Creates common instance
            #variables from the parent class

        self.brand = brand
        self.voltage = voltage

    def return_as_dictionary(self):
        """
        Return the current attributes of the instantiated class as a dictionary for processsing
        elsewhere.
        """
        output_dict = Inventory.return_as_dictionary(self)
        output_dict['brand'] = self.brand
        output_dict['voltage'] = self.voltage

        return output_dict
