""" Unit testing for database.py """

from unittest import TestCase
import database

class DatabaseTests(TestCase):
    """ Define a class for testing database functions """

    def test_import_data(self):
        """ Test importing data from csv files """

        # Test with valid files
        add_tuple, error_tuple = database.import_data("csv_files", "products.csv",
                                                      "customers.csv", "rentals.csv")
        self.assertEqual(add_tuple, (3, 3, 5))
        self.assertEqual(error_tuple, (0, 0, 0))

        # Test with missing files
        add_tuple, error_tuple = database.import_data("csv_files", "products1.csv",
                                                      "customers1.csv", "rentals1.csv")
        self.assertEqual(add_tuple, (0, 0, 0))
        self.assertEqual(error_tuple, (1, 1, 1))

    def test_show_available_products(self):
        """ Test showing available products """

        database.import_data("csv_files", "products.csv", "customers.csv", "rentals.csv")
        expected_products = {'prd001': {'description': 'Leather Sofa',
                                        'product_type': 'Furniture',
                                        'quantity_available': '5'},
                             'prd002': {'description': 'Toaster Oven',
                                        'product_type': 'Electric Appliance',
                                        'quantity_available': '3'}}

        available_products = database.show_available_products()
        self.assertEqual(available_products, expected_products)

    def test_show_rentals(self):
        """ Test showing users who have rented an item """

        database.import_data("csv_files", "products.csv", "customers.csv", "rentals.csv")
        expected_users = {'user003': {'name': 'Cyril Figgis',
                                      'address': '789 Alder Ave',
                                      'phone_number': '234-986-1829',
                                      'email': 'cyril.figgis@yahoo.com'},
                          'user002': {'name': 'Lana Kane',
                                      'address': '456 Birch St.',
                                      'phone_number': '987-654-3210',
                                      'email': 'lana.kane@hotmail.com'}}

        users_who_rented = database.show_rentals("prd001")
        self.assertEqual(users_who_rented, expected_users)
