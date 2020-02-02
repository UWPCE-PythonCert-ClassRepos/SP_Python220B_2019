"""Furniture class"""

from inventory_management.inventory_class import Inventory


class Furniture(Inventory):
    """Defines characteristics of furniture in inventory"""

    # Creates common instance variables from the parent class
    def __init__(self, product_code, description, market_price, rental_price,
                 material, size):

        Inventory.__init__(self, product_code, description, market_price,
                           rental_price)

        self.material = material
        self.size = size


    # Returns characteristics of furniture as dict
    def return_as_dictionary(self):
        """Returns characteristics of furniture as dict"""

        output_dict = Inventory.return_as_dictionary(self)
        output_dict['material'] = self.material
        output_dict['size'] = self.size

        return output_dict
