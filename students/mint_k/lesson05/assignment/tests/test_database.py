"""Unit testing"""

from unittest import TestCase
from codes import database


class DatabaseTests(TestCase):
    """This is to test the database.py"""

    def test_import_data(self):
        """This is to test import_data function in database.py"""

        #purposely entering non existing file names
        directory_name = 'codes/'
        product_file = 'products1.csv'
        customer_file = 'customers1.csv'
        rentals_file = 'rentals1.csv'
        my_counts, my_errors = database.import_data(directory_name, product_file, 
                                                    customer_file, rentals_file)
        self.assertEqual(my_counts, (0, 0, 0))
        self.assertEqual(my_errors, (1, 1, 1))

        #entering real file names
        directory_name = 'codes/'
        product_file = 'products.csv'
        customer_file = 'customers.csv'
        rentals_file = 'rentals.csv'
        my_counts, my_errors = database.import_data(directory_name, product_file, 
                                                    customer_file, rentals_file)
        self.assertEqual(my_counts, (8, 5, 9))
        self.assertEqual(my_errors, (0, 0, 0))



    def test_access_csv(self):
        """To test access_csv function. It should read the csv file and return data"""
        file_name = 'codes/customers.csv'
        my_list = database.access_csv(file_name)
        my_answer = {'user_id': 'user001', 'name': 'Jeff Bezos', 
                     'address': '879 Market Dr', 'phone_number': '555-772-1779', 
                     'email': 'jeff.bezos@amazon.com'}
        self.assertEqual(my_list[0], my_answer)

        file_name = 'codes/products.csv'
        my_list = database.access_csv(file_name)
        my_answer = {'description': 'desk', 'product_id': 'prd001', 
                     'product_type': 'office', 'quantity_available': '3'}
        self.assertEqual(my_list[0], my_answer)

    def test_show_available_prods(self):
        """To test show_available_prods function. It should read the db and show available prods"""
        my_dict = database.show_available_products()
        self.assertEqual(my_dict['prd001']['product_type'], 'office')

    def test_show_rentals(self):
        """To test show_rentals"""
        product_id = 'prd002'
        my_dict = database.show_rentals(product_id)
        #print(my_dict)
        self.assertEqual(my_dict['user005']['name'], 'J Montero')
        self.assertEqual(my_dict['user003']['name'], 'Frank Sinatra')

