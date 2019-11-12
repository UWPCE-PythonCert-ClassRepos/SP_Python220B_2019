# Advanced Programming In Python - Lesson 3 Assigmnet 1: Relational Databases
# RedMine Issue - SchoolOps-13
# Code Poet: Anthony McKeever
# Start Date: 11/06/2019
# End Date: 11/09/2019

"""
Unit tests for create_customers_db, basic_operations, and customer_db_schema.
"""

import datetime
import logging
from unittest import TestCase
from unittest import mock
from unittest.mock import patch
from unittest.mock import MagicMock

import peewee

import create_customers_db as CreateDb
import basic_operations as BaseOps
from customer_db_schema import Customers


class MockCustomer(Customers):
    """ A Mock Customer for Testing """

    customer_id = "123"
    first_name = "Amelia"
    last_name = "Bedelia"
    home_address = "123 Starshine Ln."
    phone_number = "Pennsylvania 65000"
    email_address = "amelia@rogersfamily.com"
    status = "active"
    credit_limit = 3.14


class FakeArgs():
    """ Fake Arguements for testing """

    debug = 0
    import_file = "stuff"
    import_bandwidth = 5


class MockDatabaseTest(TestCase):
    """ Base for tests that required database mocks """

    def setUp(self):
        customer_mock = MockCustomer()

        self.hold_sqlite_db = peewee.SqliteDatabase
        self.hold_char_field = peewee.CharField
        self.hold_decimal_field = peewee.DecimalField
        self.hold_datetime_field = peewee.DateField
        self.hold_model = peewee.Model
        self.hold_datetime_value = datetime.datetime.now()

        peewee.SqliteDatabase = MagicMock()
        peewee.SqliteDatabase.connect = MagicMock()
        peewee.execute_sql = MagicMock()
        peewee.Model.save = MagicMock()
        peewee.Model.delete = MagicMock()
        peewee.Model.get_or_create = MagicMock(return_value=[customer_mock])
        peewee.Model.get_or_none = MagicMock(return_value=customer_mock)

    def tearDown(self):
        peewee.SqliteDatabase = self.hold_sqlite_db
        peewee.CharField = self.hold_char_field
        peewee.DecimalField = self.hold_decimal_field
        peewee.DateTimeField = self.hold_datetime_field
        peewee.Model = self.hold_model


class TestCustomerDBSchema(MockDatabaseTest):
    """ Tests the Customer DB Schema """

    def test_customer_schema_fields(self):
        """ Validates the fileds in the customer schema """
        with patch("customer_db_schema.Customers.get_or_create") as handle_get:
            handle_get.return_value = [MockCustomer]
            customer = Customers().get_or_create("test")[0]
            self.assertEqual(customer.customer_id, "123")
            self.assertEqual(customer.first_name, "Amelia")
            self.assertEqual(customer.last_name, "Bedelia")
            self.assertEqual(customer.home_address, "123 Starshine Ln.")
            self.assertEqual(customer.phone_number, "Pennsylvania 65000")
            self.assertEqual(customer.email_address, "amelia@rogersfamily.com")
            self.assertEqual(customer.status, "active")
            self.assertEqual(customer.credit_limit, 3.14)
            self.assertEqual(customer.date_created, self.hold_datetime_value)
            self.assertEqual(customer.date_modified, self.hold_datetime_value)

    def test_customer_schema_save(self):
        """ Validates saving the customer schema """
        customer = Customers().get_or_create("test")[0]
        customer.save()
        self.assertGreaterEqual(customer.date_modified,
                                self.hold_datetime_value)

    def test_customer_schema_as_dictionary(self):
        """ Validates returning the customer schema as a dictionary """
        with patch("customer_db_schema.Customers.get_or_create") as handle_get:
            handle_get.return_value = [MockCustomer]
            customer = Customers().get_or_create("test")[0]
            cust_dict = customer.as_dictionary(MockCustomer)

            self.assertEqual(cust_dict["customer_id"], "123")
            self.assertEqual(cust_dict["first_name"], "Amelia")
            self.assertEqual(cust_dict["last_name"], "Bedelia")
            self.assertEqual(cust_dict["home_address"], "123 Starshine Ln.")
            self.assertEqual(cust_dict["phone_number"], "Pennsylvania 65000")
            self.assertEqual(cust_dict["email_address"],
                             "amelia@rogersfamily.com")
            self.assertEqual(cust_dict["status"], "active")
            self.assertEqual(cust_dict["credit_limit"], 3.14)
            self.assertEqual(cust_dict["date_created"],
                             self.hold_datetime_value)
            self.assertEqual(cust_dict["date_modified"],
                             self.hold_datetime_value)

    def test_customer_schema_as_contact_info_dict(self):
        """
        Validates returning the customer schema as a dictionary with
        contact infomration only.
        """
        with patch("customer_db_schema.Customers.get_or_create") as handle_get:
            handle_get.return_value = [MockCustomer]
            customer = Customers().get_or_create("test")[0]
            cust_dict = customer.as_contact_info_dictionary(MockCustomer)

            self.assertEqual(cust_dict["first_name"], "Amelia")
            self.assertEqual(cust_dict["last_name"], "Bedelia")
            self.assertEqual(cust_dict["phone_number"], "Pennsylvania 65000")
            self.assertEqual(cust_dict["email_address"],
                             "amelia@rogersfamily.com")


class TestBasicOperations(MockDatabaseTest):
    """ Tests the basic_operations module """

    def test_add_customer_golden_path(self):
        """ Validates customers can be added to the DB """
        with self.assertLogs() as mock_logger:
            BaseOps.add_customer("123",
                                 "Amelia",
                                 "Bedelia",
                                 "123 Starshine Ln.",
                                 "Pennsylvania 65000",
                                 "amelia@rogersfamily.com",
                                 "active",
                                 3.14)
            name = "basic_operations"
            msg = f"INFO:{name}:Saved customer with ID: None"
            self.assertIn(msg, mock_logger.output)

    def test_add_customer_value_error(self):
        """
        Validates that a value error is thrown if a customer's status is not
        'active' or 'inactive'
        """
        status = str("She called the customer and told them to exercise." +
                     "\"Amelia, what are you doing?!\" Roared Mr. Rogers." +
                     "\"I was told to make them active.\" Replied Amelia")
        with self.assertRaises(ValueError):
            BaseOps.add_customer("123",
                                 "Amelia",
                                 "Bedelia",
                                 "123 Starshine Ln.",
                                 "Pennsylvania 65000",
                                 "amelia@rogersfamily.com",
                                 status,
                                 3.14)

    def test_add_customer_exceptions(self):
        """
        Validates add customer exceptions (IntegrityError and OperationalError)
        are handled and elegantly logged.
        """
        with patch("basic_operations.Customers.get_or_create") as handle_get:
            handle_get.side_effect = [peewee.IntegrityError("integrity"),
                                      peewee.OperationalError("operational")]

            with self.assertLogs() as mock_logger:
                BaseOps.add_customer("123",
                                     "Amelia",
                                     "Bedelia",
                                     "123 Starshine Ln.",
                                     "Pennsylvania 65000",
                                     "amelia@rogersfamily.com",
                                     "active",
                                     3.14)
                msg = "ERROR:basic_operations:integrity"
                self.assertIn(msg, mock_logger.output)

                BaseOps.add_customer("123",
                                     "Amelia",
                                     "Bedelia",
                                     "123 Starshine Ln.",
                                     "Pennsylvania 65000",
                                     "amelia@rogersfamily.com",
                                     "active",
                                     3.14)
                msg = "ERROR:basic_operations:operational"
                self.assertIn(msg, mock_logger.output)

    def test_search_customer_has_results(self):
        """ Validates customer search results """
        mock_module = "basic_operations.Customers.as_contact_info_dictionary"
        with patch(mock_module) as as_dict:
            as_dict.return_value = {"stuff": "in a box"}

            cust_dict = BaseOps.search_customer("123")
            self.assertEqual("in a box", cust_dict["stuff"])

    def test_search_customer_has_no_results(self):
        """ Validates empty dictionary returned when customer doesn't exist """
        mock_module = "basic_operations.Customers.get_or_none"
        with patch(mock_module) as get_none:
            get_none.return_value = None

            with self.assertLogs() as mock_logger:
                cust_dict = BaseOps.search_customer("456")
                self.assertEqual(cust_dict, {})

                log_msg = "No customer exists with customer_id: 456"
                msg = f"INFO:basic_operations:{log_msg}"
                self.assertIn(msg, mock_logger.output)

    def test_search_customer_error_handle(self):
        """
        Validates OperationalErrors are handled and elegantly logged
        during customer search
        """
        mock_module = "basic_operations.Customers.get_or_none"
        with patch(mock_module) as get_none:
            get_none.side_effect = peewee.OperationalError("operational")

            with self.assertLogs() as mock_logger:
                cust_dict = BaseOps.search_customer("[]")
                self.assertEqual(cust_dict, {})

                msg = "ERROR:basic_operations:operational"
                self.assertIn(msg, mock_logger.output)

                log_msg = "Failed look up of customer with customer_id: []"
                msg = f"INFO:basic_operations:{log_msg}"
                self.assertIn(msg, mock_logger.output)

    def test_delete_customer(self):
        """ Validates customer deletion """
        mock_module = "basic_operations.Customers.delete_by_id"
        with patch(mock_module):
            with self.assertLogs() as mock_logger:
                BaseOps.delete_customer("123")

                msg = "INFO:basic_operations:Customer deleted successfully."
                self.assertIn(msg, mock_logger.output)

    def test_delete_customer_error_handle(self):
        """
        Validates OperationalErrors are handled and elegantly logged
        during customer delete
        """
        mock_module = "basic_operations.Customers.delete_by_id"
        with patch(mock_module) as delete_handle:
            delete_handle.side_effect = peewee.OperationalError("operational")

            with self.assertLogs() as mock_logger:
                BaseOps.delete_customer("[]")

                msg = "ERROR:basic_operations:operational"
                self.assertIn(msg, mock_logger.output)

                log_msg = "Failed to delete customer with customer_id: []"
                msg = f"INFO:basic_operations:{log_msg}"
                self.assertIn(msg, mock_logger.output)

    def test_update_customer_credit_golden_path(self):
        """ Validates updating a customer's credit limit """
        with patch("basic_operations.Customers.save"):
            with self.assertLogs() as mock_logger:
                BaseOps.update_customer_credit("123", 2.71)

                log_msg = "Credit limit updated from 3.14 to 2.71"
                msg = f"INFO:basic_operations:{log_msg}"
                self.assertIn(msg, mock_logger.output)

                # reset mock customer's credit limit incase test case execution
                # executes this test case before others.
                MockCustomer.credit_limit = 3.14

    def test_update_customer_credit_no_customer(self):
        """
        Validates value error thrown when updating a customer's credit limit
        if customer does not exist.
        """
        mock_module = "basic_operations.Customers.get_or_none"
        with patch(mock_module) as get_none:
            get_none.return_value = None

            with self.assertLogs() as mock_logger:
                with self.assertRaises(ValueError):
                    BaseOps.update_customer_credit("456", 2.71)

                log_msg = "No customer exists with customer_id: 456"
                msg = f"INFO:basic_operations:{log_msg}"
                self.assertIn(msg, mock_logger.output)

    def test_update_customer_credit_errors(self):
        """
        Validates value error thrown when updating a customer's credit limit
        if an exception (IntegrityError or OperationalError) is thrown.
        """
        mock_module = "basic_operations.Customers.get_or_none"
        with patch(mock_module) as get_none:
            get_none.side_effect = [peewee.IntegrityError("integrity"),
                                    peewee.OperationalError("operational")]

            with self.assertRaises(ValueError):
                BaseOps.update_customer_credit("[]", 2.71)

            with self.assertRaises(ValueError):
                BaseOps.update_customer_credit("[]", 2.71)

    def test_list_active_customers(self):
        """ Validates active customer count """
        peewee.Model.select = MagicMock()
        peewee.Model.select().where = MagicMock()
        peewee.Model.select().where().count = MagicMock(return_value=3)

        count = BaseOps.list_active_customers()
        self.assertEqual(3, count)


class TestCreateCustomerDb(MockDatabaseTest):
    """ Tests Create Customer DB module """

    def test_set_logging(self):
        """ Validates logging setup """
        with self.assertLogs() as mock_logger:
            CreateDb.set_logging(0)

            msg = "INFO:root:Logging set at level: INFO"
            self.assertIn(msg, mock_logger.output)

    def test_parse_log_level(self):
        """ Validates parsing log levels """
        levels = {0: logging.INFO, 1: logging.ERROR, 2: logging.DEBUG}
        for key, value in levels.items():
            self.assertEqual(value, CreateDb.parse_log_level(key))

    def test_parse_log_level_error(self):
        """ Validates value error thrown on unexpected log level """
        with self.assertRaises(ValueError):
            CreateDb.parse_log_level("stuff")

    def test_init_database(self):
        """ Validates initializing the database """
        with self.assertLogs() as mock_logger:
            with patch("create_customers_db.SqliteDatabase") as db_helper:
                db_helper.connect = MagicMock()
                db_helper.execute_sql = MagicMock()

                test_db = CreateDb.init_database()
                self.assertEqual(str(type(db_helper)), str(type(test_db)))

                msg = "INFO:root:Database initialized successfully."
                self.assertIn(msg, mock_logger.output)

    def test_create_tables(self):
        """ Validates creating tables """
        with self.assertLogs() as mock_logger:
            with patch("create_customers_db.SqliteDatabase") as db_helper:
                db_helper.create_tables = MagicMock()

                CreateDb.create_tabels(db_helper)
                msg = "INFO:root:Tables created successfully."
                self.assertIn(msg, mock_logger.output)

    def test_import_customers(self):
        """ Validates importing customers """
        contents = str("1,2,3,4,5,6,active,2.01" +
                       "\n2,2,3,4,5,6,active,2.01" +
                       "\n3,2,3,4,5,6,active,2.01" +
                       "\n4,2,3,4,5,6,active,2.01" +
                       "\n5,2,3,4,5,6,active,2.01" +
                       "\n6,2,3,4,5,6,active,2.01")

        open_mock = mock.mock_open(read_data=contents)
        with patch("builtins.open", open_mock):
            with patch("itertools.islice"):
                db_module = "create_customers_db.Customers.get_or_create"
                with patch(db_module) as db_helper:

                    db_helper.return_value = [MockCustomer]

                    with self.assertLogs() as mock_logger:
                        CreateDb.import_customers("stuff", 3)
                        msg = "INFO:root:Customer written successfully."
                        self.assertIn(msg, mock_logger.output)

    def test_write_customer_errors(self):
        """ Validates errors on writing customers to the DB """
        db_module = "create_customers_db.Customers.get_or_create"
        with patch(db_module) as db_helper:
            db_helper.side_effect = [peewee.IntegrityError("integrity"),
                                     peewee.OperationalError("operational")]

            customer_list = ["1,2,3,4,5,6,active,2.01",
                             "2,3,4,5,6,7,active,2.01"]

            with self.assertLogs() as mock_logger:
                CreateDb.write_customers(customer_list)
                msg = "ERROR:root:integrity"
                self.assertIn(msg, mock_logger.output)

                msg = "ERROR:root:operational"
                self.assertIn(msg, mock_logger.output)

    def test_main(self):
        """ Validates main method """
        contents = str("1,2,3,4,5,6,active,2.01" +
                       "\n2,2,3,4,5,6,active,2.01" +
                       "\n3,2,3,4,5,6,active,2.01" +
                       "\n4,2,3,4,5,6,active,2.01" +
                       "\n5,2,3,4,5,6,active,2.01" +
                       "\n6,2,3,4,5,6,active,2.01")
        db_module = "create_customers_db.SqliteDatabase"
        cust_module = "create_customers_db.Customers.get_or_create"
        args = FakeArgs()

        open_mock = mock.mock_open(read_data=contents)
        with patch("builtins.open", open_mock):
            with patch(db_module) as db_helper:
                db_helper.connect = MagicMock()
                db_helper.execute_sql = MagicMock()
                db_helper.create_tabels = MagicMock()

                with patch(cust_module) as cust_helper:
                    cust_helper.side_effect = [[MockCustomer],
                                               [MockCustomer],
                                               [MockCustomer],
                                               [MockCustomer],
                                               [MockCustomer],
                                               [MockCustomer]]
                    with self.assertLogs() as mock_logger:
                        CreateDb.main(args)

                        msg = "INFO:root:Database initialized successfully."
                        self.assertIn(msg, mock_logger.output)

                        msg = "INFO:root:Customer written successfully."
                        self.assertIn(msg, mock_logger.output)
