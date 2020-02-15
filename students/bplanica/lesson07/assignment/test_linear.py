from unittest import TestCase

import linear

#PATH contains files with ideal data
PATH =  "./test_input_files\\"

class BasicTests(TestCase):

    def test_a_clear_data(self):
        linear.clear_data()


    def test_b_import_product(self):
        #expected to import all, no errors
        processed, before, after, time = linear.import_product(PATH,"products.csv")
        self.assertEqual(2, processed)
        self.assertEqual(0, before)
        self.assertEqual(2, after)


    def test_b_import_customer(self):
        #expected to import all, no errors
        processed, before, after, time = linear.import_customer(PATH,"customers.csv")
        self.assertEqual(2, processed)
        self.assertEqual(0, before)
        self.assertEqual(2, after)


    def test_b_import_rental(self):
        #expected to import all, no errors
        processed, before, after, time = linear.import_rental(PATH,"rentals.csv")
        self.assertEqual(2, processed)
        self.assertEqual(0, before)
        self.assertEqual(2, after)


    def test_c_show_available_products(self):
        expected = {"prd00001": {"description": "60-inch TV stand", "product_type": "livingroom",
                    "quantity_available": "3"}, "prd00002": {"description": "L-shaped sofa",
                    "product_type": "livingroom", "quantity_available": "1"}}
        actual = linear.show_available_products()
        self.assertEqual(actual, expected)


    def test_c_show_rentals(self):
        expected = {"user00001": {"name": "Elisa Miles", "address": "4490 Union Street",
                    "phone": "206-922-0882", "email": "elisa.miles@yahoo.com"}}
        actual = linear.show_rentals('prd00002')
        self.assertEqual(actual, expected)
