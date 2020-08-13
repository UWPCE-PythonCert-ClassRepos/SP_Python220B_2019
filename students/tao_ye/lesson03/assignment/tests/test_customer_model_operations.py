from unittest import TestCase
import logging

import basic_operations as op
import customer_model as db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CUSTOMER_ID = 0
NAME = 1
LAST_NAME = 2
HOME_ADDRESS = 3
PHONE_NUMBER = 4
EMAIL_ADDRESS = 5
ACTIVE = 6
CREDIT_LIMIT = 7

customers = [('1', 'Albert Einstein', 'Einstein', '7 Vine Drive, Cleveland, TN 37312',
                   '559-555-0107', 'albert.einstein@gmail.com', True, 1000.00),
             ('2', 'Blaise Pascal', 'Pascal', '9834 Vernon Ave., Smyrna, GA 30080',
                   '404-555-0124', 'blaise.pascal@gmail.com', False, 600.00),
             ('3', 'Chien-Shiung Wu', 'Wu', '263 Orange Lane, Deerfield, IL 60015',
                   '630-555-0129', 'chien-shiung.wu@gmail.com', True, 1300.00),
             ('4', 'Enrico Fermi', 'Fermi', '468 Wilson St., Solon, OH 44139',
                   '567-555-0199', 'enrico.fermi@gmail.com', True, 2100.00),
             ('5', 'Jane Goodall', 'Goodall', '52 S. Summer St., Littleton, CO 80123',
                   '970-555-0171', 'jane.goodall@gmail.com', False, 1800.00)]

new_customer = ('6', 'Max Planck', 'Planck', '9175 E. Marvon St., Sunnyside, NY 11104',
                     '716-555-0195', 'max.planck@gmail.com', False, 2400.00)


class OperationsTests(TestCase):
    def setUp(self):
        """ test setup to populate the database table  """
        logger.info('setUp: create and populate the Customer table...')
        op.create_customer_table()
        self.assertTrue(db.Customer.table_exists())

        for customer in customers:
            with db.database.transaction():
                new_customer = db.Customer.create(
                    customer_id=customer[CUSTOMER_ID],
                    name=customer[NAME],
                    last_name=customer[LAST_NAME],
                    home_address=customer[HOME_ADDRESS],
                    phone_number=customer[PHONE_NUMBER],
                    email_address=customer[EMAIL_ADDRESS],
                    active=customer[ACTIVE],
                    credit_limit=customer[CREDIT_LIMIT])
                new_customer.save()

    def test_add_customer(self):
        """ test add_customer function """
        logger.info('Test add_customer')
        op.add_customer(new_customer[CUSTOMER_ID], new_customer[NAME], new_customer[LAST_NAME],
                        new_customer[HOME_ADDRESS], new_customer[PHONE_NUMBER],
                        new_customer[EMAIL_ADDRESS], new_customer[ACTIVE], new_customer[CREDIT_LIMIT])

        a_customer = db.Customer.get(db.Customer.customer_id == '6')
        db.database.close()

        self.assertEqual(a_customer.name, 'Max Planck')
        self.assertEqual(a_customer.last_name, 'Planck')
        self.assertEqual(a_customer.home_address, '9175 E. Marvon St., Sunnyside, NY 11104')
        self.assertEqual(a_customer.phone_number, '716-555-0195')
        self.assertEqual(a_customer.email_address, 'max.planck@gmail.com')
        self.assertTrue(not a_customer.active)
        self.assertEqual(a_customer.credit_limit, 2400.00)

        # Test exception: add an existing customer
        op.add_customer('1', new_customer[NAME], new_customer[LAST_NAME],
                        new_customer[HOME_ADDRESS], new_customer[PHONE_NUMBER],
                        new_customer[EMAIL_ADDRESS], new_customer[ACTIVE], new_customer[CREDIT_LIMIT])

    def test_search_customer(self):
        """ test search_customer function """
        logger.info('Test search_customer')
        customer_info = op.search_customer('5')

        self.assertEqual(customer_info['name'], 'Jane Goodall')
        self.assertEqual(customer_info['last name'], 'Goodall')
        self.assertEqual(customer_info['email address'], 'jane.goodall@gmail.com')
        self.assertEqual(customer_info['phone number'], '970-555-0171')

        # test exception
        customer_info = op.search_customer('50')

    def test_delete_customer(self):
        """ test delete_customer function """
        logger.info('Test delete_customer')
        op.delete_customer('4')

        names = []
        for customer in db.Customer:
            names.append(customer.name)

        self.assertTrue('Enrico Fermi' not in names)

        # Test customer not found exception
        op.delete_customer('40')

        db.database.close()

    def test_update_customer_credit(self):
        """ test update_customer_credit function """
        logger.info('Test update_customer_credit')
        op.update_customer_credit('1', 2000)
        a_customer = db.Customer.get(db.Customer.customer_id == '1')
        self.assertEqual(a_customer.credit_limit, 2000)

        # Test customer not found exception
        op.update_customer_credit('100', 2000)

        db.database.close()

    def test_list_active_customers(self):
        """ test list_active_customers function """
        logger.info('Test list_active_customers')
        self.assertEqual(op.list_active_customers(), 3)

    def tearDown(self):
        """ clean up the test setup """
        logger.info('tearDown: empty the table')
        for customer in db.Customer:
            customer.delete_instance()