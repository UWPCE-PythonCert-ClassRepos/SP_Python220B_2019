from unittest import TestCase
from database_redo import import_data, show_available_products, show_rentals

class TestDataBase(TestCase):

    def test_import_data_good(self):
        results = import_data('input_csv_redo', 'products.csv', 'customer.csv', 'rentals.csv')
        self.assertEqual(results, ((4,4,4), (0,0,0)))

    def test_import_data_bad(self):
        results = import_data('input_csv_redo', 'products1.csv', 'customer1.csv', 'rentals1.csv')
        self.assertEqual(results, ((0, 0, 0), (1, 1, 1)))

    def test_show_available_products(self):
        import_data('input_csv_redo', 'products.csv', 'customer.csv', 'rentals.csv')
        results = show_available_products()
        self.assertEqual(results, {'prd001': {'description': '60_inch_tv', 'product_type': 'Living_room', 'quantity_available': '3'},
                                   'prd002': {'description': 'L_shaped_sofa', 'product_type': 'Living_room', 'quantity_available': '1'},
                                   'prd003': {'description': 'Queen_bed', 'product_type': 'Bed_room', 'quantity_available': '2'},
                                   'prd004': {'description': 'Blender', 'product_type': 'Kitchen', 'quantity_available': '5'}})

    def test_show_rentals(self):
        import_data('input_csv_redo', 'products.csv', 'customer.csv', 'rentals.csv')
        results = show_rentals('prd003')
        self.assertEqual(results, {'user001': {'name': 'Elisa Miles', 'address': '4490 Union Street',
                                              'phone_number': '206-922-0882', 'email': 'elisa.miles@yahoo.com'}})
