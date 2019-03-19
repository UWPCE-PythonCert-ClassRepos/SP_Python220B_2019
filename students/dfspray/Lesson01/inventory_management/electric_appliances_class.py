"""Electric appliances class"""

from inventory_class import Inventory

class ElectricAppliances(Inventory):
    """Creates a class that handles data on electric appliances"""

    def __init__(self, inventory_info, brand, voltage):
        """Initializes the class info"""

        #Creates common instance variables from the parent class
        Inventory.__init__(self, inventory_info)

        self.brand = brand
        self.voltage = voltage

    def return_as_dictionary(self):
        """Returns a dictionary of the appliance information"""
        output_dict = Inventory.return_as_dictionary(self)
        output_dict['brand'] = self.brand
        output_dict['voltage'] = self.voltage

        return output_dict
