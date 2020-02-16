"""
Module for testing linear.py function.
"""

from unittest import TestCase
import linear
import parallel


class LinearTest(TestCase):
    """Testing linear module."""

    def setUp(self):
        self.data_folder = 'sample_csv_files/'
        self.data_files = ['products.csv', 'customers.csv', 'rentals.csv']

    def test_import_data(self):
        """Test import data function."""
        linear.clear_database()
        import_result= linear.import_data(self.data_folder, *self.data_files)
        self.assertEqual(len(import_result), 3)
        self.assertEqual(import_result[0][0], 1000)

    def test_import_data_error(self):
        """Test error handling in import data function."""
        linear.clear_database()
        import_result = linear.import_data('wrong', 'place', 'to', 'look')
        self.assertEqual(len(import_result), 3)
        self.assertEqual(import_result[0][0], 0)

    def test_clear_database(self):
        """Test that clear_database empties linear."""
        linear.clear_database()
        available_products = linear.show_available_products()
        self.assertEqual({}, available_products)


class ParallelTest(TestCase):
    """Testing parallel module."""

    def setUp(self):
        self.data_folder = 'sample_csv_files/'
        self.data_files = ['products.csv', 'customers.csv', 'rentals.csv']

    def test_import_data(self):
        """Test import data function."""
        parallel.clear_database()
        import_result= parallel.parallel_import(self.data_folder, *self.data_files)
        self.assertEqual(len(import_result), 3)
        self.assertEqual(import_result[0][0], 1000)

    def test_import_data_error(self):
        """Test error handling in import data function."""
        parallel.clear_database()
        import_result = parallel.parallel_import('wrong', 'place', 'to', 'look')
        self.assertEqual(len(import_result), 3)
        self.assertEqual(import_result[0][0], 0)

    def test_clear_database(self):
        """Test that clear_database empties linear."""
        parallel.clear_database()
        available_products = parallel.show_available_products()
        self.assertEqual({}, available_products)








