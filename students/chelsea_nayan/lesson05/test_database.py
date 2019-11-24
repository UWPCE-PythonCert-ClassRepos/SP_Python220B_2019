'''Testing database.py'''

from unittest import TestCase
import logging
import database

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
PATH = ('C:\\Users\\chels\\SP_Python220B_2019\\students\\chelsea_nayan\\lesson05\\')

class TestDatabase(TestCase):
    '''test the basic functions in database.py'''

    def test_import_data(self):
        '''Test import_data function'''
        database.clear_all()

        # Test that the file not found error works for all three csv files
        import_test_one = database.import_data(PATH, 'DNE_products.csv', 'DNE_customers.csv',
                                               'DNE_rentals.csv')
        import_test_two = database.import_data(PATH, 'products.csv', 'customers.csv', 'rentals.csv')
        self.assertEqual(import_test_one, [(0, 0, 0), (1, 1, 1)]) # File Not Found
        self.assertEqual(import_test_two, [(6, 6, 9), (0, 0, 0)]) # File exists

    def test_show_available_products(self):
        '''Test show_available_products function'''
        database.clear_all()
        database.import_data(PATH, 'products.csv', 'customers.csv', 'rentals.csv')

        expected = {'p001': {'description': 'water bending scroll', 'product_type': 'artificat',
                             'quantity_available': '10'},
                    'p002': {'description': 'space sword', 'product_type': 'weaponry',
                             'quantity_available': '1'},
                    'p003': {'description': 'cactus juice', 'product_type': 'food',
                             'quantity_available': '3'},
                    'p004': {'description': 'meat jerky', 'product_type': 'food',
                             'quantity_available': '15'},
                    'p005': {'description': 'dual swords', 'product_type': 'weaponry',
                             'quantity_available': '2'},
                    'p006': {'description': 'blue mask', 'product_type': 'artifact',
                             'quantity_available': '0'}}

        dict_test = database.show_available_products()

        self.assertEqual(expected, dict_test)
        database.clear_all()

    def test_show_rentals(self):
        '''Test show_available_products function'''
        database.clear_all()
        database.import_data(PATH, 'products.csv', 'customers.csv', 'rentals.csv')

        expected_1 = {'c004': {'name': 'Sokka', 'address': 'Southern Water Tribe',
                               'phone_number': '1-206-444-4444', 'email': 'boomerang@gmail.com'},
                      'c005': {'name': 'Toph', 'address': 'Southern Earth Kingdom',
                               'phone_number': '1-206-555-5555', 'email': 'earth@gmail.com'}}

        expected_2 = {'c001': {'name': 'Aang', 'address': 'Eastern Air Temple',
                               'phone_number': '1-206-111-1111', 'email': 'avatar@gmail.com'},
                      'c006': {'name': 'Zuko', 'address': 'Fire Nation',
                               'phone_number': '1-206-666-6666', 'email': 'pride@gmail.com'}}

        dict_test_1 = database.show_rentals('p004') # meat jerky
        dict_test_2 = database.show_rentals('p006') # blue mask

        self.assertEqual(expected_1, dict_test_1)
        self.assertEqual(expected_2, dict_test_2)

        database.clear_all()
