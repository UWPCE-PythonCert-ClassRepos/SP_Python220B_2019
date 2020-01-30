"""
Furniture Class
"""
from inventory_management.inventory import Inventory


class Furniture(Inventory):
    """
    Furniture Class
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.material = kwargs["material"]
        self.size = kwargs["size"]

    def return_as_dictionary(self):
        output_dict = super().return_as_dictionary()
        output_dict["material"] = self.material
        output_dict["size"] = self.size

        return output_dict
