""" Furniture class """


from inventory_management.inventory_class import Inventory

# pylint: disable = too-many-arguments, too-few-public-methods


class Furniture(Inventory):
    """ Furniture object containing the furniture info  """
    def __init__(self, product_code, description, market_price, rental_price, material, size):

        # Creates common instance variables from the parent class
        Inventory.__init__(self, product_code, description, market_price, rental_price)

        self.material = material
        self.size = size

    def return_as_dictionary(self):
        """ Get the furniture info
        :return output_dict: A dictionary containing the furniture info
        """
        output_dict = {}
        output_dict['product_code'] = self.product_code
        output_dict['description'] = self.description
        output_dict['market_price'] = self.market_price
        output_dict['rental_price'] = self.rental_price
        output_dict['material'] = self.material
        output_dict['size'] = self.size

        return output_dict
