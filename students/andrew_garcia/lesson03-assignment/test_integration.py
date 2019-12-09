# Testing integration of basic_operations.py

""" Testings module interactions """

from unittest import TestCase
import basic_operations as bo
import customer_model as cm


class BasicOperationsTest(TestCase):
    """ Creating integration tests """
    def test_integration(self):
        """ Tests integration of modules """
        database = cm.DATABASE
        database.drop_tables([cm.Customer])
        database.create_tables([cm.Customer])

        bo.add_customer('1150', 'Mark', 'Rollins', '46 Hawthorne Lane, Great Falls, MT 59404',
                        '406-604-4060', 'rockinrollins@gmail.com', True, 575.00)

        bo.add_customer('5102', 'Parker', 'Phan', '8811 Kingston Road, Boynton Beach, FL 33435',
                        '786-115-5125', 'parkingphan@yahoo.com', True, 250.00)

        bo.update_customer('1150', 175.75)
        a_customer = cm.Customer.get(cm.Customer.customer_id == '1150')
        self.assertEqual(a_customer.customer_credit, 175.75)

        bo.add_customer('3030', 'Joseph', 'Tribbiani', '43 Foster Avenue, New York, NY 10003',
                        '212-013-7564', 'joeytribbiani@gmail.com', False, 1000.00)

        self.assertEqual(bo.list_active_customers(), 2)

        a_customer2 = bo.search_customer('3030')
        a_customer2_dict = {'first_name': 'Joseph', 'last_name': 'Tribbiani',
                            'email_address': '43 Foster Avenue, New York, NY 10003',
                            'phone_number': '212-013-7564'}

        self.assertEqual(a_customer2, a_customer2_dict)

        bo.delete_customer('3030')

        self.assertEqual(bo.search_customer('3030'), {})
