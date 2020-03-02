#!/usr/bin/env python
"""
Integration test module.

Initiates the program from main_menu, and mocks key sequences to:

- create an inventory item
- create a furniture item
- create an electric appliances item
- show info for the inventory item
- show info for the furniture item
- show info for the electric appliances item
- query for a nonexistem item code

Checks to see if final data structure is correct.

Checks to see if text output is correct.
"""

from unittest import TestCase
from unittest.mock import patch
from io import StringIO
import os
import sys

os.chdir('inventory_management/')
sys.path.append(os.getcwd())

from main import *

INV_CDE = '123456'
INV_DSC = 'thing'
INV_RNT_PRC = '30'
FUR_CDE = '456789'
FUR_DSC = 'couch'
FUR_RNT_PRC = '20'
FUR_MAT = 'leather'
FUR_SZ = 'L'
EA_CDE = '789123'
EA_DSC = 'tv'
EA_RNT_PRC = '10'
EA_BRD = 'Samsung'
EA_VLT = '110'

key_seq = ['1', INV_CDE, INV_DSC, INV_RNT_PRC, 'N', 'N', '1', FUR_CDE, FUR_DSC, FUR_RNT_PRC, 'Y',
           FUR_MAT, FUR_SZ, '1', EA_CDE, EA_DSC, EA_RNT_PRC, 'N', 'Y', EA_BRD, EA_VLT, '2',
           INV_CDE, '2', FUR_CDE, '2', '888']

main_menu_passes = key_seq.count('1') + key_seq.count('2')
# number of passes through main_menu is countable by number of '1' or '2' entries


class IntegrationTest(TestCase):

    def setUp(self):
        self.maxDiff = None

    @patch('sys.stdout', new_callable=StringIO)
    def test_main(self, mock_stdout):
        with patch('builtins.input', side_effect=key_seq):
            for i in range(main_menu_passes):
                main_menu()()
            self.assertEqual(FULL_INVENTORY, {INV_CDE: {'product_code': INV_CDE,
                             'description': INV_DSC, 'market_price': 24,
                             'rental_price': INV_RNT_PRC}, FUR_CDE: {'product_code': FUR_CDE,
                             'description': FUR_DSC, 'market_price': 24,
                             'rental_price': FUR_RNT_PRC, 'material': FUR_MAT, 'size': FUR_SZ},
                             EA_CDE: {'product_code': EA_CDE, 'description': EA_DSC,
                             'market_price': 24, 'rental_price': EA_RNT_PRC, 'brand': EA_BRD,
                             'voltage': EA_VLT}})
            self.assertEqual(mock_stdout.getvalue(), """Please choose from the following options (1, 2, q):
1. Add a new item to the inventory
2. Get item information
q. Quit
New inventory item added
Please choose from the following options (1, 2, q):
1. Add a new item to the inventory
2. Get item information
q. Quit
New inventory item added
Please choose from the following options (1, 2, q):
1. Add a new item to the inventory
2. Get item information
q. Quit
New inventory item added
Please choose from the following options (1, 2, q):
1. Add a new item to the inventory
2. Get item information
q. Quit
product_code:123456
description:thing
market_price:24
rental_price:30
Please choose from the following options (1, 2, q):
1. Add a new item to the inventory
2. Get item information
q. Quit
product_code:456789
description:couch
market_price:24
rental_price:20
material:leather
size:L
Please choose from the following options (1, 2, q):
1. Add a new item to the inventory
2. Get item information
q. Quit
Item not found in inventory
""")
