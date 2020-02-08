"""Unit tests for basic database functionalities"""

# pylint: disable=line-too-long, logging-format-interpolation

from unittest import TestCase
from database import setup_database, delete_collections, import_data, show_available_products, show_rentals, read_file, print_collections

class DatabaseTest(TestCase):
    """Test basic database functionalities"""

    def test_read_file(self):
        """Test read_file() funtion"""
        expect_response = [
            {'product_id': 'prd001', 'description': '60-inch TV stand', 'product_type': 'livingroom', 'quantity_available': 5},
            {'product_id': 'prd002', 'description': 'L-shaped sofa', 'product_type': 'livingroom', 'quantity_available': 0},
            {'product_id': 'prd003', 'description': 'bicycle', 'product_type': 'outdoor', 'quantity_available': 10},
        ]
        result = read_file('input', 'product.csv')
        self.assertEqual(result, expect_response)

    def test_read_invalid_file(self):
        """Test read_file() funtion"""
        with self.assertRaises(FileNotFoundError):
            read_file('input', 'dump_product.csv')

    def test_import_data(self):
        """Test import_data() function"""
        test_db = setup_database()
        delete_collections(test_db)
        record, error = import_data(test_db, 'input', 'product.csv', 'customer.csv', 'rentals.csv')
        self.assertTupleEqual(record, (3, 2, 5))
        self.assertTupleEqual(error, (0, 0, 0))
        print_collections(test_db)
        delete_collections(test_db)

    def test_import_invalid_data(self):
        """Test import_data() function"""
        test_db = setup_database()
        delete_collections(test_db)
        record, error = import_data(test_db, 'input', 'product.csv', 'dump_customer.csv', 'rentals.csv')
        with self.assertRaises(AssertionError):
            self.assertTupleEqual(error, (0, 0, 0))
            self.assertTupleEqual(record, (3, 2, 5))
        delete_collections(test_db)

    def test_show_available_products(self):
        """Test show_available_products() function"""
        expect_response = {
            'prd001': {'description': '60-inch TV stand', 'product_type': 'livingroom', 'quantity_available': 5},
            'prd003': {'description': 'bicycle', 'product_type': 'outdoor', 'quantity_available': 10},
        }
        test_db = setup_database()
        delete_collections(test_db)
        import_data(test_db, 'input', 'product.csv', 'customer.csv', 'rentals.csv')
        result = show_available_products(test_db['product'])
        self.assertDictEqual(result, expect_response)
        delete_collections(test_db)

    def test_show_rentals(self):
        """Test show_rentals() function"""
        expect_response = {
            'user002': {'name': 'Maya Data', 'address': '4936 Elliot Avenue', 'phone_number': '206-777-1927', 'email': 'mdata@uw.edu'},
        }
        test_db = setup_database()
        delete_collections(test_db)
        import_data(test_db, 'input', 'product.csv', 'customer.csv', 'rentals.csv')
        result = show_rentals(test_db['rentals'], test_db['customer'], 'prd003')
        self.assertDictEqual(result, expect_response)
        delete_collections(test_db)
