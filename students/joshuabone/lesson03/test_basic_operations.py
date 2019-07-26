import decimal
import unittest
from basic_operations import *

DATABASE.init('unittest.db')


class CustomerTests(unittest.TestCase):
    def setUp(self):
        DATABASE.drop_tables([Customer])
        DATABASE.create_tables([Customer])

    def test_add_customer(self):
        added = add_customer(
            customer_id=111,
            name="Billy",
            lastname="Bones",
            home_address="123 4th Ave, Seattle WA",
            phone_number=1234567890,
            email_address="spam@gmail.com",
            status=True,
            credit_limit=1234.56
        )
        retrieved = Customer.get(Customer.customer_id == 111)
        self.assertEqual(added, retrieved)

    def test_add_duplicate_key(self):
        first = add_customer(
            customer_id=111,
            name="Billy",
            lastname="Bones",
            home_address="123 4th Ave, Seattle WA",
            phone_number=1234567890,
            email_address="spam@gmail.com",
            status=True,
            credit_limit=1234.56
        )
        second = add_customer(
            customer_id=111,
            name="Roger"
        )
        self.assertIsNone(second)
        retrieved = Customer.get(Customer.customer_id == 111)
        self.assertEqual(retrieved, first)
        self.assertEqual(len(Customer), 1)

    def test_search_customer(self):
        added = add_customer(customer_id=111, name="Aaron")
        retrieved = search_customer(111)
        self.assertEqual(retrieved, added)

    def test_search_customer_not_found(self):
        add_customer(customer_id=111, name="Aaron")
        retrieved = search_customer(222)
        self.assertIsNone(retrieved)

    def test_delete_customer(self):
        add_customer(customer_id=111, name="Aaron")
        delete_customer(111)
        retrieved = search_customer(111)
        self.assertIsNone(retrieved)

    def test_update_credit(self):
        add_customer(customer_id=111, name="Aaron", credit_limit=123.45)
        update_customer_credit(111, 246.90)
        retrieved = search_customer(111)
        self.assertAlmostEqual(retrieved.credit_limit, decimal.Decimal(246.90))

    def test_update_credit_not_found(self):
        self.assertRaises(ValueError, lambda: update_customer_credit(111, 7.1))

    def test_list_active_customers(self):
        add_customer(customer_id=111, name="Amy", status=True)
        add_customer(customer_id=222, name="Ben", status=False)
        add_customer(customer_id=333, name="Carrie", status=True)
        add_customer(customer_id=444, name="David")  # status unset
        add_customer(customer_id=555, name="Erin", status=True)
        self.assertEqual(list_active_customers(), 3)
