"""
Furniture class

"""
from inventoryclass import Inventory

class Furniture(Inventory):
    """
    Furniture class

    """
    def __init__(self, material, size, *args):
        # Creates common instance variables from the parent class
        Inventory.__init__(self, *args)
        self.material = material
        self.size = size

    def return_as_dictionary(self):
        """ Function that return dictionary object for furniure.  """
        outputdict = {}
        outputdict = Inventory.return_as_dictionary(self)
        outputdict['material'] = self.material
        outputdict['size'] = self.size

        return outputdict
