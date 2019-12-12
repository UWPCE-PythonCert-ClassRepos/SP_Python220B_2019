"""
This module contains a class for furniture items.
"""


from inventory_management import inventory_class as inv


class Furniture(inv.Inventory):
    """Contains class methods and attributes for furniture items."""
    def __init__(self, item_code, description, market_price,
                 rental_price, material, size):
        """Creates furniture item."""
        # Creates common instance variables from the parent class
        inv.Inventory.__init__(self, item_code, description,
                               market_price, rental_price)

        self.material = material
        self.size = size

    def return_as_dictionary(self):
        """Return furniture item information as a dictionary."""
        output_dict = {}
        output_dict['item_code'] = self.item_code
        output_dict['description'] = self.description
        output_dict['market_price'] = self.market_price
        output_dict['rental_price'] = self.rental_price
        output_dict['material'] = self.material
        output_dict['size'] = self.size

        return output_dict
