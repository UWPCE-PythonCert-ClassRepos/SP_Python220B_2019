# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 12:49:08 2019

@author: Laura.Fiorentino
"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from inventory_management.furniture import Furniture
from inventory_management.inventory import Inventory
from inventory_management.electricappliances import ElectricAppliances
from inventory_management.main import main_menu as main_menu
from inventory_management.main import get_price as get_price, \
    add_new_item as add_new_item, item_info as item_info, \
    exit_program as exit_program


class ModuleTests(TestCase):

    def test_module(self):
        Furniture('100', 'description', 'rentalprice', 'y', 'material', 'size')
        ElectricAppliances('200', 'description', 'rentalprice', 'n', 'y',
                           'brand', 'voltage')
        Inventory('300', 'description', 'rentalprice', 'n', 'n')