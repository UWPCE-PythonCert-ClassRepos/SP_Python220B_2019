import io
import inventory_management.main as M
from unittest import TestCase
from unittest.mock import patch


class ModulesTest(TestCase):

    def setUp(self):
        self.items = dict()
        self.inventory = dict()
        self.items[53] = ('GEN234', 'Generic Widget', 41.25, 'N', 'N')
        self.items[689] = (1321, 'Chair', 13.05, 'Y', 'wood', 'XL')
        self.items[127] = (1573, 'Samsung Microwave', 50.00, 'N', 'y', 'Samsung', 110)

        self.inventory['GEN234'] = {
            'product_code': 'GEN234',
            'description': 'Generic Widget',
            'market_price': 53,
            'rental_price': 41.25
        }
        self.inventory[1321] = {
            'product_code': 1321,
            'description': 'Chair',
            'market_price': 689,
            'rental_price': 13.05,
            'material': 'wood',
            'size': 'XL'
        }
        self.inventory[1573] = {
            'product_code': 1573,
            'description': 'Samsung Microwave',
            'market_price': 127,
            'rental_price': 50.00,
            'brand': 'Samsung',
            'voltage': 110
        }

    def test_workflow(self):
        # Verify that the FULL_INVENTORY doesn't contain expected items yet.
        with patch('sys.stdout', new=io.StringIO()) as stdout:
            with patch('builtins.input', side_effect=[1321], autospec=True):
                M.item_info()
                expected_init = "Item not found in inventory\n"
                self.assertEqual(expected_init, stdout.getvalue())

        # Add all items to the FULL_INVENTORY dictionary in main
        for k,v in self.items.items():
            with patch('builtins.input', side_effect=v):
                with patch('inventory_management.main.get_latest_price', return_value=k):
                    M.add_new_item()
        self.assertEqual(self.inventory, M.FULL_INVENTORY)

        # Verify that items are in the FULL_INVENTORY in main
        with patch('sys.stdout', new=io.StringIO()) as stdout1:
            with patch('builtins.input', side_effect=[1321], autospec=True):
                M.item_info()

                expected = "product_code:1321\n" \
                           "description:Chair\n" \
                           "market_price:689\n" \
                           "rental_price:13.05\n" \
                           "material:wood\n" \
                           "size:XL\n"
                self.assertEqual(expected, stdout1.getvalue())

        # Verify that items will return expected stdout statement
        with patch('sys.stdout', new=io.StringIO()) as stdout2:
            with patch('builtins.input', side_effect=[11321], autospec=True):
                M.item_info()
                expected_nf = "Item not found in inventory\n"
                self.assertEqual(expected_nf, stdout2.getvalue())

        # Ensure program exits gracefully
        with self.assertRaises(SystemExit):
            M.exit_program()
