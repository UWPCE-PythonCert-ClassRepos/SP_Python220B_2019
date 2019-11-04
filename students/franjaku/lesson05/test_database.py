"""
    Test suite for the mongodb database functions

"""
import unittest
import database


class DatabaseTests(unittest.TestCase):
    """ Tests for database module"""

    def setUp(self):
        """Clean up database before each test."""
        mongo = database.MongoDBConnection()
        with mongo:
            hp_db = mongo.connection.HPNortonDatabase
            product_data = hp_db['product_data']
            customer_data = hp_db['customer_data']
            rental_data = hp_db['rental_data']

            # drop all data in collections
            product_data.drop()
            customer_data.drop()
            rental_data.drop()

    def test_import_data(self):
        """Test import function"""
        directory_path = 'C:/Users/USer/Documents/UW_Python_Certificate/Course_2/' \
                         'SP_Python220B_2019/students/franjaku/lesson05/data_files'
        tup1, tup2 = database.import_data(directory_path, 'product_data.csv',
                                          'customer_data.csv', 'rental_data.csv')

        # assert the correct number of items were added
        self.assertEqual(tup1[0], 4)  # check number of products added
        self.assertEqual(tup1[1], 4)  # check number of customers added
        self.assertEqual(tup1[2], 4)  # check number of rentals added

        # check no errors occurred during addition
        self.assertEqual(tup2, ())

    def test_show_available_products(self):
        """
        Test that show_available_products() satisfies the following requirement:
            Returns a Python dictionary of products listed as available with the following fields:
                product_id
                description
                product_type
                quantity_available
        Assumes that import_data() works as intended
        """
        test_dict1 = database.show_available_products()

        # Check that an empty database returns an empty dict
        self.assertDictEqual(test_dict1, {})

        # Add products and check we return the added products
        directory_path = 'C:/Users/USer/Documents/UW_Python_Certificate/Course_2/' \
                         'SP_Python220B_2019/students/franjaku/lesson05/data_files'
        database.import_data(directory_path, 'product_data.csv', 'customer_data.csv',
                             'rental_data.csv')

        test_dict2 = database.show_available_products()

        expected_dict = {'prod1': {'product_id': '1',
                                   'description': 'Table',
                                   'product_type': 'Dining Room',
                                   'quantity_available': '25'},
                         'prod2': {'product_id': '2',
                                   'description': 'Chair',
                                   'product_type': 'Dining Room',
                                   'quantity_available': '654'},
                         'prod3': {'product_id': '3',
                                   'description': 'Mattress',
                                   'product_type': 'Bedroom',
                                   'quantity_available': '200'},
                         'prod4': {'product_id': '4',
                                   'description': 'Couch',
                                   'product_type': 'Living Room',
                                   'quantity_available': '36'}
                         }
        # print(expected_dict)
        # print(test_dict2)
        self.assertDictEqual(test_dict2, expected_dict)

    def test_show_rentals(self):
        """
        Test that show_rentals(product_id) satisfies the following requirement:
            Returns a Python dictionary with the following user information from users that have
            rented products matching product_id:
                user_id
                name
                address
                phone_number
                email
        """
        test_dict1 = database.show_rentals('1')

        # Check an empty collection returns an empty dict
        self.assertDictEqual(test_dict1, {})

        # Add rentals and check we return the added rentals by prod_id
        directory_path = 'C:/Users/USer/Documents/UW_Python_Certificate/Course_2/' \
                         'SP_Python220B_2019/students/franjaku/lesson05/data_files'
        database.import_data(directory_path, 'product_data.csv', 'customer_data.csv',
                             'rental_data.csv')

        test_dict2 = database.show_rentals('1')

        expected_dict = {'rental_2': {'customer_id': '2',
                                      'name': 'Jon',
                                      'address': '1900 43rd Ave E, Seattle WA 98112',
                                      'phone_number': '538-987-0245',
                                      'email': 'test2@test.com'},
                         'rental_3': {'customer_id': '1',
                                      'name': 'Jim',
                                      'address': '105 Main Street, Seattle WA 98109',
                                      'phone_number': '254-553-3600',
                                      'email': 'test1@test.com'}
                         }

        self.assertDictEqual(test_dict2, expected_dict)
