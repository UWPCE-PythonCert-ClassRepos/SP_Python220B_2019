#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 13:40:32 2019

@author: lauraannf
"""

from unittest import TestCase
from database import import_data
from pymongo import MongoClient


class TestDatabase(TestCase):
    
    def test_import_data(self):
        import_data('csvs', 'product_csv.csv', 'customer_csv.csv',
                   'rental_csv.csv')