"""# Furniture class"""
from inventory_class import Inventory  # pylint: disable=import-error


class Furniture(Inventory):  # pylint: disable=too-few-public-methods

    """Furniture class to store the furniture data """

    def __init__(self, product_code, description, market_price, rental_price, material, size):
        # pylint: disable=too-many-arguments
        Inventory.__init__(self, product_code, description, market_price, rental_price)
        # Creates common instance variables from the parent class

        self.material = material
        self.size = size

    def return_as_dictionary(self):
        """Function to store furniture as a data dictionary"""
        output_dict = Inventory.return_as_dictionary(self)
        output_dict['material'] = self.material
        output_dict['size'] = self.size

        return output_dict
