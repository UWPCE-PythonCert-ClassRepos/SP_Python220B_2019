import io

from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch

from inventory_management.market_prices import get_latest_price as MP
from inventory_management.furniture import Furniture
from inventory_management.inventory import Inventory
from inventory_management.electric_appliances import ElectricAppliances
import inventory_management.main as M

class InventoryTests(TestCase):

    def setUp(self):
        self.widget = Inventory('GEN234', 'Generic Widget', 400.25, 12.45)

    def test_create_furniture(self):
        self.assertEqual(self.widget.product_code, 'GEN234')
        self.assertEqual(self.widget.description, 'Generic Widget')
        self.assertEqual(self.widget.rental_price, 12.45)
        self.assertEqual(self.widget.market_price, 400.25)


    def test_return_as_dict(self):
        self.assertEqual(self.widget.return_as_dictionary().get('product_code'), 'GEN234')
        self.assertEqual(self.widget.return_as_dictionary().get('description'), 'Generic Widget')
        self.assertEqual(self.widget.return_as_dictionary().get('market_price'), 400.25)
        self.assertEqual(self.widget.return_as_dictionary().get('rental_price'), 12.45)


class FurnitureTests(TestCase):

    def setUp(self):
        self.new_chair = Furniture(1321, 'Chair', 1203.05, 35.00, 'wood', 'XL')

    def test_create_furniture(self):
        self.assertEqual(self.new_chair.size, 'XL')
        self.assertEqual(self.new_chair.material, 'wood')
        self.assertEqual(self.new_chair.rental_price, 35.00)
        self.assertEqual(self.new_chair.market_price, 1203.05)
        self.assertEqual(self.new_chair.description, 'Chair')
        self.assertEqual(self.new_chair.product_code, 1321)

    def test_return_as_dict(self):
        self.assertEqual(self.new_chair.return_as_dictionary().get('product_code'), 1321)
        self.assertEqual(self.new_chair.return_as_dictionary().get('description'), 'Chair')
        self.assertEqual(self.new_chair.return_as_dictionary().get('market_price'), 1203.05)
        self.assertEqual(self.new_chair.return_as_dictionary().get('rental_price'), 35.00)
        self.assertEqual(self.new_chair.return_as_dictionary().get('material'), 'wood')
        self.assertEqual(self.new_chair.return_as_dictionary().get('size'), 'XL')


class ElectricAppliancesTests(TestCase):

    def setUp(self):
        self.microwave = ElectricAppliances(1573, 'Samsung Microwave', 120.00, 125.00, 'Samsung', 120)

    def test_create_appliance(self):
        self.assertEqual(self.microwave.product_code, 1573)
        self.assertEqual(self.microwave.description, 'Samsung Microwave')
        self.assertEqual(self.microwave.market_price, 120.00)
        self.assertEqual(self.microwave.rental_price, 125.00)
        self.assertEqual(self.microwave.brand, 'Samsung')
        self.assertEqual(self.microwave.voltage, 120)

    def test_appliance_dict(self):
        self.assertEqual(self.microwave.return_as_dictionary().get('product_code'), 1573)
        self.assertEqual(self.microwave.return_as_dictionary().get('description'), 'Samsung Microwave')
        self.assertEqual(self.microwave.return_as_dictionary().get('market_price'), 120.00)
        self.assertEqual(self.microwave.return_as_dictionary().get('rental_price'), 125.00)
        self.assertEqual(self.microwave.return_as_dictionary().get('brand'), 'Samsung')
        self.assertEqual(self.microwave.return_as_dictionary().get('voltage'), 120)


class MarketPricesTests(TestCase):

    def setUp(self):
        self.tv_code = 24332
        self.table_code = 89773
        self.lamp_code = 7346

        self.tv = ElectricAppliances(self.tv_code, 'Samsung TV', 1200.00, 125.00, 'Samsung', 120)
        self.table = Furniture(self.table_code, 'Coffee Table', 300.00, 125.00, 'Glass', 'L')
        self.lamp = ElectricAppliances(self.lamp_code, 'Bed side lamp', 20.00, 23.00, 'Target', 9)

    def test_market_price(self):
        market_price = MP(self.lamp.product_code)

        self.assertEqual(market_price, 24)

    def test_tv_market_price(self):
        MP.get_latest_price = Mock(return_value=456)
        price = MP.get_latest_price(self.tv.product_code)

        self.assertEqual(price, 456)

    def test_table_market_price(self):
        MP.get_latest_price = Mock(return_value=self.table.market_price)
        table_price = MP.get_latest_price(self.table_code)

        self.assertEqual(table_price, self.table.market_price)


class MainTests(TestCase):

    def test_main_menu_option_1(self):
        with patch('builtins.input', side_effect='1', spec=True):
            call_1 = M.main_menu()
        expected = M.add_new_item
        self.assertEqual(call_1, expected)

    def test_main_menu_option_2(self):
        with patch('builtins.input', side_effect='2', spec=True):
            call_2 = M.main_menu()
        expected = M.item_info
        self.assertEqual(call_2, expected)

    def test_main_menu_option_3(self):
        with patch('builtins.input', side_effect='q', spec=True):
            call_3 = M.main_menu()
        expected = M.exit_program
        self.assertEqual(call_3, expected)

    def test_add_new_item_furniture(self):
        with patch('builtins.input', side_effect=['DTABLE12', 'Dining Table', 142.12, 'Y', 'Wood', 'L'], spec=True):
            with patch('sys.stdout', new=io.StringIO()) as stdout:
                M.add_new_item()
        expected = "New inventory item added\n"
        self.assertEqual(stdout.getvalue(), expected)

    def test_add_new_item_electrical(self):
        with patch('builtins.input', side_effect=['SMSNG123', 'TV', 12.00, 'N', 'Y', 'SAMSUNG', 120], spec=True):
            with patch('sys.stdout', new=io.StringIO()) as stdout:
                M.add_new_item()
        expected = "New inventory item added\n"
        self.assertEqual(stdout.getvalue(), expected)

    def test_add_new_item_inventory(self):
        with patch('builtins.input', side_effect=['rug5432', 'Rug', 132.10, 'N', 'N'], spec=True):
            with patch('sys.stdout', new=io.StringIO()) as stdout:
                M.add_new_item()
        expected = "New inventory item added\n"
        self.assertEqual(stdout.getvalue(), expected)

    def test_item_info_not_found(self):
        with patch('builtins.input', side_effect='SMSNG500', spec=True):
            with patch('sys.stdout', new=io.StringIO()) as stdout:
                M.item_info()
        expected = "Item not found in inventory\n"
        self.assertEqual(stdout.getvalue(), expected)

    def test_item_info(self):
        M.FULL_INVENTORY = \
            {'SMSNG123400': {
                'product_code': 'SMSNG123400',
                'description': 'TV',
                'market_price': 450,
                'rental_price': 12,
                'brand': 'SAMSUNG',
                'voltage': 120
            }
            }
        with patch('sys.stdout', new=io.StringIO()) as stdout:
            with patch('builtins.input', side_effect=['SMSNG123400'], autospec=True):
                M.item_info()

        expected = "product_code:SMSNG123400\n" \
                   "description:TV\n" \
                   "market_price:450\n" \
                   "rental_price:12\n" \
                   "brand:SAMSUNG\n" \
                   "voltage:120\n"
        self.assertEqual(expected, stdout.getvalue())

    def test_get_price(self):
        with patch('sys.stdout', new=io.StringIO()) as stdout:
            price = M.get_price('item_code_here')
            expected = "Get price\n"
        self.assertEqual(expected, stdout.getvalue())
        self.assertEqual(price, 24)

    def test_sys_exit(self):
        with self.assertRaises(SystemExit):
            M.exit_program()
