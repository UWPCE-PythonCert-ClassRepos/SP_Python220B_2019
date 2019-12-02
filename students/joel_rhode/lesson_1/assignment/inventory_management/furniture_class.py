"""This module provides a class for tracking furniture in inventory."""
from inventory_class import Inventory

class Furniture(Inventory):
    """Creats a furniture class for furniture in inventory."""
    def __init__(self, material, size, *args, **kwargs):
        # Creates common instance variables from the parent class
        super().__init__(*args, **kwargs)

        self.material = material
        self.size = size

    def return_as_dictionary(self):
        """Returns a dictionary of attributes for furniture in inventory."""
        output_dict = super().return_as_dictionary()
        output_dict['material'] = self.material
        output_dict['size'] = self.size

        return output_dict
