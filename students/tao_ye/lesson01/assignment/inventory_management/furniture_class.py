""" This modue defines Furniture class """


from inventory_management.inventory_class import Inventory


class Furniture(Inventory):
    """ Furniture class """

    def __init__(self, product_code, description, market_price, rental_price, material, size):
        Inventory.__init__(self, product_code, description, market_price, rental_price)
        self.material = material
        self.size = size

    def return_as_dictionary(self):
        """ return the furniture item as dictionary """
        output_dict = Inventory.return_as_dictionary(self)
        output_dict['material'] = self.material
        output_dict['size'] = self.size

        return output_dict
