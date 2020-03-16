"""
Tests integration of Inventory Management.
"""
import sys
sys.path.append('inventory_management')
# Test libs
from unittest import TestCase
from unittest.mock import patch, MagicMock
# Import modules
from inventory_management.inventory_class import Inventory
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
import inventory_management.market_prices as market_prices
import inventory_management.main as main

class InventoryManagementIntegration(TestCase):
    """Class to test function of Inventory Management as a whole."""
    
    def test_integration_im(self):
        """Tests integration across modules."""
        
        # Prep test cases for each type of new item
        inv_1 = ['2203', 'speaker', 225, 'n', 'n']
        furn_1 = ['0682', 'chair', 85, 'y', 'leather', '54 x 42']
        ea_1 = ['1547', 'monitor', 210, 'N', 'Y', 'Acer', 200]

        # Expected dicts for each item
        inv_dict = {'product_code': '2203',
                    'description': 'speaker',
                    'market_price': 500,
                    'rental_price': 225}
                    

        ea_dict = {'product_code': '1547',
                   'description': 'monitor',
                   'market_price': 400,
                   'rental_price': 210,
                   'brand': 'Acer',
                   'voltage': 200}
                   

        furn_dict = {'product_code': '0682',
                     'description': 'chair',
                     'market_price': 150,
                     'rental_price': 85,
                     'material': 'leather',
                     'size': '54 x 42'}
                     
        # Main inventory
        main.FULL_INVENTORY = {}

        #Add items to inventory
        with patch('builtins.input', side_effect=inv_1):
                with patch('market_prices.get_latest_price', return_value=500):
                    main.add_new_item()
        with patch('builtins.input', side_effect=ea_1):
                with patch('market_prices.get_latest_price', return_value=400):
                    main.add_new_item()
        with patch('builtins.input', side_effect=furn_1):
                with patch('market_prices.get_latest_price', return_value=150):
                    main.add_new_item()
        print(main.FULL_INVENTORY)

        # Compare output
        expected = {}
        expected['2203'] = inv_dict
        expected['1547'] = ea_dict
        expected['0682'] = furn_dict
        print(expected)
        self.assertEqual(main.FULL_INVENTORY, expected)
                  
    def test_item_info(self): # Test item info lookup
        
        inv_info = {'product_code': '2203',
                    'description': 'speaker',
                    'market_price': 500,
                    'rental_price': 225}

        # Compare info lookup vs expected
        with patch('builtins.input', side_effect=['2203']):
            self.assertEqual(main.item_info(), print(inv_info))

    def test_exit_program(self):
        """Tests functionality program will close."""
        with self.assertRaises(SystemExit):
            main.exit_program()
