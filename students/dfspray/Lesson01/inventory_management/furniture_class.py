"""Furniture class"""

from inventory_management.inventory_class import Inventory

class Furniture(Inventory):
    """Creates a class that handles data on furniture"""

    def __init__(self, inventory_info, material, size):
        """Initializes the class info"""
        # Creates common instance variables from the parent class
        Inventory.__init__(self, inventory_info)

        self.material = material
        self.size = size

    def return_as_dictionary(self):
        """Returns a dictionary of the furniture information"""
        output_dict = Inventory.return_as_dictionary(self)
        output_dict['material'] = self.material
        output_dict['size'] = self.size

        return output_dict
