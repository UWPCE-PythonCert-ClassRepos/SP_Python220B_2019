# pylint: disable=W0401,W0614
'''
look into  sys.path.append()  to save
this in a separate folder
'''
from unittest import TestCase
from database import (import_data, show_available_products, show_rentals)

# print(import_data('csv_files', 'products.csv', 'customers.csv', 'rentals.csv'))
# print_mdb_collection()
# print(show_available_products())
# print(show_rentals('prd001'))


class TestDatabase(TestCase):
    '''UnitTest class to test database.py'''

    show_rentals_dict = {'user001': {'name': 'Stinky', 'address': '123 3rd St', 'phone_number': '206-420-9034', 'email': 'stink@hotmail.com'}, 'user002': {'name': 'Farter', 'address': '321 Walbutt', 'phone_number': '425-420-0192', 'email': 'fart@aol.com'}}

    available_products_dict = {'prd001': {'description': '60-inch TV stand', 'product_type': 'livingroom', 'quantity_available': '3'}, 'prd002': {'description': 'L-shaped sofa', 'product_type': 'livingroom', 'quantity_available': '1'}, 'prd003': {'description': 'Lazy Boy', 'product_type': 'bedroom', 'quantity_available': '2'}, 'prd004': {'description': 'Bidet', 'product_type': 'bathroom', 'quantity_available':'1'}, 'prd005': {'description': 'Extra Large Bidet',
                                    'product_type': 'bathroom', 'quantity_available': '3'}}

    def setup(self):
        self.context_mgr = MongoDBConnection()

    def test_import_data(self):
        '''test import data function.'''
        # First reset the db
        errors, count = import_data('csv_files', 'products.csv',
                                    'customers.csv', 'rentals.csv')
        self.assertEqual(count, (5, 4, 8))
        self.assertEqual(errors, (0, 0, 0))

    def test_list_available_products(self):
        '''test list all products.'''
        avail_products = show_available_products()
        self.assertEqual(avail_products, self.available_products_dict)

    def test_show_rentals(self):
        '''test show rentals.'''
        rentals = show_rentals('prd001')
        self.assertEqual(rentals, self.show_rentals_dict)
