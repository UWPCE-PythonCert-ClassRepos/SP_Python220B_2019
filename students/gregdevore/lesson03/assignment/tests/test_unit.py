import sys
# Add path to files
sys.path.append('/Users/gdevore21/Documents/Certificate Programs/Python/PYTHON220/SP_Python220B_2019/students/gregdevore/lesson03/assignment')

from customer_model import *
from unittest import TestCase

import basic_operations

class CustomerTests(TestCase):

    def test_customer_add(self):
        new_customer = {'id':'00001', 'firstname':'Ron', 'lastname':'Swanson',
        'address':'123 Fake Street', 'phone':'555-867-5309',
        'email':'ronswanson@pawnee.gov', 'status':0, 'credit_limit':10000}
        # Add customer to database
        basic_operations.add_customer(new_customer['id'], new_customer['firstname'],
        new_customer['lastname'], new_customer['address'], new_customer['phone'],
        new_customer['email'], new_customer['status'], new_customer['credit_limit'])
        # Retrieve customer to all fields were added
        customer = Customer.get(Customer.id == new_customer['id'])
        self.assertEqual(customer.id,new_customer['id'])
        self.assertEqual(customer.firstname,new_customer['firstname'])
        self.assertEqual(customer.lastname,new_customer['lastname'])
        self.assertEqual(customer.address,new_customer['address'])
        self.assertEqual(customer.phone,new_customer['phone'])
        self.assertEqual(customer.email,new_customer['email'])
        self.assertEqual(customer.status,new_customer['status'])
        self.assertEqual(customer.credit_limit,new_customer['credit_limit'])
