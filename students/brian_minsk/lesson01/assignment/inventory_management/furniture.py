""" furniture module

Class:
    Furniture
"""
from inventory_management.inventory import Inventory


# pylint: disable=too-few-public-methods
class Furniture(Inventory):
    """ Furniture class. All attributes must be supplied to the contructor, including the
    attributes of Inventory, the base class.

    Methods:
        return_as_dictionary

    Attributes:
        material
        size
    """

    def __init__(self, **kwargs):
        Inventory.__init__(self, **kwargs)  # Initializes common instance attributes from the
                                            # parent class

        self.material = kwargs["material"]
        self.size = kwargs["size"]

    def return_as_dictionary(self):
        """ Return class attributes in a dict."""
        output_dict = super().return_as_dictionary()
        output_dict['material'] = self.material
        output_dict['size'] = self.size

        return output_dict
