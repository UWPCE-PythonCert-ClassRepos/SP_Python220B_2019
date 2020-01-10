"""Module for testing database"""

import unittest
from unittest import TestCase
import database as db

PATH = "C:/Users/kumar/Documents/GitHub/SP_Python220B_2019/" \
       "students/ramkumar_rajanbabu/lesson_05/assignment"

class TestDatabase(TestCase):
    """"""
    def test_import_data(self):
        """"""
        actual = db.import_data(PATH, "products.csv", "customers.csv",
                                "rentals.csv")
        expected = ((4,3,4), (0,0,0))
        #Count = 4 products rows, 3 customers rows, 4 rentals rows
        #Error = 0, 0, 0 
        self.assertEqual(actual, expected)
        
    def test_show_available_products(self):
        """"""
        actual = db
        actual.import_data(PATH, "products.csv", "customers.csv",
                                "rentals.csv")
        expected = {"51": {"description": "TV", "product_type": "Electric", 
                         "quantity_available": "4"},
                    "999": {"description": "Couch", "product_type": "Furniture", 
                         "quantity_available": "15"},
                    "325": {"description": "Laptop", "product_type": "Electric", 
                         "quantity_available": "112"},
                    "223": {"description": "Table", "product_type": "Furniture", 
                         "quantity_available": "25"}}
        self.assertEqual(actual.show_available_products(), expected)
        
        #test msg
        
if __name__ == "__main__":
    unittest.main()