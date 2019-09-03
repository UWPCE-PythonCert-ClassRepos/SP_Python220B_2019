# Furniture class
"""Contains furniture class."""

from inventory_management.inventory_class import Inventory


class Furniture(Inventory):
    """Defines the furniture class."""
    def __init__(self, product_code, description, market_price, rental_price, **kwargs):
        Inventory.__init__(self, product_code, description, market_price,
                           rental_price)  # Creates common instance variables from the parent class

        if "size" in kwargs:
            self.size = kwargs["size"]
        else:
            self.size = "N/A"

        if "material" in kwargs:
            self.material = kwargs["material"]
        else:
            self.material = "N/A"

    def return_as_dictionary(self):
        """
        Return the furniture object as a dictionary
        Use the parent class function to assign all the attributes that we inherit from the parent.
        """

        output_dict = Inventory.return_as_dictionary(self)
        output_dict['material'] = self.material
        output_dict['size'] = self.size

        return output_dict
