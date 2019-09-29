""" electric_appliances module

Class:
    ElectricAppliance
"""
from inventory_management.inventory import Inventory


# pylint: disable=too-few-public-methods
class ElectricAppliance(Inventory):
    """ ElectricAppliance class

    Methods:
        return_as_dictionary

    Attributes:
        brand
        voltage
    """

    def __init__(self, **kwargs):
        Inventory.__init__(self, **kwargs)  # Initializes common instance attributes from the
                                            # parent class

        self.brand = kwargs["brand"]
        self.voltage = kwargs["voltage"]

    def return_as_dictionary(self):
        """ Return class attribute values in a dict. """
        output_dict = super().return_as_dictionary()
        output_dict['brand'] = self.brand
        output_dict['voltage'] = self.voltage

        return output_dict
