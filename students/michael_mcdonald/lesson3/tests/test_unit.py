"""test the inventory management module"""

# pylint: disable=E1111
# pylint: disable=import-error
# pylint: disable=W0614
# pylint: disable-msg=R0913
# pylint: disable-msg=too-many-locals

from unittest import TestCase
from unittest.mock import patch
import unittest.mock
import uuid
import sqlite3
import logging
import peewee as pw
import lesson3.basic_operations as ba  # pylint: disable=import-error

# set up logging
LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"
formatter = logging.Formatter(LOG_FORMAT)
file_handler = logging.FileHandler('basic_operations.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)
console_handler.setFormatter(formatter)

logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# integration testing
# linting
# cd C:\Users\mimcdona\Dropbox\UW\UW-Python220_Project
# python -m unittest lesson3\tests\test_unit.py
# python -m coverage run --source=lesson3 -m unittest lesson3\tests\test_unit.py
# python -m coverage report -m

CUSTOMER_ID = '3111111-e25a-11ea-9f69-287fcf638d95'
NAME = 'name1'
LASTNAME = 'lastname1'
HOME_ADDRESS = 'home_address1'
PHONE_NUMBER = 'phone_number1'
EMAIL_ADDRESS = 'email_address1'
STATUS = 'active'
CREDIT_LIMIT = 1000


class Connection:
    """connect to database"""

    database = pw.SqliteDatabase('customers.db', pragmas={'foreign_keys': 1})
    connection_result = ''
    try:
        database.connect()
        logger.info('connection successful')
        connection_result = 'connection successful'
    except sqlite3.Error as error:
        logger.error('sqlite3 connection error %s', error, exc_info=True)
        connection_result = 'connection failed'


class BaseModel(pw.Model):
    """create a db base model"""

    class Meta():
        """ add meta class"""

        my_connection = Connection()
        database = my_connection.database


class Customer(BaseModel):
    """ customer model/table"""

    customer_id = pw.CharField(max_length=200, primary_key=True, null=False)
    name = pw.CharField(max_length=200, null=False)
    lastname = pw.CharField(max_length=200, null=False)
    home_address = pw.CharField(max_length=200, null=False)
    phone_number = pw.CharField(max_length=50, null=False)
    email_address = pw.CharField(max_length=200, null=False)
    status = pw.CharField(max_length=200, null=False)
    credit_limit = pw.IntegerField(default=0, null=False)  # int


def insert_new_customer():
    """insert customer test data"""

    with Connection.database.transaction():
        new_customers = [{'name': 'name3', 'lastname': 'lastname3',
                          'home_address': 'home_address3',
                          'phone_number': 'phone_number3',
                          'email_address': 'email_address3',
                          'status': 'active', 'credit_limit': 1000,
                          'customer_id': '30000000-e25a-11ea-9f69-287fcf638d95'}]
        with Connection.database.atomic():
            Customer.insert_many(new_customers).execute()


# python -m coverage run --source=lesson3 -m unittest lesson3\tests\test_unit.py
class TestBasicOperations(TestCase):
    """test TestBasicOperations class"""

    m_in = ['1', '2', '3', '4', '5', '6', 'q']
    c_id = '30000000-e25a-11ea-9f69-287fcf638d95'

    @staticmethod
    def test_main_menu():
        """test main_menu"""

        with unittest.mock.patch('builtins.input',
                                 side_effect=TestBasicOperations.m_in) as main_menu_test:
            ba.main_menu()
            main_menu_test.assert_has_calls([unittest.mock.call('>')])

    def test_delete_all_customers(self):
        """test delete_all_customers"""

        ba.delete_all_customers()
        cust_cnt = ba.Customer.select().count()
        self.assertEqual(0, cust_cnt)

    @patch('builtins.input', side_effect=[c_id, '3000'])
    def test_update_customer_credit_handler(self, mock_input):
        """test update credit"""
        ba.delete_all_customers()
        insert_new_customer()
        ba.update_customer_credit_handler()
        tmp_customer = Customer.get_or_none(Customer.customer_id == TestBasicOperations.c_id)
        if tmp_customer is not None:
            new_credit_limit = tmp_customer.credit_limit
        self.assertEqual(new_credit_limit, 3000)
        print(mock_input)

    @patch('builtins.input', side_effect=[c_id])
    def test_delete_customer_handler(self, mock_input):
        """test delete customer handler"""

        ba.delete_all_customers()
        insert_new_customer()
        tmp_customer = Customer.get_or_none(Customer.customer_id == TestBasicOperations.c_id)
        if tmp_customer is not None:
            result = 'customer exists'
        self.assertEqual(result, 'customer exists')
        ba.delete_customer_handler()
        tmp_customer = Customer.get_or_none(Customer.customer_id == TestBasicOperations.c_id)
        if tmp_customer is None:
            result = 'customer deleted'
        self.assertEqual(result, 'customer deleted')
        print(mock_input)

    @patch('builtins.input', side_effect=[CUSTOMER_ID, NAME, LASTNAME,
                                          HOME_ADDRESS, PHONE_NUMBER,
                                          EMAIL_ADDRESS, 'a', '3000'])
    def test_add_customer_handler(self, mock_input):
        """test add customer handler"""

        ba.delete_all_customers()
        tmp_customer = Customer.get_or_none(Customer.customer_id == TestBasicOperations.c_id)
        if tmp_customer is None:
            result = 'customer does not exist'
        self.assertEqual(result, 'customer does not exist')
        ba.add_customer_handler()
        tmp_customer = Customer.get_or_none(Customer.customer_id == TestBasicOperations.c_id)
        if tmp_customer is None:
            result = 'customer does exist'
        self.assertEqual(result, 'customer does exist')
        print(mock_input)

    @patch('builtins.input', side_effect=[c_id])
    def test_search_customer_handler(self, mock_input):
        """test delete customer handler"""

        ba.delete_all_customers()
        insert_new_customer()
        results = ba.search_customer_handler()
        self.assertEqual(results, '{}\tname3\tlastname3'.format(TestBasicOperations.c_id))
        print(mock_input)

    def test_insert_new_customers(self):
        """test insert_new_customers"""

        ba.delete_all_customers()
        ba.insert_new_customers()
        cust_cnt = ba.Customer.select().count()
        self.assertEqual(2, cust_cnt)

    def test_connection(self):
        """test connection"""

        my_unittest_connection = Connection()
        my_unittest_result = my_unittest_connection.connection_result
        my_test_connection = ba.Connection()
        my_test_result = my_test_connection.connection_result
        self.assertEqual(my_unittest_result, my_test_result)
        self.assertEqual(my_unittest_result, 'connection successful')
        self.assertEqual(my_test_result, 'connection successful')

    def test_is_digit(self):
        """test is digit"""

        self.assertFalse(ba.is_digit('one'))
        self.assertTrue(ba.is_digit('1'))

    def test_add_new_customer(self):
        """test_add_new_customer"""

        customer_id = uuid.uuid1()
        ba.add_customer(customer_id, NAME, LASTNAME, HOME_ADDRESS,
                        PHONE_NUMBER, EMAIL_ADDRESS, STATUS, CREDIT_LIMIT)
        test_results = ba.Customer.get_or_none(ba.Customer.customer_id == customer_id)
        self.assertEqual(test_results.name, 'name1')
        self.assertEqual(test_results.lastname, 'lastname1')
        self.assertEqual(test_results.home_address, 'home_address1')
        self.assertEqual(test_results.phone_number, 'phone_number1')
        self.assertEqual(test_results.email_address, 'email_address1')
        self.assertEqual(test_results.status, 'active')
        self.assertEqual(test_results.credit_limit, 1000)

    def test_search_customer(self):
        """test search customer method"""

        customer_id = uuid.uuid1()
        ba.add_customer(customer_id, NAME, LASTNAME, HOME_ADDRESS,
                        PHONE_NUMBER, EMAIL_ADDRESS, STATUS, CREDIT_LIMIT)
        test_results = ba.search_customer(customer_id)
        self.assertEqual(test_results['name'], 'name1')
        self.assertEqual(test_results['lastname'], 'lastname1')
        self.assertEqual(test_results['home_address'], 'home_address1')
        self.assertEqual(test_results['phone_number'], 'phone_number1')
        self.assertEqual(test_results['email_address'], 'email_address1')
        self.assertEqual(test_results['status'], 'active')
        self.assertEqual(test_results['credit_limit'], 1000)

    def test_delete_customer(self):
        """test delete customer method"""

        customer_id = uuid.uuid1()
        ba.add_customer(customer_id, NAME, LASTNAME, HOME_ADDRESS,
                        PHONE_NUMBER, EMAIL_ADDRESS, STATUS, CREDIT_LIMIT)
        ba.delete_customer(customer_id)
        tmp_customer = ba.Customer.get_or_none(ba.Customer.customer_id == customer_id)
        self.assertIsNone(tmp_customer)

    def test_update_customer_credit(self):
        """update_customer_credit"""

        new_credit = 9999
        customer_id = uuid.uuid1()
        ba.add_customer(customer_id, NAME, LASTNAME, HOME_ADDRESS,
                        PHONE_NUMBER, EMAIL_ADDRESS, STATUS, CREDIT_LIMIT)
        ba.update_customer_credit(customer_id, new_credit)
        test_results = ba.search_customer(customer_id)
        self.assertEqual(new_credit, test_results['credit_limit'])

    def test_list_active_customers(self):
        """list_active_customers"""

        cnt1 = Customer.select().where(Customer.status == 'active').count()
        self.assertEqual(cnt1, ba.list_active_customers())

    @classmethod
    def test_exit_program(cls):
        """text exit program"""

        with patch('sys.exit') as mock_exit_program:
            ba.exit_program()
            assert mock_exit_program.called


class TestOperationsIntegrated(TestCase):
    """ run an integrated test"""

    def test_integrated(self):
        """ integration method"""

        new_credit = 9999
        customer_id = uuid.uuid1()
        ba.add_customer(customer_id, NAME, LASTNAME, HOME_ADDRESS,
                        PHONE_NUMBER, EMAIL_ADDRESS, STATUS, CREDIT_LIMIT)
        test_results = ba.search_customer(customer_id)
        self.assertEqual(test_results['name'], 'name1')
        self.assertEqual(test_results['lastname'], 'lastname1')
        self.assertEqual(test_results['home_address'], 'home_address1')
        self.assertEqual(test_results['phone_number'], 'phone_number1')
        self.assertEqual(test_results['email_address'], 'email_address1')
        self.assertEqual(test_results['status'], 'active')
        self.assertEqual(test_results['credit_limit'], 1000)
        ba.delete_customer(customer_id)
        tmp_customer = ba.Customer.get_or_none(ba.Customer.customer_id == customer_id)
        self.assertIsNone(tmp_customer)
        customer_id = uuid.uuid1()
        ba.add_customer(customer_id, NAME, LASTNAME, HOME_ADDRESS,
                        PHONE_NUMBER, EMAIL_ADDRESS, STATUS, CREDIT_LIMIT)
        ba.update_customer_credit(customer_id, new_credit)
        test_results = ba.search_customer(customer_id)
        self.assertEqual(new_credit, test_results['credit_limit'])
        cnt1 = Customer.select().where(Customer.status == 'active').count()
        self.assertEqual(cnt1, ba.list_active_customers())
