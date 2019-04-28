# Inventory class
class Inventory:

    def __init__(self, product_code, description, market_price, rental_price):
        self.productCode = product_code
        self.description = description
        self.marketPrice = market_price
        self.rentalPrice = rental_price

    def return_as_dictionary(self):
        output_dict = {}
        output_dict['productCode'] = self.productCode
        output_dict['description'] = self.description
        output_dict['marketPrice'] = self.marketPrice
        output_dict['rentalPrice'] = self.rentalPrice

        return output_dict