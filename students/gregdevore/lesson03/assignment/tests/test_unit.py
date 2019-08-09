import sys
# Add path to files
sys.path.append('/Users/gdevore21/Documents/Certificate Programs/Python/PYTHON220/SP_Python220B_2019/students/gregdevore/lesson03/assignment')

from customer_model import *
from unittest import TestCase

import basic_operations

class CustomerTests(TestCase):

    def test_customer_add(self):
        # Add customer to database
        basic_operations.add_customer('00001', 'Ron', 'Swanson',
        '123 Fake Street', '555-867-5309', 'ronswanson@pawnee.gov', 0, 10000)
        # Retrieve customer to all fields were added
        customer = Customer.get(Customer.id == '00001')
        self.assertEqual(customer.id,'00001')
        self.assertEqual(customer.firstname,'Ron')
        self.assertEqual(customer.lastname,'Swanson')
        self.assertEqual(customer.address,'123 Fake Street')
        self.assertEqual(customer.phone,'555-867-5309')
        self.assertEqual(customer.email,'ronswanson@pawnee.gov')
        self.assertEqual(customer.status,0)
        self.assertEqual(customer.credit_limit,10000)
