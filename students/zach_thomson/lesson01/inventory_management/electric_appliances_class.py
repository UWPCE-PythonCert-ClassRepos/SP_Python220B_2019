'''module that creates an electric appliances class'''

# Electric appliances class
from inventory_management.inventory_class import Inventory


class ElectricAppliances(Inventory):
    '''class that creates an electrical appliance version of inventory item'''

    def __init__(self, productCode, description, market_price, rental_price, brand, voltage):
        Inventory.__init__(self, productCode, description, market_price, rental_price)
        # Creates common instance variables from the parent class
        self.brand = brand
        self.voltage = voltage

    def return_as_dictionary(self):
        output_dict = Inventory.return_as_dictionary(self)
        output_dict['brand'] = self.brand
        output_dict['voltage'] = self.voltage

        return output_dict
