# pylint: disable=invalid-name
"""
Unit tests
"""
from unittest import TestCase
import database


class TestDatabase(TestCase):
    """Test database functions"""

    def setUp(self):
        # really wish there was a way to do this easily in memory
        mongo = database.MongoDBConnection()
        with mongo:
            db = mongo.connection.test_database
            db['customers'].drop()
            db['products'].drop()
            db['rentals'].drop()

    def tearDown(self):
        mongo = database.MongoDBConnection()
        with mongo:
            db = mongo.connection.test_database
            db['customers'].drop()
            db['products'].drop()
            db['rentals'].drop()

    def test_import_data(self):
        """Test the import_data function"""
        t1, t2 = database.import_data("data",
                                      "products.csv",
                                      "customers.csv",
                                      "rentals.csv")
        self.assertEqual(t1[0], 3)
        self.assertEqual(t1[1], 2)
        self.assertEqual(t1[2], 3)
        self.assertEqual(t2[0], 0)
        self.assertEqual(t2[1], 0)
        self.assertEqual(t2[2], 0)
        t3, t4 = database.import_data("data",
                                      "doesnotexist.csv",
                                      "customers.csv",
                                      "rentals.csv")
        self.assertEqual(t3[0], 0)
        self.assertEqual(t3[1], 2)
        self.assertEqual(t3[2], 3)
        self.assertEqual(t4[0], 1)
        self.assertEqual(t4[1], 0)
        self.assertEqual(t4[2], 0)

    def test_show_available_products(self):
        """Test the show_available_products function"""
        # import some data to play with
        database.import_data("data",
                             "products.csv",
                             "customers.csv",
                             "rentals.csv")

        # get the data back as a big dict
        products = database.show_available_products()

        # check that output is as expected for an arbitrary id
        expected = {
            'description': "60-inch TV stand",
            'product_type': "livingroom",
            'quantity_available': 3
        }
        self.assertEqual(products['prd001'], expected)

        # check that products with quantity of 0 are excluded
        self.assertEqual(len(products), 2)

    def test_show_rentals(self):
        """Test the show_rentals function"""
        # import some data to play with
        database.import_data("data",
                             "products.csv",
                             "customers.csv",
                             "rentals.csv")

        # fetch data and compare to expected
        rentaldata = database.show_rentals("prd001")
        expected = {
            'user001': {
                'name': "John Doe",
                'address': "123 Example Street",
                'phone_number': "15551234567",
                'email': "john@example.com"
            },
            'user002': {
                'name': "Jane Poe",
                'address': "456 Example Lane",
                'phone_number': "15557654321",
                'email': "jane@example.com"
            }
        }
        self.assertEqual(rentaldata, expected)
