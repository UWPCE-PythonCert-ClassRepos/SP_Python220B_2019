from database import *
from unittest import TestCase


class test_database(TestCase):
    """This class includes all the required
    Test functions for testing database.py"""

    def setUp(self):
        mongo = MongoDBConnection()
        with mongo:
            mongo_db = mongo.connection.customer_rental  # name of database
            customer_info = mongo_db['customer_info']
            product_info = mongo_db['product_info']
            rental_info = mongo_db['rental_info']
            customer_info.drop()
            product_info.drop()
            rental_info.drop()


    def test_import_data(self):
        """Testing import_data and show_available_products """
        expected_result = {'prd001':
                          {'description': '60-inch TV stand', 'product_type': 'livingroom', 'quantity_available': '25'},
                           'prd002': {'description': 'L-shaped sofa', 'product_type': 'livingroom', 'quantity_available': '8'}}

        import_data ('test_input_files', 'customer_csv', 'product.csv', 'rental_csv')
        self.assertEqual(expected_result, show_available_products())

    def test_show_rentals(self):
        """Testing import_data and show_rentals """
        expected_result = {'user002': {'name': 'meysam boston', 'email': 'meysam_boston@gmail.com', 'address': '174 Elliot bay', 'phone_number': '630-282-617'}}
        import_data ('test_input_files','customer_csv', 'product.csv', 'rental_csv')
        self.assertEqual(expected_result, show_rentals('prd001'))

