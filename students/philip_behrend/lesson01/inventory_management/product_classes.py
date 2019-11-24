"""Module for application classes"""

class Inventory:
    """Inventory class"""
    def __init__(self, product_code, description, market_price, rental_price):
        """init docstring"""
        self.product_code = product_code
        self.description = description
        self.market_price = market_price
        self.rental_price = rental_price

    def return_as_dictionary(self):
        """return inputs as dict"""
        output_dict = {}
        output_dict['product_code'] = self.product_code
        output_dict['description'] = self.description
        output_dict['market_price'] = self.market_price
        output_dict['rental_price'] = self.rental_price

        return output_dict

class ElectricAppliances(Inventory):
    """Electric appliances class"""
    def __init__(self, product_code, description, market_price, rental_price, brand, voltage):
        """Creates common instance variables from the parent class"""
        Inventory.__init__(self, product_code, description, market_price, rental_price)


        self.brand = brand
        self.voltage = voltage

    def return_as_dictionary(self):
        """return inputs as dict"""
        output_dict = {}
        output_dict['product_code'] = self.product_code
        output_dict['description'] = self.description
        output_dict['market_price'] = self.market_price
        output_dict['rental_price'] = self.rental_price
        output_dict['brand'] = self.brand
        output_dict['voltage'] = self.voltage


        return output_dict

class Furniture(Inventory):
    """Furniture class"""
    def __init__(self, product_code, description, market_price, rental_price, material, size):
        """ Creates common instance variables from the parent class"""
        Inventory.__init__(self, product_code, description, market_price, rental_price)

        self.material = material
        self.size = size

    def return_as_dictionary(self):
        """return inputs as dict"""
        output_dict = {}
        output_dict['product_code'] = self.product_code
        output_dict['description'] = self.description
        output_dict['market_price'] = self.market_price
        output_dict['rental_price'] = self.rental_price
        output_dict['material'] = self.material
        output_dict['size'] = self.size

        return output_dict