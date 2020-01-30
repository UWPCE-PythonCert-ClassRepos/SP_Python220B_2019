"""
Electrical Appliances Class
"""
from inventory_management.inventory import Inventory


class ElectricAppliances(Inventory):
    """
    Electrical Appliances
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.brand = kwargs["brand"]
        self.voltage = kwargs["voltage"]

    def return_as_dictionary(self):
        output_dict = super().return_as_dictionary()
        output_dict["brand"] = self.brand
        output_dict["voltage"] = self.voltage

        return output_dict
