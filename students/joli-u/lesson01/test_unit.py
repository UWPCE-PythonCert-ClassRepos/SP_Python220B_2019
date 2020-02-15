"""
test_unit.py
joli umetsu
py220
"""

from unittest import TestCase
from unittest.mock import patch, MagicMock
import sys

from inventory_management.inventory_class import Inventory
from inventory_management.furniture_class import Furniture
from inventory_management.electric_appliances_class import ElectricAppliances
import inventory_management.market_prices as market_prices
import inventory_management.main as main


class TestInventory(TestCase):
    """ tests modules in inventory_class.py """
    
    def setUp(self):
        self.product_code = 199021
        self.description = 'na'
        self.market_price = 100
        self.rental_price = 500
        
        self.check_inventory = Inventory(self.product_code, self.description,
                                         self.market_price, self.rental_price)

    def test_init(self):
        """ check initialization of variables """
        self.assertEqual(self.check_inventory.product_code, self.product_code)
        self.assertEqual(self.check_inventory.description, self.description)
        self.assertEqual(self.check_inventory.market_price, self.market_price)
        self.assertEqual(self.check_inventory.rental_price, self.rental_price)
        
    def test_return_as_dict(self):
        """ check dictionary output """
        dict_output = self.check_inventory.return_as_dict()
        
        self.assertEqual(dict_output['product_code'], self.product_code)
        self.assertEqual(dict_output['description'], self.description)
        self.assertEqual(dict_output['market_price'], self.market_price)
        self.assertEqual(dict_output['rental_price'], self.rental_price)

        
class TestFurniture(TestCase):
    """ tests modules in furniture_class.py """
    
    def setUp(self):
        self.product_code = 199021
        self.description = 'na'
        self.market_price = 100
        self.rental_price = 500
        self.material = 'gold'
        self.size = 'm'
        
        self.check_furniture = Furniture(self.product_code, self.description,
                                         self.market_price, self.rental_price,
                                         self.material, self.size)

    def test_init(self):
        """ check initialization of variables """
        self.assertEqual(self.check_furniture.product_code, self.product_code)
        self.assertEqual(self.check_furniture.description, self.description)
        self.assertEqual(self.check_furniture.market_price, self.market_price)
        self.assertEqual(self.check_furniture.rental_price, self.rental_price)
        self.assertEqual(self.check_furniture.material, self.material)
        self.assertEqual(self.check_furniture.size, self.size)
        
    def test_return_as_dict(self):
        """ check dictionary output """
        dict_output = self.check_furniture.return_as_dict()
        
        self.assertEqual(dict_output['product_code'], self.product_code)
        self.assertEqual(dict_output['description'], self.description)
        self.assertEqual(dict_output['market_price'], self.market_price)
        self.assertEqual(dict_output['rental_price'], self.rental_price)
        self.assertEqual(dict_output['material'], self.material)
        self.assertEqual(dict_output['size'], self.size)
        
        
class TestElectricAppliances(TestCase):
    """ tests modules in electric_appliances_class.py """
    
    def setUp(self):
        self.product_code = 199021
        self.description = 'na'
        self.market_price = 100
        self.rental_price = 500
        self.brand = 'ge'
        self.voltage = 120
        
        self.check_electric = ElectricAppliances(self.product_code, self.description,
                                                 self.market_price, self.rental_price,
                                                 self.brand, self.voltage)

    def test_init(self):
        """ check initialization of variables """
        self.assertEqual(self.check_electric.product_code, self.product_code)
        self.assertEqual(self.check_electric.description, self.description)
        self.assertEqual(self.check_electric.market_price, self.market_price)
        self.assertEqual(self.check_electric.rental_price, self.rental_price)
        self.assertEqual(self.check_electric.brand, self.brand)
        self.assertEqual(self.check_electric.voltage, self.voltage)
        
    def test_return_as_dict(self):
        """ check dictionary output """
        dict_output = self.check_electric.return_as_dict()
        
        self.assertEqual(dict_output['product_code'], self.product_code)
        self.assertEqual(dict_output['description'], self.description)
        self.assertEqual(dict_output['market_price'], self.market_price)
        self.assertEqual(dict_output['rental_price'], self.rental_price)
        self.assertEqual(dict_output['brand'], self.brand)
        self.assertEqual(dict_output['voltage'], self.voltage)
        
        
class TestMarketPrices(TestCase):
    """ tests modules in market_prices.py """
    
    def test_get_latest_price(self):
        """ check latest price is 24 """     
        for each in (None, 1, 'test'):
            self.assertEqual(market_prices.get_latest_price(each), 24)
            
            
class TestMain(TestCase):
    """ tests modules in main.py """
    
    def test_main_menu(self):
        """ checks the correct menu selections are returned """
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = '1'
            self.assertEqual(main.main_menu(), main.add_new_item)
        
            mock_input.side_effect = '2'
            self.assertEqual(main.main_menu(), main.item_info)
        
            mock_input.side_effect = 'q'
            self.assertEqual(main.main_menu(), main.exit_program)
        
    def test_get_price(self):
        """ check the correct price is returned """
        for each in (None, 1, 'test'):
            self.assertEqual(main.get_price(each), 24)
    
    def test_add_new_item(self):
        """ checks that items are added to dict correctly """
        check_dict = {}
        
        with patch('builtins.input') as mock_input:
        
            # check adding of furniture item 
            mock_input.side_effect = ['199021', 'desk', '800', 'y', 'gold', 'm']
            main.add_new_item()
            
            check_dict['199021'] = {'product_code': '199021', 
                                    'description': 'desk',
                                    'market_price': 24,
                                    'rental_price': '800',
                                    'material': 'gold',
                                    'size': 'm'}
            self.assertEqual(main.FULL_INVENTORY, check_dict)                       
            self.assertIn('199021', main.FULL_INVENTORY)     
        
            # check adding of electrical item         
            mock_input.side_effect = ['532112', 'dryer', '600', 'n', 'y', 'ge', '120']
            main.add_new_item()
            
            check_dict['532112'] = {'product_code': '532112', 
                                    'description': 'dryer',
                                    'market_price': 24,
                                    'rental_price': '600',
                                    'brand': 'ge',
                                    'voltage': '120'}

            self.assertEqual(main.FULL_INVENTORY, check_dict)
            self.assertIn('532112', main.FULL_INVENTORY)
            self.assertIn('199021', main.FULL_INVENTORY)

            # check adding of inventory item
            mock_input.side_effect = ['243354', 'stuff', '10', 'n', 'n']
            main.add_new_item()
            
            check_dict['243354'] = {'product_code': '243354', 
                                    'description': 'stuff',
                                    'market_price': 24,
                                    'rental_price': '10'}

            self.assertEqual(main.FULL_INVENTORY, check_dict)
            self.assertIn('243354', main.FULL_INVENTORY)
            self.assertIn('199021', main.FULL_INVENTORY)
        
        
    @patch('builtins.input')
    def test_item_info(self, mock_input):
        """  checks item info printed """
        main.FULL_INVENTORY = {'199021': {'product_code': '199021', 
                                          'description': 'desk',
                                          'market_price': 24,
                                          'rental_price': '800',
                                          'material': 'gold',
                                          'size': 'm'}}
        # check for an item that does exist 
        check_output = "product_code:199021\ndescription:desk\nmarket_price:24,rental_price:800\nmaterial:gold\nsize:m"
        mock_input.return_value = '199021'
        self.assertEqual(main.item_info(), print(check_output))
        
        # check for an item that doesn't exist 
        check_output = "Item not found in inventory"
        mock_input.return_value = '34'
        self.assertEqual(main.item_info(), print(check_output))
        
        
    def test_exit_program(self):
        """ checks system exit """
        sys.exit = MagicMock()
        main.exit_program()
        
        sys.exit.assert_called()