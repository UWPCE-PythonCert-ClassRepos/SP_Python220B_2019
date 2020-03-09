"""Testing for basic_operations.py"""

# pylint: disable=W0401, W0614, E1120

from unittest import TestCase
from decimal import *
from peewee import *
from src.basic_operations import *
from src.customer_model import Customer


def reset_db(): # Question: Is there a better way to do this just for testing?
    """Clear the database for testing."""

    db.drop_tables([Customer])
    db.create_tables([Customer])


class BasicOperationsTests(TestCase): # Question: Does unittest test in the live db or a clone of it? If live, what's the best way to test in a sandbox?
    """Unit tests for basic_operations.py"""

    def test_add_customer(self):
        """Test adding new customer to the database."""

        reset_db()
        add_customer("test_id1", "Rhianna", "doesntneedalastname",
                     "543 Sample Address, Winnebago, AK 99302",
                     "3241232455", "star@skycloud.com", True, 333.33)

        test_customer = Customer.get_by_id("test_id1")

        self.assertEqual(test_customer.first_name, "Rhianna")
        self.assertEqual(test_customer.phone_number, "3241232455")

        test_customer.delete_instance()


    def test_add_customer_typeerror(self):
        """
        Prevent addition of new customer to the database if the record
        contains incomplete data.
        """

        reset_db()
        with self.assertRaises(TypeError):
            add_customer("not_enough_args")


    def test_search_customer(self):
        """Test finding existing record in db."""

        reset_db()
        add_customer("test_id1", "Rhianna", "doesntneedalastname",
                     "543 Sample Address, Winnebago, AK 99302",
                     "3241232455", "star@skycloud.com", True, 333.33)

        test_dict = {'first_name': "Rhianna",
                     'last_name': "doesntneedalastname",
                     'email_address': "star@skycloud.com",
                     'phone_number': "3241232455"}

        self.assertEqual(search_customer("test_id1"), test_dict)


    def test_search_customer_no_match(self):
        """Test returning empty dict when searching for nonexistent records."""

        reset_db()
        self.assertEqual(search_customer("bad_id"), {})


    def test_delete_customer(self):
        """Test deleting a record from db."""

        reset_db()
        add_customer("test_id1", "Rhianna", "doesntneedalastname",
                     "543 Sample Address, Winnebago, AK 99302",
                     "3241232455", "star@skycloud.com", True, 333.33)

        # Make sure the record exists
        self.assertEqual(Customer.get_by_id("test_id1").first_name, "Rhianna")

        # Then delete the record and make sure it's gone
        delete_customer("test_id1")
        self.assertEqual(search_customer("test_id1"), {})


    def test_delete_customer_no_match(self):
        """Test raising exception if no record to delete."""

        reset_db()
        with self.assertRaises(DoesNotExist):
            delete_customer("bad_id")


    def test_update_customer_credit(self):
        """Test updating customer credit."""

        reset_db()
        add_customer("test_id1", "Rhianna", "doesntneedalastname",
                     "543 Sample Address, Winnebago, AK 99302",
                     "3241232455", "star@skycloud.com", True, 333.33)

        # Make sure the current credit limit is 333.33
        self.assertEqual(Customer.get_by_id("test_id1").credit_limit,
                         Decimal('333.33'))

        # Then update the record and make sure it changed
        update_customer_credit("test_id1", Decimal('1000.00'))
        self.assertEqual(Customer.get_by_id("test_id1").credit_limit,
                         Decimal('1000.00'))


    def test_list_active_customers(self):
        """Test counting the number of customers with active status."""

        reset_db()
        add_customer("test_id1", "Rhianna", "doesntneedalastname",
                     "543 Sample Address, Winnebago, AK 99302",
                     "3241232455", "star@skycloud.com", True, 333.33)
        self.assertEqual(list_active_customers(), 1)

        add_customer("test_id2", "John", "Muir", "Yosemite",
                     "3241232455", "muir@skycloud.com", False, 333.33)
        self.assertEqual(list_active_customers(), 1)

        add_customer("test_id3", "Beyonce", "Knowles-Carter",
                     "543 Sample Address, Winnebago, AK 99302",
                     "3241232455", "bey@skycloud.com", True, 333.33)
        self.assertEqual(list_active_customers(), 2)

reset_db()
