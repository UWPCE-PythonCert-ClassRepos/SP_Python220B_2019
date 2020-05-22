#!/usr/bin/env python3
"""
This module includes integration tests for the inventory management system.
"""
import io
from unittest import TestCase
from unittest.mock import patch
from inventory_management import main as m


class IntegrationTests(TestCase):
    """Perform integration tests inventory_management package."""
    def setUp(self):
        """Peform setup of tests."""
        self.new_inv_item = ['1', 'Knife Set', 10, 'n', 'n']
        self.new_furn_item = ['2', 'Couch', 25, 'y', 'Cloth', 'L']
        self.new_elec_item = ['3', 'Dryer', 100, 'n', 'y', 'Samsung', 12]

    def test_integration(self):
        """Test all modules together."""
        m.FULL_INVENTORY = {}
        # TEST ADDING FIRST ITEM (INVENTORY)
        with patch('builtins.input', side_effect=self.new_inv_item):
            with patch('inventory_management.market_prices.get_latest_price',
                       return_value=100):
                m.addnew_item()
                self.assertEqual(m.FULL_INVENTORY,
                                 {'1': {'item_code': '1',
                                        'description': 'Knife Set',
                                        'market_price': 100,
                                        'rental_price': 10
                                        }
                                  }
                                 )
        # TEST ADDING SECOND ITEM (FURNITURE)
        with patch('builtins.input', side_effect=self.new_furn_item):
            with patch('inventory_management.market_prices.get_latest_price',
                       return_value=600):
                m.addnew_item()
                self.assertEqual(m.FULL_INVENTORY,
                                 {'1': {'item_code': '1',
                                        'description': 'Knife Set',
                                        'market_price': 100,
                                        'rental_price': 10},
                                  '2': {'item_code': '2',
                                        'description': 'Couch',
                                        'market_price': 600,
                                        'rental_price': 25,
                                        'material': 'Cloth',
                                        'size': 'L'}
                                  }
                                 )
        # TEST ADDING THIRD ITEM (ELECTRIC APPLIANCE)
        with patch('builtins.input', side_effect=self.new_elec_item):
            with patch('inventory_management.market_prices.get_latest_price',
                       return_value=1000):
                m.addnew_item()
                self.assertEqual(m.FULL_INVENTORY,
                                 {'1': {'item_code': '1',
                                        'description': 'Knife Set',
                                        'market_price': 100,
                                        'rental_price': 10},
                                  '2': {'item_code': '2',
                                        'description': 'Couch',
                                        'market_price': 600,
                                        'rental_price': 25,
                                        'material': 'Cloth',
                                        'size': 'L'},
                                  '3': {'item_code': '3',
                                        'description': 'Dryer',
                                        'market_price': 1000,
                                        'rental_price': 100,
                                        'brand': 'Samsung',
                                        'voltage': 12}
                                  }
                                 )
        # TEST PULLING ITEM INFO
        # Expected
        output_found = 'item_code: 1\n' \
                       'description: Knife Set\n' \
                       'market_price: 100\n' \
                       'rental_price: 10\n'
        output_not_found = 'Item not found in inventory\n'

        # Actual - Item Found
        with patch('builtins.input', side_effect='1'):
            with patch('sys.stdout', new_callable=io.StringIO) as real_out:
                m.item_info()
                self.assertEqual(output_found, real_out.getvalue())

        # Actual - Item Not Found
        with patch('builtins.input', side_effect='4'):
            with patch('sys.stdout', new_callable=io.StringIO) as real_out:
                m.item_info()
                self.assertEqual(output_not_found, real_out.getvalue())
