import sys
from io import StringIO
from unittest import TestCase
from unittest.mock import patch, MagicMock

from inventory_management.inventory_class import Inventory
from inventory_management.furniture_class import Furniture
from inventory_management.electric_appliances_class import ElectricAppliances

import inventory_management.main as main
import inventory_management.market_prices as market_prices

side_effect_list = ['X72','Power Drill', 5, 'N', 'Y', 'Drillswell', '12V', #Electric item
                    'C23','Blue Couch', 20, 'Y', 'Cloth', 'XL',            #Furniture item
                    'S99','Screwdriver', 2, 'N', 'N',                      #Non-electric, non-furniture item
                    'S99']                                                 #Item Search - S99

inventory_elec = {'X72': {'product_code': 'X72', 'description': 'Power Drill', 'market_price': 'FakePrice',
                  'rental_price': 5, 'brand': 'Drillswell', 'voltage': '12V'}}

inventory_elec_furn = {'X72': {'product_code': 'X72', 'description': 'Power Drill', 'market_price': 'FakePrice',
                       'rental_price': 5, 'brand': 'Drillswell', 'voltage': '12V'}, 
                       'C23': {'product_code': 'C23', 'description': 'Blue Couch', 'market_price': 'FakePrice',
                       'rental_price': 20, 'material': 'Cloth', 'size': 'XL'}}

inventory_elec_furn_gen = {'X72': {'product_code': 'X72', 'description': 'Power Drill', 'market_price': 'FakePrice',
                           'rental_price': 5, 'brand': 'Drillswell', 'voltage': '12V'}, 
                           'C23': {'product_code': 'C23', 'description': 'Blue Couch', 'market_price': 'FakePrice',
                           'rental_price': 20, 'material': 'Cloth', 'size': 'XL'},
                           'S99': {'product_code': 'S99', 'description': 'Screwdriver', 'market_price': 'FakePrice',
                           'rental_price': 2}}

stdout_statement = ("New inventory item added\nNew inventory item added\nNew inventory item added\n" +
                    "product_code:S99\ndescription:Screwdriver\nmarket_price:FakePrice\nrental_price:2")

class IntergrationTests(TestCase):

    @patch('builtins.input', side_effect=side_effect_list)
    def test_multi_creation_lookup(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_output:
            main.get_latest_price = MagicMock(return_value='FakePrice')
            main.add_new_item()
            assert main.FULL_INVENTORY == inventory_elec
            main.add_new_item()
            assert main.FULL_INVENTORY == inventory_elec_furn
            main.add_new_item()
            assert main.FULL_INVENTORY == inventory_elec_furn_gen
            main.item_info()
            assert fake_output.getvalue().strip() == stdout_statement
            main.FULL_INVENTORY = {}
