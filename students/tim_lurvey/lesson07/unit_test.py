#!/usr/env/bin python
"""Unit testing for MongoDB database functions"""

# pylint: disable=missing-function-docstring,line-too-long,wildcard-import,invalid-name,unused-variable,unused-wildcard-import

from unittest import TestCase
import linear
# import parallel


class LinearDatabaseTest(TestCase):
    """Test functions"""
    mongo = linear.mongo
    TEST_PATH = r"C:\Users\pants\PycharmProjects\SP_Python220B_2019\students\tim_lurvey\lesson05\assignment\test"
    DATA_PATH = r"C:\Users\pants\PycharmProjects\SP_Python220B_2019\students\tim_lurvey\lesson05\assignment\data"

    def test_database_connection(self):
        with self.mongo:
            db = self.mongo.connection.norton
            self.assertEqual(db.name,
                             "norton")
            self.assertEqual(self.mongo.connection.address,
                             ('127.0.0.1', 27017))

    def test_parse_file_data(self):
        file = "test.csv"
        parsed = linear.parsed_file_data(file, self.TEST_PATH)
        self.assertEqual(parsed[0],
                         {'this': 'red', 'that': 'blue', 'thing': 'hat', 'stuff': 'pen', 'number': '6'})
        self.assertEqual(parsed[1],
                         {'this': 'white', 'that': 'red', 'thing': '1,2,3', 'stuff': 'screw', 'number': '2'})

    def test_parse_file_data_error(self):
        file = "doesNotExist.csv"

        self.assertRaises(FileNotFoundError, linear.parsed_file_data, file, self.TEST_PATH)

    def test_import_data(self):
        pathx = r"C:\Users\pants\PycharmProjects\SP_Python220B_2019\students\tim_lurvey\lesson05\assignment\data"

        r, e = linear.import_data(path_name=pathx,
                                  product_file='products.csv',
                                  customer_file='customers.csv',
                                  rentals_file='rentals.csv')

        self.assertEqual(r, (18, 19616, 19617))
        self.assertEqual(e, (0, 0, 0,))

    def test_show_available_products(self):
        linear.delete_all_collections()

        r, e = linear.import_data(path_name=self.DATA_PATH,
                                  product_file='products.csv',
                                  customer_file='customers.csv',
                                  rentals_file='rentals.csv')

        response = linear.show_available_products()

        self.assertEqual(len(response), 18)

        self.assertEqual(response.get("prod000001"),
                         {'description': 'TV 50 inch',
                          'product_type': 'residential',
                          'quantity_available': '8'})

        self.assertEqual(response.get("prod000014"),
                         {'description': 'Leaf blower small',
                          'product_type': 'tools',
                          'quantity_available': '10'})

        linear.delete_all_collections()

    def test_show_rentals(self):
        linear.delete_all_collections()

        r, e = linear.import_data(path_name=self.DATA_PATH,
                                  product_file='products.csv',
                                  customer_file='customers.csv',
                                  rentals_file='rentals.csv')

        response = linear.show_rentals("prod000014")

        self.assertEqual(len(response), 1106)

        self.assertEqual(response.get("zuvelpa01"),
                         {'name': 'Paul Zuvella',
                          'address': 'San Mateo, CA USA',
                          'phone_number': '123-456-7890',
                          'email': 'Paul.Zuvella@gmail.com'})

        linear.delete_all_collections()


# class ParallelDatabaseTest(TestCase):
#     """Test functions"""
#     mongo = parallel.mongo
#     TEST_PATH = r"C:\Users\pants\PycharmProjects\SP_Python220B_2019\students\tim_lurvey\lesson05\assignment\test"
#     DATA_PATH = r"C:\Users\pants\PycharmProjects\SP_Python220B_2019\students\tim_lurvey\lesson05\assignment\data"
#
#     def test_database_connection(self):
#         with self.mongo:
#             db = self.mongo.connection.norton
#             self.assertEqual(db.name,
#                              "norton")
#             self.assertEqual(self.mongo.connection.address,
#                              ('127.0.0.1', 27017))
#
#     def test_parse_file_data(self):
#         file = "test.csv"
#         parsed = parallel.parsed_file_data(file, self.TEST_PATH)
#         self.assertEqual(parsed[0],
#                          {'this': 'red', 'that': 'blue', 'thing': 'hat', 'stuff': 'pen', 'number': '6'})
#         self.assertEqual(parsed[1],
#                          {'this': 'white', 'that': 'red', 'thing': '1,2,3', 'stuff': 'screw', 'number': '2'})
#
#     def test_parse_file_data_error(self):
#         file = "doesNotExist.csv"
#
#         self.assertRaises(FileNotFoundError, parallel.parsed_file_data, file, self.TEST_PATH)
#
#     def test_import_data(self):
#         pathx = r"C:\Users\pants\PycharmProjects\SP_Python220B_2019\students\tim_lurvey\lesson05\assignment\data"
#
#         r, e = parallel.import_data(directory_name=pathx,
#                                   product_file='products.csv',
#                                   customer_file='customers.csv',
#                                   rentals_file='rentals.csv')
#
#         self.assertEqual(r, (18, 19616, 19617))
#         self.assertEqual(e, (0, 0, 0,))
#
#     def test_show_available_products(self):
#         parallel.delete_all_collections()
#
#         r, e = parallel.import_data(directory_name=self.DATA_PATH,
#                                   product_file='products.csv',
#                                   customer_file='customers.csv',
#                                   rentals_file='rentals.csv')
#
#         response = parallel.show_available_products()
#
#         self.assertEqual(len(response), 18)
#
#         self.assertEqual(response.get("prod000001"),
#                          {'description': 'TV 50 inch',
#                           'product_type': 'residential',
#                           'quantity_available': '8'})
#
#         self.assertEqual(response.get("prod000014"),
#                          {'description': 'Leaf blower small',
#                           'product_type': 'tools',
#                           'quantity_available': '10'})
#
#         parallel.delete_all_collections()
#
#     def test_show_rentals(self):
#         parallel.delete_all_collections()
#
#         r, e = parallel.import_data(directory_name=self.DATA_PATH,
#                                   product_file='products.csv',
#                                   customer_file='customers.csv',
#                                   rentals_file='rentals.csv')
#
#         response = parallel.show_rentals("prod000014")
#
#         self.assertEqual(len(response), 1106)
#
#         self.assertEqual(response.get("zuvelpa01"),
#                          {'name': 'Paul Zuvella',
#                           'address': 'San Mateo, CA USA',
#                           'phone_number': '123-456-7890',
#                           'email': 'Paul.Zuvella@gmail.com'})
#
#         parallel.delete_all_collections()
