import sys
from io import StringIO
from unittest import TestCase
from unittest.mock import patch, MagicMock #maybe patch

from inventory_management.inventory_class import Inventory
from inventory_management.furniture_class import Furniture
from inventory_management.electric_appliances_class import ElectricAppliances

import inventory_management.main as main
import inventory_management.market_prices as market_prices

class FurnitureTests(TestCase):

    def test_furniture(self):
        f = Furniture('X55', 'Red couch', 120, 20, 'Cloth', 'XL')
        f_dict = f.return_as_dictionary()
        assert f_dict == {'product_code': 'X55',
                          'description': 'Red couch',
                          'market_price': 120,
                          'rental_price': 20,
                          'material': 'Cloth',
                          'size': 'XL'}

class ElectricAppliancesTests(TestCase):

    def test_electric_appliances(self):
        e = ElectricAppliances('D23', 'Circular Saw', 300, 25, 'Sawsly', '12V')
        e_dict = e.return_as_dictionary()
        assert e_dict == {'product_code': 'D23',
                          'description': 'Circular Saw',
                          'market_price': 300,
                          'rental_price': 25,
                          'brand': 'Sawsly',
                          'voltage': '12V'}

class InventoryTests(TestCase):

    def test_inventory(self):
        inv = Inventory('Y43', 'Screwdriver', 5, 1)
        inv_dict = inv.return_as_dictionary()
        assert inv_dict == {'product_code': 'Y43',
                          'description': 'Screwdriver',
                          'market_price': 5,
                          'rental_price': 1}

class MainTests(TestCase):

    def test_get_price(self):
        main.get_latest_price = MagicMock(return_value='FakePrice')
        price = main.get_price('X55')
        assert price == 'FakePrice'
        main.get_latest_price.assert_called()

    def test_exit(self):
        '''Tests that the code exits on a selection of 4'''
        with patch('sys.exit') as exit_mock:
            main.exit_program()
            assert exit_mock.called is True

    @patch('builtins.input', side_effect=['X72','Power Drill', 5, 'N', 'Y', 'Drillswell', '12V'])
    def test_add_new_item_electric(self, mock_input):
        main.get_latest_price = MagicMock(return_value='FakePrice')
        main.add_new_item()
        assert main.FULL_INVENTORY == {'X72': {'product_code': 'X72', 'description': 'Power Drill', 'market_price': 'FakePrice', 'rental_price': 5, 'brand': 'Drillswell', 'voltage': '12V'}}
        main.FULL_INVENTORY = {}

    @patch('builtins.input', side_effect=['C23','Blue Couch', 20, 'Y', 'Cloth', 'XL'])
    def test_add_new_item_furniture(self, mock_input):
        main.get_latest_price = MagicMock(return_value='FakePrice')
        main.add_new_item()
        assert main.FULL_INVENTORY == {'C23': {'product_code': 'C23', 'description': 'Blue Couch', 'market_price': 'FakePrice', 'rental_price': 20, 'material': 'Cloth', 'size': 'XL'}}
        main.FULL_INVENTORY = {}

    @patch('builtins.input', side_effect=['S99','Screwdriver', 2, 'N', 'N'])
    def test_add_new_item_generic(self, mock_input):
        main.get_latest_price = MagicMock(return_value='FakePrice')
        main.add_new_item()
        assert main.FULL_INVENTORY == {'S99': {'product_code': 'S99', 'description': 'Screwdriver', 'market_price': 'FakePrice', 'rental_price': 2}}
        main.FULL_INVENTORY = {}

    @patch('builtins.input', side_effect='1')
    def test_main_menu(self, mock_input):
        response = main.main_menu()
        assert response == main.add_new_item


    @patch('builtins.input', side_effect=['S99'])
    def test_item_info(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_output:
            main.FULL_INVENTORY = {'S99': {'product_code': 'S99', 'description': 'Screwdriver', 'market_price': 'FakePrice', 'rental_price': 2}}
            main.item_info()
            assert fake_output.getvalue().strip() == "product_code:S99\ndescription:Screwdriver\nmarket_price:FakePrice\nrental_price:2"
            main.FULL_INVENTORY = {}

    @patch('builtins.input', side_effect='S99')
    def test_item_info_not_found(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_output:
            main.item_info()
            assert fake_output.getvalue().strip() == "Item not found in inventory"
            main.FULL_INVENTORY = {}

class MarketPrices(TestCase):

    def test_market_prices(self):
        price = market_prices.get_latest_price('X72')
        assert price == 24

