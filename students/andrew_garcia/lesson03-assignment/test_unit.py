# Testing individual parts of basic_operations.py

"""" Testing individual functions of code """

from unittest import TestCase
import peewee as pw
import basic_operations as bo
import customer_model as cm


def setup():
    """ Setup for Database """
    database = cm.DATABASE
    database.drop_tables([cm.Customer])
    database.create_tables([cm.Customer])


class BasicOperationsTest(TestCase):
    """ Testing basic_operations.py """
    def test_add_customer(self):
        """ Testing Adding a New Customer """
        setup()
        bo.add_customer('1150', 'Mark', 'Rollins', '46 Hawthorne Lane, Great Falls, MT 59404',
                        '406-604-4060', 'rockinrollins@gmail.com', True, 575.00)

        bo.add_customer('5102', 'Parker', 'Phan', '8811 Kingston Road, Boynton Beach, FL 33435',
                        '786-115-5125', 'parkingphan@yahoo.com', True, 250.00)

        a_customer = cm.Customer.get(cm.Customer.customer_id == '1150')
        self.assertEqual(a_customer.customer_id, '1150')
        self.assertEqual(a_customer.customer_email, 'rockinrollins@gmail.com')
        self.assertEqual(a_customer.customer_status, True)

        a_customer2 = cm.Customer.get(cm.Customer.customer_id == '5102')
        self.assertEqual(a_customer2.customer_id, '5102')
        self.assertEqual(a_customer2.customer_lastname, 'Phan')
        self.assertEqual(a_customer2.customer_status, True)

    def test_list_active_customers(self):
        """ Testing listing active customers """
        setup()
        bo.add_customer('1150', 'Mark', 'Rollins', '46 Hawthorne Lane, Great Falls, MT 59404',
                        '406-604-4060', 'rockinrollins@gmail.com', True, 575.00)

        bo.add_customer('5102', 'Parker', 'Phan', '8811 Kingston Road, Boynton Beach, FL 33435',
                        '786-115-5125', 'parkingphan@yahoo.com', True, 250.00)

        bo.add_customer('3030', 'Joseph', 'Tribbiani', '43 Foster Avenue, New York, NY 10003',
                        '212-013-7564', 'joeytribbiani@gmail.com', False, 1000.00)

        self.assertEqual(bo.list_active_customers(), 2)

    def test_search_customer(self):
        """ Testing search function """
        setup()
        bo.add_customer('3030', 'Joseph', 'Tribbiani', '43 Foster Avenue, New York, NY 10003',
                        '212-013-7564', 'joeytribbiani@gmail.com', False, 1000.00)

        a_customer = bo.search_customer('3030')
        a_customer_dict = {'first_name': 'Joseph', 'last_name': 'Tribbiani',
                           'email_address': '43 Foster Avenue, New York, NY 10003',
                           'phone_number': '212-013-7564'}

        self.assertEqual(a_customer, a_customer_dict)

    def test_search_customer_fail(self):
        """ Testing failed search """
        setup()
        bo.add_customer('3030', 'Joseph', 'Tribbiani', '43 Foster Avenue, New York, NY 10003',
                        '212-013-7564', 'joeytribbiani@gmail.com', False, 1000.00)

        a_customer = bo.search_customer('1029')

        self.assertEqual(a_customer, {})

    def test_delete_customer(self):
        """ Testing deleting a customer """
        setup()
        bo.add_customer('1150', 'Mark', 'Rollins', '46 Hawthorne Lane, Great Falls, MT 59404',
                        '406-604-4060', 'rockinrollins@gmail.com', True, 575.00)

        bo.add_customer('5102', 'Parker', 'Phan', '8811 Kingston Road, Boynton Beach, FL 33435',
                        '786-115-5125', 'parkingphan@yahoo.com', True, 250.00)

        bo.add_customer('3030', 'Joseph', 'Tribbiani', '43 Foster Avenue, New York, NY 10003',
                        '212-013-7564', 'joeytribbiani@gmail.com', False, 1000.00)

        bo.delete_customer('5102')

        self.assertEqual(bo.search_customer('5102'), {})

    def test_delete_customer_fail(self):
        """ testing deleting a customer fail """
        setup()
        bo.add_customer('1150', 'Mark', 'Rollins', '46 Hawthorne Lane, Great Falls, MT 59404',
                        '406-604-4060', 'rockinrollins@gmail.com', True, 575.00)

        bo.add_customer('3030', 'Joseph', 'Tribbiani', '43 Foster Avenue, New York, NY 10003',
                        '212-013-7564', 'joeytribbiani@gmail.com', False, 1000.00)

        with self.assertRaises(pw.DoesNotExist):
            bo.delete_customer('5102')

    def test_update_customer(self):
        """ Testing updating customer """
        setup()
        bo.add_customer('1150', 'Mark', 'Rollins', '46 Hawthorne Lane, Great Falls, MT 59404',
                        '406-604-4060', 'rockinrollins@gmail.com', True, 575.00)

        bo.update_customer('1150', 175.75)
        a_customer = cm.Customer.get(cm.Customer.customer_id == '1150')

        self.assertEqual(a_customer.customer_credit, 175.75)

    def test_update_customer_fail(self):
        """ Testing updating a customer fail """
        setup()
        bo.add_customer('1150', 'Mark', 'Rollins', '46 Hawthorne Lane, Great Falls, MT 59404',
                        '406-604-4060', 'rockinrollins@gmail.com', True, 575.00)

        with self.assertRaises(ValueError):
            bo.update_customer('2050', 175.75)
