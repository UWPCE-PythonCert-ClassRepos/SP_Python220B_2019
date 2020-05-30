"""
Creates an Electric appliance object that will be added
to the inventory configuration.
"""
from inventory_management.inventory import Inventory


class ElectricAppliances(Inventory):
    """
    A subclass of Inventory that is an electric appliance
    and contains extra instance attributes of brand and
    voltage.

    :param brand: Describes the brand of the manufacturer
    :type brand: str
    :param voltage: The electricity voltage of the appliance
    :type voltage: float
    """

    def __init__(self, product_code, description,
                 market_price, rental_price, brand, voltage):
        # Creates common instance variables from the parent class
        super().__init__(product_code, description, market_price, rental_price)
        self.brand = brand
        self.voltage = voltage

    def return_as_dictionary(self):
        output_dict = super().return_as_dictionary()
        output_dict['brand'] = self.brand
        output_dict['voltage'] = self.voltage

        return output_dict
