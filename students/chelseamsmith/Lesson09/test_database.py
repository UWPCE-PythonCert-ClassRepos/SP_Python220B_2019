"""unit tests for database.py"""
from unittest import TestCase
from database import import_data, show_available_products, show_rentals, cleanup


class TestDatabase(TestCase):
    """tests for database.py"""

    def test_import_data_success(self):
        """tests successful import of data"""
        cleanup()
        actual = import_data('csvfiles', 'products.csv', 'customers.csv', 'rentals.csv')
        self.assertEqual(actual, ((4, 4, 5), (0, 0, 0)))

    def test_import_data_fails(self):
        """test failed import of data"""
        cleanup()
        actual = import_data('csvfiles', 'product.csv', 'customer.csv', 'rental.csv')
        self.assertEqual(actual, ((0, 0, 0), (1, 1, 1)))

    def test_show_available_products(self):
        """test show available products function"""
        cleanup()
        import_data('csvfiles', 'products.csv', 'customers.csv', 'rentals.csv')
        actual = show_available_products()
        expected = {"prd001": {"description": "60-in tv",
                               "product_type": "livingroom",
                               "quantity_available": "3"}}
        self.assertEqual(actual, expected)

    def test_show_rentals(self):
        """tests show rentals function"""
        cleanup()
        import_data('csvfiles', 'products.csv', 'customers.csv', 'rentals.csv')
        actual = show_rentals('prd001')
        expected = {"user001": {"name": "Elisa Miles", "address": "4490 Union Street",
                                "phone_number": "206-922-0882",
                                "email": "elisa.mile@yahoo.com"}}
        self.assertEqual(actual, expected)
