"""
Electric appliances Module
"""
from inventory import Inventory

class Electric_Appliances(Inventory):
    """ The ElectricAppliances class """
    def __init__(self, product_code, description, market_price,
                 rental_price, brand, voltage):
        """ Creates common instance variables from the parent class """
        Inventory.__init__(self, product_code, description, market_price,
                           rental_price)


        self.brand = brand
        self.voltage = voltage

    def return_as_dictionary(self):
        """ Function to return appliance as a dictionary """
        output = {}
        output['productCode'] = self.product_code
        output['description'] = self.description
        output['marketPrice'] = self.market_price
        output['rentalPrice'] = self.rental_price
        output['brand'] = self.brand
        output['voltage'] = self.voltage

        return output
