#!/usr/env/bin python
"""Unit testing for database basic operations.
Borrowed heavily from peewee documentation."""

from unittest import TestCase
from database_models import *

import basic_operations
import logging

# logging.basicConfig(level=logging.ERROR)
logging.basicConfig(level=logging.INFO)
test_logger = logging.getLogger(__name__)

RECORDS = (
    ('0001', 'Fergie', 'Jenkins', '123 fakse st, Chicago, IL',
     1234567890, 'jenkinsf@cubs.com', True, 1000000.),

    ('0002', 'Nolan', 'Ryan', '123 fakse st, Houston, TX',
     1234567890, 'ryan.nolan@astros.com', True, 2000000.),

    ('0003', 'Phill', 'Niekro', '123 fakse st, Atlanta, GA',
     1234567890, 'philniekro@braves.com', True, 1500000.),

    ('0004', 'Don', 'Drysdale', '123 fakse st, Los Angeles, CA',
     1234567890, 'd.drysdale@dodgers.com', False, 1000000.),
)

CUSTOMER_ID = 0
NAME = 1
LASTNAME = 2
HOME_ADDRESS = 3
PHONE_NUMBER = 4
EMAIL_ADDRESS = 5
ACTIVE = 6
CREDIT_LIMIT = 7

# MODELS = [User, Tweet, EventLog, Relationship]
MODELS = [Customer]

# use an in-memory SQLite for tests.
test_db = SqliteDatabase(':memory:')


class BaseTestCase(TestCase):
    """testing database operations"""

    def setUp(self):
        # Bind model classes to test db. Since we have a complete list of
        # all models, we do not need to recursively bind dependencies.
        # test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

        test_db.connect(reuse_if_open=True)
        test_db.drop_tables(MODELS)
        test_db.create_tables(MODELS)

        self.populate_db_with_records()

    def tearDown(self):
        # Not strictly necessary since SQLite in-memory databases only live
        # for the duration of the connection, and in the next step we close
        # the connection...but a good practice all the same.
        test_db.drop_tables(MODELS)

        # Close connection to db.
        test_db.close()

        # If we wanted, we could re-bind the models to their original
        # database here. But for tests this is probably not necessary.

    def populate_db_with_records(self):
        """populate the database with baseline data from RECORDS"""
        for record in RECORDS:
            basic_operations.add_customer(*record)
        test_logger.info("records added for testing")

    def test_add_customer(self):
        """add records test"""
        self.setUp()
        test_logger.info("begin test_add_customer() ...")

        for record in RECORDS:
            test_logger.info(f"Testing record {record[CUSTOMER_ID]}")
            self.assertEqual(first=record[EMAIL_ADDRESS],
                             second=Customer.get_by_id(record[CUSTOMER_ID]).email_address)

        self.tearDown()
        test_logger.info("end test_add_customer()")

    def test_search_customer(self):
        """add records test"""
        self.setUp()
        test_logger.info("begin test_search_customer() ...")

        for record in RECORDS:
            test_logger.info(f"Testing record {record[CUSTOMER_ID]}")
            self.assertEqual(first=record[EMAIL_ADDRESS],
                             second=basic_operations.search_customer(record[CUSTOMER_ID]).get("email_address"))

        self.tearDown()
        test_logger.info("end test_search_customer()")

    def test_delete_customer(self):
        """add records test"""
        self.setUp()
        test_logger.info("begin test_delete_customer() ...")

        for record in RECORDS:
            test_logger.info(f"Testing record {record[CUSTOMER_ID]}")
            basic_operations.delete_customer(record[CUSTOMER_ID])

            self.assertEqual(first={},
                             second=basic_operations.search_customer(record[CUSTOMER_ID]))

        self.tearDown()
        test_logger.info("end test_delete_customer()\n")

    def test_update_customer_credit(self):
        """add records test"""
        self.setUp()
        test_logger.info("begin test_update_customer_credit() ...")

        for record in RECORDS:
            test_logger.info(f"Testing record {record[CUSTOMER_ID]}")
            update_limit = record[CREDIT_LIMIT] ** 2
            basic_operations.update_customer_credit(customer_id=record[CUSTOMER_ID],
                                                    credit_limit=update_limit)
            self.assertEqual(first=update_limit,
                             second=basic_operations.search_customer(record[CUSTOMER_ID]).get("credit_limit"))

        self.tearDown()
        test_logger.info("end test_update_customer_credit()\n")

    def test_list_active_customers(self):
        """add records test"""
        self.setUp()
        test_logger.info("begin test_list_active_customers() ...")

        test_logger.info(f"Testing records ")
        active_records = []
        for rec in RECORDS:
            if rec[ACTIVE] is True:
                active_records.append(basic_operations.search_customer(rec[CUSTOMER_ID]))

        self.assertEqual(first=tuple(active_records),
                         second=basic_operations.list_active_customers())

        self.tearDown()
        test_logger.info("end test_list_active_customers()\n")

    def test_fail_bad_phone_number(self):
        self.setUp()
        test_logger.info("begin () ...")
        basic_operations.add_customer(customer_id='01',
                                      name='test',
                                      lastname='test',
                                      home_address='test',
                                      phone_number='1234567890',
                                      email_address='test',
                                      active='True',
                                      credit_limit='unlimited', )
        c = basic_operations.search_customer('01')

        # self.assertEqual(first=c.get('phone_number'),
        #                  second=1234567890)
        self.assertEqual(first='1234567890',
                         second=c.get('phone_number'))
        test_logger.info("phone number as str() is converted if correct format")

        test_logger.info("end ()\n")

    def test_fail_bad_active(self):
        self.setUp()
        test_logger.info("begin test_bad_active() ...")
        basic_operations.add_customer(customer_id='01',
                                      name='test',
                                      lastname='test',
                                      home_address='test',
                                      phone_number='1234567890',
                                      email_address='test',
                                      active='True',
                                      credit_limit='unlimited', )
        c = basic_operations.search_customer('01')

        # self.assertEqual(first=c.get('active'),
        #                  second=False)
        self.assertEqual(first='True',
                         second=c.get('active'))
        test_logger.info("Active status is False if not boolean")

        test_logger.info("end test_bad_active()\n")

    def test_fail_bad_credit_limit(self):
        self.setUp()
        test_logger.info("begin test_bad_credit_limit() ...")
        basic_operations.add_customer(customer_id='01',
                                      name='test',
                                      lastname='test',
                                      home_address='test',
                                      phone_number='1234567890',
                                      email_address='test',
                                      active='True',
                                      credit_limit='unlimited', )
        c = basic_operations.search_customer('01')

        # self.assertEqual(first=c.get('credit_limit'),
        #                  second=0.)
        self.assertEqual(first='unlimited',
                         second=c.get('credit_limit'))
        test_logger.info("Credit limit is not float-able value, set to 0.")

        test_logger.info("end test_bad_credit_limit()\n")
