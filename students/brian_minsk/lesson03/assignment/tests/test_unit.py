""" Unit tests for the lesson03 assignment.

Note: 'DATABASE' is a global from basic_operations that refers to the sqlite
database.
"""

# pylint: disable=unused-wildcard-import
# pylint: disable=wrong-import-position

import sys
sys.path.append('C:\\Users\\brian\\PythonClass\\PY220\\SP_Python220B_2019\\'
                '\\students\\brian_minsk\\lesson03\\assignment')
from unittest import TestCase
import logging
from peewee import *  # pylint: disable=wildcard-import
from basic_operations import *  # pylint: disable=wildcard-import

logging.basicConfig(level=logging.ERROR)
LOGGER = logging.getLogger(__name__)

# Sample customer data
CUSTOMERS = {"beat_choonz": {"customer_id": 1,
                             "first_name": "Beat",
                             "last_name": "Choonz",
                             "address": "123 Main Street, Anywhere, NY 12345",
                             "phone": "123.456.7890",
                             "email_address": "beat.choonz@gmail.com",
                             "status": True,
                             "credit_limit": 10000.00},
             "shady_flava": {"customer_id": 2,
                             "first_name": "Shady",
                             "last_name": "Flava",
                             "address": "987 Elm Street, Elsewhere, CA 09876",
                             "phone": "999.888.7777",
                             "email_address": "shady.flava@gmail.com",
                             "status": True,
                             "credit_limit": 8000.00},
             "vegeta_colt": {"customer_id": 3,
                             "first_name": "Vegeta",
                             "last_name": "Colt",
                             "address": "5554 Oak Lane, Nowhere, ND, 50000",
                             "phone": "555.444.6666",
                             "email_address": "vegeta.colt@gmail.com",
                             "status": False,
                             "credit_limit": 5000.00}}


class PrePopulatedTests(TestCase):
    """ Tests run before data is added to the db.
    """
    def setUp(self):
        """ Create the Customer table.
        """
        create_tables()

    def tearDown(self):
        """ Delete the Customer table.
        """
        delete_customer_table()

    def test_create_customer_model(self):
        """ Create a customer model.
        """
        LOGGER.info("test_create_customer_model")
        customer_model = Customer()
        self.assertIsInstance(customer_model, BaseModel)
        self.assertIsInstance(customer_model, Model)

        # Test that it has all the attributes it is supposed to have
        self.assertTrue(hasattr(customer_model, "customer_id"))
        self.assertTrue(hasattr(customer_model, "first_name"))
        self.assertTrue(hasattr(customer_model, "last_name"))
        self.assertTrue(hasattr(customer_model, "home_address"))
        self.assertTrue(hasattr(customer_model, "phone_number"))
        self.assertTrue(hasattr(customer_model, "email_address"))
        self.assertTrue(hasattr(customer_model, "status"))
        self.assertTrue(hasattr(customer_model, "credit_limit"))

    def test_create_customer_table(self):
        """ Add a Customer model to the db and verify that the db has the associated table.
        """
        LOGGER.info("test_create_customer_table")

        create_tables()

        DATABASE.connect()
        self.assertTrue(Customer.table_exists())
        DATABASE.close()

    def test_add_customer_to_db(self):
        """ Add data to the table and test to make sure it actually got in the db by querying it.
        """
        LOGGER.info("test_add_customer_to_db")

        beat_choonz = CUSTOMERS["beat_choonz"]

        add_customer(customer_id=beat_choonz["customer_id"],
                     name=beat_choonz["first_name"],
                     lastname=beat_choonz["last_name"],
                     home_address=beat_choonz["address"],
                     phone_number=beat_choonz["phone"],
                     email_address=beat_choonz["email_address"],
                     status=beat_choonz["status"],
                     credit_limit=beat_choonz["credit_limit"])

        acustomer = Customer.get(Customer.customer_id == beat_choonz["customer_id"])

        self.assertEqual(acustomer.customer_id, beat_choonz["customer_id"])
        self.assertEqual(acustomer.email_address, beat_choonz["email_address"])
        self.assertEqual(acustomer.first_name, beat_choonz["first_name"])
        self.assertEqual(acustomer.last_name, beat_choonz["last_name"])
        self.assertEqual(acustomer.home_address, beat_choonz["address"])
        self.assertEqual(acustomer.phone_number, beat_choonz["phone"])
        self.assertEqual(acustomer.status, beat_choonz["status"])
        self.assertEqual(acustomer.credit_limit, beat_choonz["credit_limit"])


class PostPopulatedTest(TestCase):
    """ Tests run after data sample is added to the db.
    """
    def setUp(self):
        """ Add a customer model, then add sample data to the db.
        """
        LOGGER.info('in TestCase:setUp')

        create_tables()
        LOGGER.info('Created the tables')
        add_customers(CUSTOMERS)
        LOGGER.info('Added the customers')

    def tearDown(self):
        """ Delete the Customer table.
        """
        delete_customer_table()

    def test_search_customer(self):
        """ Search for a customer in the database by customer_id.
        """
        LOGGER.info("test_search_customer")

        shady_flava = CUSTOMERS["shady_flava"]
        acustomer = search_customer(shady_flava["customer_id"])

        # Test that the values are the same for one of the rows.

        self.assertEqual(acustomer["name"], shady_flava["first_name"])
        self.assertEqual(acustomer["last_name"], shady_flava["last_name"])
        self.assertEqual(acustomer["phone_number"], shady_flava["phone"])
        self.assertEqual(acustomer["email_address"], shady_flava["email_address"])

    def test_search_customer_not_found(self):
        """ Test for empty dict if no customer found.
        """
        LOGGER.info("test_search_customer_not_found")
        acustomer = search_customer(4)

        self.assertDictEqual(acustomer, {})

    def test_delete_customer(self):
        """ Delete a customer row.
        """
        LOGGER.info("test_delete_customer")
        vegeta_colt = CUSTOMERS["vegeta_colt"]
        delete_customer(vegeta_colt["customer_id"])

        self.assertDictEqual(search_customer(vegeta_colt["customer_id"]), {})

    def test_delete_customer_not_in_the_db(self):
        """ Try to delete a customer that is not in the database
        """
        LOGGER.info("test_delete_customer_not_in_the_db")

        # first delete the customer
        vegeta_colt = CUSTOMERS["vegeta_colt"]
        delete_customer(vegeta_colt["customer_id"])

        # make sure the customer has been deleted
        with DATABASE.transaction():
            try:
                Customer.get(Customer.customer_id == vegeta_colt["customer_id"])
            except DoesNotExist:
                assert True
            else:
                LOGGER.error("test_delete_customer_not_in_the_db: customer was not deleted")
                assert False

        # Now try deleting a customer that isn't there.
        with self.assertRaises(ValueError):
            delete_customer(vegeta_colt["customer_id"])

    def test_update_customer_credit(self):
        """ Try to update a customer's credit.
        """
        LOGGER.info("test_update_customer_credit")

        beat_choonz = CUSTOMERS["beat_choonz"]
        self.assertEqual(beat_choonz["credit_limit"], 10000.00)

        update_customer_credit(beat_choonz["customer_id"], 13000.01)
        acustomer = Customer.get(Customer.customer_id == beat_choonz["customer_id"])
        self.assertEqual(float(acustomer.credit_limit), 13000.01)

    def test_update_customer_credit_not_in_the_db(self):
        """ Try to update the credit of a customer that isn't in the db.
        """
        # make sure the customer has been deleted
        with DATABASE.transaction():
            try:
                Customer.get(Customer.customer_id == 4)
            except DoesNotExist:
                assert True
            else:
                LOGGER.error("test_update_customer_credit_not_in_the_db: customer is in the db")
                assert False

        # Now try updating credit for a customer that isn't there.
        with self.assertRaises(ValueError):
            update_customer_credit(4, 13000.00)

    def test_list_active_customers(self):
        """ Find the number of active customers.
        """
        LOGGER.info("test_list_active_customers")
        active_customers = [acustomer for acustomer in CUSTOMERS.values()
                            if acustomer["status"] is True]

        self.assertEqual(list_active_customers(), len(active_customers))
