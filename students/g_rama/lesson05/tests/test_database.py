"""Testing the database.py"""
import logging
import unittest
import pytest
import sys
sys.path.append('/Users/guntur/PycharmProjects/uw/p220/SP_Python220B_2019/'
                'students/g_rama/lesson05/src/')
import database


class TestDatabase(unittest.TestCase):

    @pytest.mark.parametrize('directory_name, product_file, customer_file, rentals_file, expected_output', [
        ("/Users/guntur/PycharmProjects/uw/", "product_file1", "customer_file1", "rentals_file1",
         "((0, 0, 0), (1, 1, 1))")
    ])
    def test_import_data(self):
        """Testing of the import data"""
        directory_name = "/Users/guntur/PycharmProjects/uw/" \
                         "p220/SP_Python220B_2019/students/g_rama/lesson05/src/data"
        added, errors = database.import_data(directory_name, "products1.csv", "customers1.csv", "rentals1.csv")

        #added, errors = database.import_data(directory_name, product_file, customer_file, rentals_file)
        actual_output = added, errors
        expected_output = ((0, 0, 0), (1, 1, 1))
        assert actual_output == expected_output

    def test_show_available_products(self):
        """Testing the available products function"""
        directory_name = "/Users/guntur/PycharmProjects/uw/" \
                         "p220/SP_Python220B_2019/students/g_rama/lesson05/src/data"
        database.import_data(directory_name, "products.csv", "customers.csv", "rentals.csv")

        expected_output = {'p101': {'Electronics', '5', 'TV'},
                           'p102': {'Lamp', 'Livingroom', '5'},
                           'p103': {'Dining Table', 'Diningroom', '5'},
                           'p104': {'5', 'bedroom', 'Queen bed'},
                           'p105': {'bedroom', '5', 'Kung bed'},
                           'p106': {'studyroom', 'Study Table', '5'},
                           'p107': {'kidsroom', 'Bunk Bed', '5'},
                           'p108': {'Microwave', 'Electronics', '5'},
                           'p109': {'Fan', 'livingroom', '5'},
                           'p110': {'5', 'livingroom', 'Heater'}}
        actual_data = database.show_available_products()
        database.drop_collections()
        self.assertEqual(expected_output,actual_data)

    def test_show_rentals(self):
        """Function to test the return of user details for a product that is rented"""
        directory_name = "/Users/guntur/PycharmProjects/uw/" \
                         "p220/SP_Python220B_2019/students/g_rama/lesson05/src/data"
        database.import_data(directory_name, "products.csv", "customers.csv", "rentals.csv")
        expected_data = {'UID103': {'dom@gmail.com', '3 Seattle Dr', 'Dom'},
                         'UID105': {'5 Vincent dr', 'Dan', 'dan@gmail.com'},
                         'UID101': {'1 Redmond dr', 'Sam', 'sam@gmail.com'}}
        actual_data = database.show_rentals("p101")
        database.drop_collections()
        self.assertEqual(expected_data, actual_data)


if __name__ == '__main__':
    unittest.main()
