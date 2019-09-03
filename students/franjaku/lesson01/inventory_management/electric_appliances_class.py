# Electric appliances class
"""
Module contains the electric appliance class.
"""
from inventory_management.inventory_class import Inventory


class ElectricAppliances(Inventory):
    """
    Electric appliances class.
    Define electric appliances I guess...
    """
    def __init__(self, product_code, description, market_price, rental_price, **kwargs):
        Inventory.__init__(self, product_code, description, market_price,
                           rental_price)  # Creates common instance variables from the parent class

        if "brand" in kwargs:
            self.brand = kwargs['brand']
        else:
            self.brand = "N/A"

        if "voltage" in kwargs:
            self.voltage = kwargs['voltage']
        else:
            self.voltage = "N/A"

    def return_as_dictionary(self):
        """
        Returns the appliance as a dictionary object
        :return: output dictionary with all the appliance properties
        """
        output_dict = Inventory.return_as_dictionary(self)
        output_dict['brand'] = self.brand
        output_dict['voltage'] = self.voltage

        return output_dict
