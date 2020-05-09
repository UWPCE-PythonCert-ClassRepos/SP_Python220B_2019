from unittest import TestCase
from inventory_management import market_prices as mp
from inventory_management import electric_appliances_class as ea
from inventory_management import inventory_class as inv


class market_prices_test(TestCase):
    """for market_prices module."""
    def setUp(self):
        """set up instance for Market Price tests."""
        print('setUp')
        self.item_code = 12345

    def test_get_latest_price(self):
        """Test get_latest_price module"""
        print('test_get_latest_price')
        actual_price = mp.get_latest_price(12345)
        assert actual_price == 24


class InventoryTests(TestCase):
    """Perform tests on inventory_class module."""

    def setUp(self):
        """Define set up characteristics of inventory tests."""
        print('setUp')
        self.item_code = 12345
        self.description = "First Product"
        self.market_price = 800
        self.rental_price = 25
        self.test_inv = inv.Inventory(self.item_code,
                                      self.description,
                                      self.market_price,
                                      self.rental_price
                                      )
        self.test_inv_dict = self.test_inv.return_as_dictionary()

    def test_inv_creation(self):
        """Compare setup dict to intended dict created."""
        print('test_inv_creation')
        compare_dict = {'item_code': 12345,
                        'description': "First Product",
                        'market_price': 800,
                        'rental_price': 25
                        }
        self.assertEqual(self.item_code, 12345)
        self.assertEqual(self.description, "First Product")
        self.assertEqual(self.market_price, 800)
        self.assertEqual(self.rental_price, 25)
        self.assertDictEqual(self.test_inv_dict, compare_dict)
