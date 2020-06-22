import unittest

from database import *
from unittest.mock import patch, mock_open

class TestCalculateRows(unittest.TestCase):
    TEST_DATA = '\n' * 500

    @patch("builtins.open", new_callable=mock_open, read_data=TEST_DATA)
    def test_open3(self, mock_open):
        line_count = calculate_rows(mock_open)
        self.assertEqual(line_count, 499)


class TestImport(unittest.TestCase):
    def test_import_bad_data(self):
        results = import_data('.', 'products.csv', 'bad_file', 'rentals.csv')
        self.assertRaises(FileNotFoundError)
        self.assertEqual(results, ((6, 0, 4), (0, 1, 0)))

    def test_import_data(self):
        results = import_data('.', 'products.csv', 'customer.csv', 'rentals.csv')
        self.assertEqual(results, ((6, 4, 4), (0, 0, 0)))

class TestProducts(unittest.TestCase):
    def setUp(self):
        import_data('.', 'products.csv', 'customer.csv', 'rentals.csv')

    def test_show_rentals(self):
        customers = show_rentals(7298)
        expected = {'user001':
                        {
                            'name': 'Mike Johnson',
                            'address': '1200 Fauntleroy Ave SW',
                            'email': 'mike.johnson@gmail.com',
                            'phone_number': '206-519-5554'
                        },
                    'user002': {
                                    'name': 'Alex Jackson',
                                    'address': '1206 California Ave SW',
                                    'email': 'ajax206@gmail.com',
                                    'phone_number': '206-519-5555'
                                }
                    }
        self.assertEqual(customers, expected)

class TestAvailability(unittest.TestCase):
    def setUp(self):
        import_data('.', 'products.csv', 'customer.csv', 'rentals.csv')

    def test_show_availability(self):
        available = show_available_products()
        print(available)
        expected = {
            5001:
                {
                    'quantity_available': 17,
                    'description': 'computer',
                    'product_type': 'electronic'
                },
            2367:
                {
                    'quantity_available': 4,
                    'description': 'beer',
                    'product_type': 'food'
                },
            4598:
                {
                    'quantity_available': 229,
                    'description': 'sunglasses',
                    'product_type': 'accessory'
                },
            7227:
                {
                    'quantity_available': 1057,
                    'description': 'pong table',
                    'product_type': 'furniture'
                }
        }
        self.assertEqual(available, expected)


if __name__ == '__main__':
    unittest.main()
