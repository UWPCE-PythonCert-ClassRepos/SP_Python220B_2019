"""
Module for testing database.py function.
"""

from unittest import TestCase
import database


class DataBaseTest(TestCase):
    """Testing database module."""

    def setUp(self):
        self.data_folder = 'data/'
        self.data_files = ['products.csv', 'customers.csv', 'rentals.csv']
        self.test_product_input = [{'product_id': 'prd001',
                                    'description': '60-inch TV stand',
                                    'product_type': 'livingroom',
                                    'quantity_available': 3},
                                   {'product_id': 'prd002',
                                    'description': 'L-shaped sofa',
                                    'product_type': 'livingroom',
                                    'quantity_available': 1},
                                   {'product_id': 'prd003',
                                    'description': 'Queen size bed frame',
                                    'product_type': 'bedroom',
                                    'quantity_available': 2},
                                   {'product_id': 'prd004',
                                    'description': 'Table with leaves',
                                    'product_type': 'diningroom',
                                    'quantity_available': 1},
                                   {'product_id': 'prd005',
                                    'description': 'Desk',
                                    'product_type': 'den',
                                    'quantity_available': 3},
                                   {'product_id': 'prd006',
                                    'description': 'Desk Light',
                                    'product_type': 'den',
                                    'quantity_available': 4},
                                   {'product_id': 'prd007',
                                    'description': 'Coffee Table',
                                    'product_type': 'livingroom',
                                    'quantity_available': 0},
                                   {'product_id': 'prd008',
                                    'description': 'Throw Pillow',
                                    'product_type': 'livingroom',
                                    'quantity_available': 10}]
        self.test_avail_prod_dict = {'prd001': {'description': '60-inch TV stand',
                                                'product_type': 'livingroom',
                                                'quantity_available': 3},
                                     'prd002': {'description': 'L-shaped sofa',
                                                'product_type': 'livingroom',
                                                'quantity_available': 1},
                                     'prd003': {'description': 'Queen size bed frame',
                                                'product_type': 'bedroom',
                                                'quantity_available': 2},
                                     'prd004': {'description': 'Table with leaves',
                                                'product_type': 'diningroom',
                                                'quantity_available': 1},
                                     'prd005': {'description': 'Desk',
                                                'product_type': 'den',
                                                'quantity_available': 3},
                                     'prd006': {'description': 'Desk Light',
                                                'product_type': 'den',
                                                'quantity_available': 4},
                                     'prd008': {'description': 'Throw Pillow',
                                                'product_type': 'livingroom',
                                                'quantity_available': 10}}
        self.test_show_rentals_dict = {'user003': {'name': 'Charles Dickens',
                                                   'address': '175 Pickering Ave',
                                                   'phone_number': '253-694-1021',
                                                   'email': 'pickwick@londonfog.org'},
                                       'user002': {'name': 'Burt Reynolds',
                                                   'address': '991 Walnut Wy',
                                                   'phone_number': '425-697-0192',
                                                   'email': 'bandit@aol.com'}}

    def test_import_csv(self):
        """Test import function."""
        input, count = database.import_csv('data/', 'products.csv')
        self.assertEqual(self.test_product_input, input)
        self.assertEqual(count, 8)

    def test_import_data(self):
        """Test import data function."""
        import_tuples = database.import_data(self.data_folder, *self.data_files)
        self.assertEqual(import_tuples, ((8, 7, 12), (0, 0, 0)))

    def test_import_data_error(self):
        """Test error handling in import data function."""
        import_tuples = database.import_data('wrong', 'place', 'to', 'look')
        self.assertEqual(import_tuples, ((0, 0, 0), (1, 1, 1)))

    def test_show_available_products(self):
        """Test that function returns dict of available products"""
        available_products = database.show_available_products()
        self.assertEqual(self.test_avail_prod_dict, available_products)

    def test_show_rentals(self):
        """Test that function returns dict of renters of input product ID."""
        renters = database.show_rentals('prd008')
        self.assertEqual(self.test_show_rentals_dict, renters)

    def test_clear_database(self):
        """Test that clear_database empties database."""
        database.clear_database()
        available_products = database.show_available_products()
        self.assertEqual({}, available_products)









