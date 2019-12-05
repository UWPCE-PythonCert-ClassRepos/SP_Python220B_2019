"""Inventory class"""
class inventory:
    """Inventory class"""

    def __init__(self, productCode, description, marketPrice, rentalPrice):
        self.productCode = productCode
        self.description = description
        self.marketPrice = marketPrice
        self.rentalPrice = rentalPrice

    def returnAsDictionary(self):
        output_dict = {}
        output_dict['productCode'] = self.productCode
        output_dict['description'] = self.description
        output_dict['marketPrice'] = self.marketPrice
        output_dict['rentalPrice'] = self.rentalPrice
        return output_dict
