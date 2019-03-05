# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 14:52:01 2019

@author: Laura.Fiorentino
"""

from unittest import TestCase
from unittest.mock import MagicMock

from main.furniture import Furniture
from main.inventory import Inventory


class FurnitureTests(TestCase):

    def test_adding(self):
        adder = Adder()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i + j, adder.calc(i, j))


class InventoryTests(TestCase):

    def test_subtracting(self):
        subtracter = Subtracter()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i - j, subtracter.calc(i, j))

