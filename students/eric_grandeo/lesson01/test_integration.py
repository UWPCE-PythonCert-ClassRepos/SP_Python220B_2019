from unittest import TestCase
from unittest.mock import patch
import sys
sys.path.append('./inventory_management')
import inventory_management.main as main

class IntegrationTests(TestCase):
    
    def test_main(self):
        main.FULL_INVENTORY = {}
        
        expected = {'123': {'product_code': '123',
                      'description': 'table',
                      'market_price': 24,
                      'rental_price': '456',
                      'material': 'wood',
                      'size': 'm'}, 
                    '321':{'product_code': '321',
                      'description': 'blender',
                      'market_price': 24,
                      'rental_price': '456',
                      'brand': 'samsung',
                      'voltage': '120'}}
        
        elec_inputs = ['321', 'blender', '456', 'n', 'y', 'samsung', '120']
        furn_inputs = ['123', 'table', '456', 'y', 'wood', 'm']
        
        with patch('builtins.input', side_effect=furn_inputs):
            main.add_new_item()
         
        with patch('builtins.input', side_effect=elec_inputs):
            main.add_new_item()    
            
        self.assertEqual(main.FULL_INVENTORY, expected)

