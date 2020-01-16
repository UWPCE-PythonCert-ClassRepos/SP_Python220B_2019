""" Integration tests for the lesson03 assignment.

One large test that does a bunch of things.

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


class CustomerDBIntegrationTests(TestCase):
    """ One large test that does the following, in order:
    1. First, clears out the Customer table
    2. Adds three rows to the Customer table (add_customers calls add_customer)
    3. Deletes a row containing a customer whose status is active. (delete_customer)
    4. Updates the other active customer's credit. (update_customer_credit)

    It then verifies that the remaining data looks like it should using
    1. list_active_customer to get the number of active customers remaining.
    2. search_customer to search for the remaining customer rows, then verify the field data for
       those.
    3. update_customer_credit to try to update the deleted customer's credit
    4. delete_customer to try to delete the deleted customer
    5. search_customer for the customer who was deleted.
    6. update_multiple_customers_credit to update all the customer credit limits in batch,
       including trying with the deleted one.

    Note: I would usually decompose this into much smaller functions but it kind of makes sense for
    integration testing to do this all together.
    """

    def tearDown(self):
        """ Delete the Customer table data.
        """
        delete_customer_table()

    def test_it_all(self):
        """ Create a customer model.
        """
        LOGGER.info("test_it_all")

        # Make sure a Customer table exists and make sure it is empty.
        create_tables()
        delete_customer_table()

        # Add three rows to the Customer table from the CUSTOMERS data, above.
        add_customers(CUSTOMERS)

        # Delete a row containing a customer whose status is active.
        customer_id_deleted = -1  # will be used in blocks below
        customer_id_credit_updated = -1  # will be used in blocks below

        with DATABASE.transaction():
            query = Customer.select().where(Customer.status == True)  # pylint: disable=E1111,C0121
            self.assertTrue(len(query) == 2)
            customer_id_deleted = query[0].customer_id
            delete_customer(customer_id_deleted)
            # update credit for the other active customer
            customer_id_credit_updated = query[1].customer_id
            update_customer_credit(customer_id_credit_updated, 1300.01)

        # Verify that there is 1 active customer in the db.
        self.assertEqual(list_active_customers(), 1)

        # Search the remaining customers and verify their data
        customer_lookup = {"Beat": "beat_choonz",
                           "Shady": "shady_flava",
                           "Vegeta": "vegeta_colt"}

        for customer_id in range(1, 4):
            if customer_id is customer_id_deleted:
                continue

            acustomer = search_customer(customer_id)
            original_customer_key = customer_lookup[acustomer["name"]]
            original_customer = CUSTOMERS[original_customer_key]

            self.assertEqual(acustomer["name"], original_customer["first_name"])
            self.assertEqual(acustomer["last_name"], original_customer["last_name"])
            self.assertEqual(acustomer["email_address"], original_customer["email_address"])
            self.assertEqual(acustomer["phone_number"], original_customer["phone"])

            # Verify the new credit limit for the customer whose credit was updated
            if customer_id is customer_id_credit_updated:
                with DATABASE.transaction():
                    query = Customer.select().where(Customer.customer_id == customer_id)  # pylint: disable=E1111
                    self.assertEqual(float(query[0].credit_limit), 1300.01)

        # Try to update the deleted customer's credit
        with self.assertRaises(ValueError):
            update_customer_credit(customer_id_deleted, 12345.00)

        # Try to delete the deleted customer
        with self.assertRaises(ValueError):
            delete_customer(customer_id_deleted)

        # Try to search for deleted customer
        acustomer = search_customer(customer_id_deleted)
        self.assertDictEqual(acustomer, {})

        # Update customer credit in batch
        ids_credit = tuple((id, 21000) for id in range(1, 4))

        # Check all results are True, meaning all the customers' credit was updated successfully,
        # except for the customer that is not in the db, which should have a False result.
        for result in update_multiple_customers_credit(ids_credit):
            if result[0] is customer_id_deleted:
                self.assertFalse(result[1])
            else:
                self.assertTrue(result[1])

        # Check the ones that got updated that they were updated to 21000.00.
        for customer_id in range(1, 4):
            with DATABASE.transaction():
                try:
                    acustomer = Customer.get(Customer.customer_id == customer_id)
                    self.assertEqual(float(acustomer.credit_limit), 21000.00)
                except DoesNotExist:
                    pass
