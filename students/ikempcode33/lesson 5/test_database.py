"""Tests HP Norton Mongo DB"""
from unittest import TestCase
from database import import_data, show_available_products, show_rentals
class TestDatabase(TestCase):
    """Tests that CSV data is entered correctly and counted"""
    def test_import_data(self):
        data = import_data('csv_data', 'products.csv', 'customers.csv', 'rentals.csv')
        self.assertEqual(data, ((3, 3, 3), (0, 0, 0)))
    

    def test_show_available_products(self):
        """list all available products in the database"""
        import_data('csv_data', 'products.csv', 'customers.csv', 'rentals.csv')
        product_results = show_available_products()
        self.assertEqual(product_results, {'867': {'description': 'couch', 'product_type': 'livingroom', 'quantity': '8'},
                                           '1009': {'description': 'chair', 'product_type': 'kitchen', 'quantity': '2'},
                                           '148': {'description': 'table', 'product_type': 'office', 'quantity': '4'}})
    
    def test_show_rentals(self):
        """Tests that customer ID matches to rental user"""
        import_data('csv_data', 'products.csv', 'customers.csv', 'rentals.csv')
        rental_results = show_rentals('148')
        self.assertEqual(rental_results, {'27654': {'name': 'Matt Bell', 'address': '410 3rd Ave, Seattle, WA',
                                                    'phone': '425-900-8976', 'email': 'mbell@google.com'}})
