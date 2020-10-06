#!/usr/env/bin python
""" Documentation for Test integration """

import os
from unittest import TestCase
from inventory import add_furniture, single_customer


class InventoryIntegrationTest(TestCase):
    """Full test of inventory.py"""

    def __init__(self, *args, **kwargs):
        super(InventoryIntegrationTest, self).__init__(*args, **kwargs)
        self.rented = "rented_items.csv" + "_tmp"
        self.test = "test_items.csv"

    def test_system(self):
        """Full test procedure outlined in assignment"""
        add_furniture(self.rented, "Elisa Miles", "LR04", "Leather Sofa", 25)
        add_furniture(self.rented, "Edward Data", "KT78", "Kitchen Table", 10)
        add_furniture(self.rented, "Alex Gonzales", "BR02", "Queen Mattress", 17)
        create_invoice = single_customer("Susan Wong", self.rented)
        create_invoice(self.test)

        expected = "Elisa Miles,LR04,Leather Sofa,25.00\n" \
                   "Edward Data,KT78,Kitchen Table,10.00\n" \
                   "Alex Gonzales,BR02,Queen Mattress,17.00\n" \
                   "Susan Wong,LR04,Leather Sofa,25.00\n" \
                   "Susan Wong,KT78,Kitchen Table,10.00\n" \
                   "Susan Wong,BR02,Queen Mattress,17.00\n" \

        self.assertEqual(first=open(self.rented, 'r').read(),
                         second=expected)

        # clean up tmp file
        self.addCleanup(os.remove, self.rented)
        self.doCleanups()
