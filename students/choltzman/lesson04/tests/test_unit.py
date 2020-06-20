"""
Unit tests for basic operations
"""
from unittest import TestCase
import peewee as pw
import basic_operations as bo

MODELS = [bo.Customer]
TEST_DB = pw.SqliteDatabase(':memory:')

# sample customer data
CUST1 = {
    'customer_id': 1,
    'full_name': "John Doe",
    'last_name': "Doe",
    'home_address': "123 Example Street",
    'phone_number': "15551234567",
    'email_address': "john@example.com",
    'is_active': True,
    'credit_limit': 10000
}
CUST2 = {
    'customer_id': 2,
    'full_name': "Jane Poe",
    'last_name': "Poe",
    'home_address': "456 Example Lane",
    'phone_number': "15557654321",
    'email_address': "jane@example.com",
    'is_active': False,
    'credit_limit': 11000
}


class TestBasicOperations(TestCase):
    """Test basic operations functions"""

    def setUp(self):
        """Create database in memory for testing"""
        TEST_DB.bind(MODELS, bind_refs=False, bind_backrefs=False)
        TEST_DB.connect()
        TEST_DB.create_tables(MODELS)

    def tearDown(self):
        """Tear down the temporary database"""
        TEST_DB.drop_tables(MODELS)
        TEST_DB.close()

    def test_add_customer(self):
        """Test adding a customer to the db"""
        bo.add_customer(**CUST1)
        querydata = bo.Customer.get(
            bo.Customer.customer_id == CUST1['customer_id'])
        self.assertEqual(querydata.customer_id, CUST1['customer_id'])
        self.assertEqual(querydata.full_name, CUST1['full_name'])
        self.assertEqual(querydata.last_name, CUST1['last_name'])
        self.assertEqual(querydata.home_address, CUST1['home_address'])
        self.assertEqual(querydata.phone_number, CUST1['phone_number'])
        self.assertEqual(querydata.email_address, CUST1['email_address'])
        self.assertEqual(querydata.is_active, CUST1['is_active'])
        self.assertEqual(querydata.credit_limit, CUST1['credit_limit'])

    def test_add_customer_twice(self):
        """Test adding the same customer twice"""
        with self.assertRaises(ValueError):
            bo.add_customer(**CUST1)
            bo.add_customer(**CUST1)

    def test_search_customer(self):
        """Test the search_customer function"""
        # expected output
        expected = {
            'full_name': CUST1['full_name'],
            'last_name': CUST1['last_name'],
            'email_address': CUST1['email_address'],
            'phone_number': CUST1['phone_number']
        }

        # add customer and check
        bo.add_customer(**CUST1)
        data = bo.search_customer(CUST1['customer_id'])
        self.assertEqual(data, expected)

    def test_search_customer_missing(self):
        """Test searching for an invalid customer_id"""
        data = bo.search_customer(CUST1['customer_id'])
        self.assertIsNone(data)

    def test_delete_customer(self):
        """Test the delete_customer function"""
        bo.add_customer(**CUST1)
        bo.delete_customer(CUST1['customer_id'])
        with self.assertRaises(pw.DoesNotExist):
            bo.Customer.get(bo.Customer.customer_id == CUST1['customer_id'])

    def test_delete_customer_missing(self):
        """Test deleting an invalid customer_id"""
        with self.assertRaises(ValueError):
            bo.delete_customer(CUST1['customer_id'])

    def test_update_credit(self):
        """Test the update_customer_credit function"""
        bo.add_customer(**CUST1)
        bo.update_customer_credit(CUST1['customer_id'], 5000)
        querydata = bo.Customer.get(
            bo.Customer.customer_id == CUST1['customer_id'])
        self.assertEqual(querydata.credit_limit, 5000)

    def test_update_credit_missing(self):
        """Test updating credit for an invalid customer_id"""
        with self.assertRaises(ValueError):
            bo.update_customer_credit(CUST1['customer_id'], 5000)

    def test_list_active(self):
        """Test the list_active_customers function"""
        bo.add_customer(**CUST1)
        self.assertEqual(bo.list_active_customers(), 1)
        bo.add_customer(**CUST2)
        self.assertEqual(bo.list_active_customers(), 1)
