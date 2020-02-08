from unittest import TestCase
from unittest.mock import patch

import database

#PATH contains files with ideal data
PATH =  "C:\\_PythonClass\\AdvPython\\SP_Python220B_2019\\students\\bplanica\\lesson05\\assignment\\"

class BasicTests(TestCase):

    def test_a_clear_data(self):
        with patch ('builtins.input', side_effect ='Y'):
            database.clear_data()


    def test_b_import_data(self):
        #expected to import all, no errors
        expected = ((2, 2, 2), (0, 0, 0))
        actual = database.import_data(PATH,"products.csv","customers.csv","rentals.csv")
        self.assertEqual(actual, expected)


    def test_c_show_available_products(self):
        expected = {"prd001": {"description": "60-inch TV stand", "product_type": "livingroom",
                    "quantity_available": "3"}, "prd002": {"description": "L-shaped sofa",
                    "product_type": "livingroom", "quantity_available": "1"}}
        actual = database.show_available_products()
        self.assertEqual(actual, expected)


    def test_d_show_rentals(self):
        expected = {"user001": {"name": "Elisa Miles", "address": "4490 Union Street",
                    "phone": "206-922-0882", "email": "elisa.miles@yahoo.com"}}
        actual = database.show_rentals('prd002')
        self.assertEqual(actual, expected)


    def test_e_import_data(self):
        #data previously imported, expected to return all errors (duplicate keys)
        expected = ((0, 0, 0), (2, 2, 2))
        actual = database.import_data(PATH,"products.csv","customers.csv","rentals.csv")
        self.assertEqual(actual, expected)


    def test_f_import_data(self):
        #partial/incomplete data, expected to return a mix
        PATH =  "C:\\_PythonClass\\AdvPython\\SP_Python220B_2019\\students\\bplanica\\lesson05\\assignment\\test input files\\"
        with patch ('builtins.input', side_effect ='Y'):
            database.clear_data()

        expected = ((2, 3, 3), (2, 1, 1))
        actual = database.import_data(PATH,"products.csv","customers.csv","rentals.csv")
        self.assertEqual(actual, expected)


    def test_f_show_available_products(self):
        expected = {"prd001": {"description": "60-inch TV stand", "product_type": "livingroom",
                    "quantity_available": "3"}}
        actual = database.show_available_products()
        self.assertEqual(actual, expected)


    def test_g_import_data(self):
        #no data, expected to retuen no errors or imports
        with patch ('builtins.input', side_effect ='Y'):
            database.clear_data()

        expected = ((0, 0, 0), (0, 0, 0))
        actual = database.import_data(PATH,"blank_products.csv","blank_customers.csv","blank_rentals.csv")
        self.assertEqual(actual, expected)


    def test_h_import_data(self):
        with patch ('builtins.input', side_effect ='Y'):
            database.clear_data()

        with self.assertLogs(level ='ERROR'):
            database.import_data(PATH, "prod.csv", "cust.csv", "rent.csv")
