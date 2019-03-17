# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 18:27:33 2019

@author: Laura.Fiorentino
"""
from unittest import TestCase
from unittest.mock import MagicMock, patch

from inventory_management.furniture import Furniture
from inventory_management.inventory import Inventory
from inventory_management.electricappliances import ElectricAppliances
from inventory_management.main import main_menu
from inventory_management.main import get_price
from inventory_management.main import add_new_item
from inventory_management.main import item_info
from inventory_management.main import exit_program
from inventory_management.market_prices import get_latest_price

class ModuleTests(TestCase):
    def test_furniture(self):
        furniture_input = ['100', 'description', 'rentalprice', 'y',
                           'material', 'size']
        with patch('builtins.input', side_effect=furniture_input):
            add_new_item()

    def test_electric(self):
        electric_input = ['200', 'description', 'rentalprice', 'n', 'y',
                          'brand', 'voltage']
        with patch('builtins.input', side_effect=electric_input):
            add_new_item()
