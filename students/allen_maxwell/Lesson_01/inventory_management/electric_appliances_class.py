'''Electric Appliances Class Module'''

from inventory_class import Inventory

# pylint: disable = R0913, R0903

class ElectricAppliances(Inventory):
    '''Electrical Appliances Class'''
    def __init__(self, product_code, description, market_price, rental_price, brand, voltage):
        # Creates common instance variables from the parent class
        Inventory.__init__(self, product_code, description, market_price, rental_price)
        self.brand = brand
        self.voltage = voltage

    def return_as_dictionary(self):
        '''Returns the electrical appliances inventory as a dictionary'''
        output_dict = Inventory.return_as_dictionary(self)
        output_dict['brand'] = self.brand
        output_dict['voltage'] = self.voltage

        return output_dict
