from unittest import TestCase

import parallel
from queue import Queue

#PATH contains files with ideal data
PATH =  "./test_input_files\\"
QUEUE = Queue()

class BasicTests(TestCase):

    def test_a_clear_data(self):
        parallel.clear_data()


    def test_b_import_product(self):
        #expected to import all, no errors
        parallel.import_product(PATH, "products.csv", QUEUE)
        actual = QUEUE.get()
        self.assertEqual(2, actual[0])
        self.assertEqual(0, actual[1])
        self.assertEqual(2, actual[2])


    def test_b_import_customer(self):
        #expected to import all, no errors
        parallel.import_customer(PATH, "customers.csv", QUEUE)
        actual = QUEUE.get()
        self.assertEqual(2, actual[0])
        self.assertEqual(0, actual[1])
        self.assertEqual(2, actual[2])


    def test_b_import_rental(self):
        #expected to import all, no errors
        parallel.import_rental(PATH, "rentals.csv", QUEUE)
        actual = QUEUE.get()
        self.assertEqual(2, actual[0])
        self.assertEqual(0, actual[1])
        self.assertEqual(2, actual[2])


    def test_c_show_available_products(self):
        expected = {"prd00001": {"description": "60-inch TV stand", "product_type": "livingroom",
                    "quantity_available": "3"}, "prd00002": {"description": "L-shaped sofa",
                    "product_type": "livingroom", "quantity_available": "1"}}
        actual = parallel.show_available_products()
        self.assertEqual(actual, expected)


    def test_c_show_rentals(self):
        expected = {"user00001": {"name": "Elisa Miles", "address": "4490 Union Street",
                    "phone": "206-922-0882", "email": "elisa.miles@yahoo.com"}}
        actual = parallel.show_rentals('prd00002')
        self.assertEqual(actual, expected)
