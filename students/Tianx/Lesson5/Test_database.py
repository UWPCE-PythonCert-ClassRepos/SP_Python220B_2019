from unittest import TestCase
import database as db


class TestDatabase(TestCase):
    def test_import_data(self):
        """Test importing data"""
        db.clear_db()
        counts, errors = db.import_data('/Users/Tian/Documents/PythonClass/Tianx/SP_Python220B_2019'
                           '/students/Tianx/Lesson5/',
                               'product.csv',
                               'customers.csv',
                               'rental.csv')
        self.assertEqual(counts, (4, 11, 10))
        self.assertEqual(errors, (0, 0, 0))

    def test_show_available_products(self):
        """Test show available products"""
        actual = db.show_available_products()
        expected = {'prd001': {'description': '60-inch TV stand',
                               'product_type': 'livingroom',
                               'quantity_available': '3'},
                    'prd002': {'description': 'L-shaped sofa',
                               'product_type': 'livingroom',
                               'quantity_available': '1'},
                    'prd003': {'description': 'Acacia kitchen table',
                               'product_type': 'kitchen',
                               'quantity_available': '7'
                               }}
        self.assertEqual(expected, actual)

    def test_show_rentals(self):
        """Test show rentals"""
        actual = db.show_rentals('prd001')
        expected = {'user010': {'address': '2717 Raccoon Run',
                                'email': 'joegarza@boeing.com',
                                'name': 'Jose Garza',
                                'phone_number': '206-946-8200'}}
        self.assertEqual(expected, actual)
