#!/usr/bin/env python3
"""
Unit tests for basic_operations
"""
import unittest
from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch
from customer_schema import Customer
from functools import wraps
import peewee


test_db = peewee.SqliteDatabase(':memory:')


# Bind the given models to the db for the duration of wrapped block.
def use_test_database(fn):
    @wraps(fn)
    def inner(self):
        with test_db.bind_ctx([Customer]):
            test_db.create_tables([Customer])
            try:
                fn(self)
            finally:
                test_db.drop_tables([Customer])
    return inner


class BasicOperationsTest(TestCase):
    @use_test_database
    def test_add_customer(self):
        from basic_operations import add_customer
        test_user = {'customer_id': '1255', 'name': 'Tim', 'lastname': 'Allen',
                     'home_address': "15402 W 8 Mile Rd, Detroit, MI 48219",
                     'phone_number': '5558468665', 'email_address': 'TimToolManTaylor@ToolTime.com',
                     'status': True, 'credit_limit': 10000.00}
        add_customer(**test_user)
        # add_customer(**test_user)
        db_query = Customer.get_by_id('1255')
        self.assertEqual(db_query.name, test_user['name'])
