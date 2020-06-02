"""Electric appliances class"""
# pylint:disable=R0913,R0903,W0613
from inventory_class import Inventory


class ElectricAppliances(Inventory):
    """
    Electric appliances class
    """

    def __init__(self, product_code, description, market_price, rental_price, brand, voltage):
        Inventory.__init__(self, product_code, description, market_price, rental_price)
        # Creates common instance variables from the parent class
        self.brand = brand
        self.voltage = voltage

    def return_as_dictionary(self):
        """
        :return: Electric appliances class as a dictionary
        """
        output_dict = {'product_code': self.product_code, 'description': self.description,
                       'market_price': self.market_price, 'rental_price': self.rental_price,
                       'brand': self.brand, 'voltage': self.voltage}

        return output_dict
