"""# Electric appliances class"""
from inventory_class import Inventory # pylint: disable=import-error


class ElectricAppliances(Inventory):

    """ElectricAppliances class"""

    # pylint: disable=too-few-public-methods

    def __init__(self, product_code, description, market_price, rental_price, brand, voltage):
        # pylint: disable=too-many-arguments
        Inventory.__init__(self, product_code, description, market_price, rental_price)
        # Creates common instance variables from the parent class

        self.brand = brand
        self.voltage = voltage

    def return_as_dictionary(self):
        """Function to return Inventory as dictionary"""
        output_dict = Inventory.return_as_dictionary()
        output_dict['brand'] = self.brand
        output_dict['voltage'] = self.voltage

        return output_dict
