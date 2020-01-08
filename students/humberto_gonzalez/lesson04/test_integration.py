# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 13:20:17 2019

@author: Humberto
"""

from unittest import TestCase
from assignment.customer_model import DATABASE as database
from assignment.customer_model import Customer
from assignment.basic_operations import add_customer
from assignment.basic_operations import delete_customer
from assignment.basic_operations import list_active_customers

class TestIntegration(TestCase):
    """test for the integration of the code as a whole"""
    def setUp(self):
        """sets up the tests"""
        database.create_tables([Customer])

    def tearDown(self):
        """Remves tables created by tests"""
        database.drop_tables([Customer])

    def test_integration(self):
        """tests the integration of the functions"""
        added_customer_1 = {'customer_id':'LUX65',
                            'first_name':'Lucifer',
                            'last_name':'Morningstar',
                            'home_address':'4578 Main Street',
                            'phone_number':'6197602022',
                            'email_address':'lucy@yahoo.com',
                            'status':'Active',
                            'credit_limit':12000.00}
        add_customer(**added_customer_1)
        added_customer_2 = {'customer_id':'JJ77',
                            'first_name':'Jax',
                            'last_name':'Linx',
                            'home_address':'333 Acorn Avenue',
                            'phone_number':'4257602145',
                            'email_address':'Loud@yahoo.com',
                            'status':'Active',
                            'credit_limit':17000.00}
        add_customer(**added_customer_2)
        added_customer_3 = {'customer_id':'JKL456',
                            'first_name':'Luke',
                            'last_name':'Josety',
                            'home_address':'1547 Acorn Avenue',
                            'phone_number':'7477371916',
                            'email_address':'Luke@gamil.com',
                            'status':'Inactive',
                            'credit_limit':1000.00}
        add_customer(**added_customer_3)
        delete_customer(added_customer_2['customer_id'])
        result = list_active_customers()
        self.assertEqual(result, 1)
             