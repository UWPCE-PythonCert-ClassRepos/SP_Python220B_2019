# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 14:52:01 2019

@author: Laura.Fiorentino
"""

from unittest import TestCase
from unittest.mock import MagicMock

from furniture import Furniture
from inventory import Inventory
from electricappliances import ElectricAppliances


class FurnitureTests(TestCase):

    def test_furniture(self):
        new_item = Furniture('code', 'description', 'm_price', 'r_price',
                             'material', 'size')
        self.assertEqual('description', new_item.description)
        self.assertEqual('code', new_item.product_code)
        self.assertEqual('m_price', new_item.market_price)
        self.assertEqual('r_price', new_item.rental_price)
        self.assertEqual('material', new_item.material)
        self.assertEqual('size', new_item.size)


class InventoryTests(TestCase):
    def test_inventory(self):
        new_item = Inventory('code', 'description', 'm_price', 'r_price')
        self.assertEqual('description', new_item.description)
        self.assertEqual('code', new_item.product_code)
        self.assertEqual('m_price', new_item.market_price)
        self.assertEqual('r_price', new_item.rental_price)


class ElectricApplicancesTests(TestCase):
    def test_electricappliances(self):
        new_item = ElectricAppliances('code', 'description', 'm_price',
                                      'r_price', 'brand', 'voltage')
        self.assertEqual('description', new_item.description)
        self.assertEqual('code', new_item.product_code)
        self.assertEqual('m_price', new_item.market_price)
        self.assertEqual('r_price', new_item.rental_price)
        self.assertEqual('brand', new_item.brand)
        self.assertEqual('voltage', new_item.voltage)
