"""
    Test suite for the mongodb database functions

"""
import database
import unittest


class DatabaseTests(unittest.TestCase):
    """ Tests for database module"""

    def setUp(self):
        """Clean up database before each test."""
        mongo = database.MongoDBConnection()
        with mongo:
            db = mongo.connection.HPNortonDatabase
            product_data = db['product_data']
            customer_data = db['customer_data']
            rental_data = db['rental_data']

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
        pass

    def test_show_rentals(self):
        pass
