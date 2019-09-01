# test_inregration.py
"""Test the integrated product."""
from unittest import mock, TestCase
from inventory_management import main
from inventory_management.main import FULL_INVENTORY


class ModuleTests(TestCase):

    def test_integration(self):
        comp_dict = {}
        comp_dict['100'] = {'product_code': '100',
                            'description': 'furn_item',
                            'market_price': 24,
                            'rental_price': '5.00',
                            'material': 'cloth',
                            'size': 'm'}
        comp_dict['50'] = {'product_code': '50',
                           'description': 'elec_item',
                           'market_price': 24,
                           'rental_price': '30.00',
                           'brand': 'LG',
                           'voltage': '240'}

        # add electrical item
        electrical_item = ['50', 'elec_item', '30.00', 'n', 'y', 'LG', '240']
        with mock.patch('builtins.input', side_effect=electrical_item):
            main.add_new_item()

        # add furniture item
        furniture_item = ['100', 'furn_item', '5.00', 'y', 'cloth', 'm']
        with mock.patch('builtins.input', side_effect=furniture_item):
            main.add_new_item()

        self.assertIn('100', FULL_INVENTORY.keys())
        self.assertIn('50', FULL_INVENTORY.keys())

        self.assertEqual(FULL_INVENTORY, comp_dict)
