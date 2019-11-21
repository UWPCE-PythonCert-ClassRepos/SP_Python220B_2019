"""Integration Testing"""

from unittest import TestCase
from codes import basic_operations
from codes.customer_model import Customer, DATABASE

class TestIntegration(TestCase):
    """Testing overall basic_operation"""

    def test_basic_operation(self):
        """Test basic operation"""

        DATABASE.drop_tables([Customer])
        DATABASE.create_tables([Customer])

        new_data = {'code':'A1', 'fname':'John', 'lname':'doe', 'address':'1004 ST SE', 
                    'phone':'206-555-1234', 'email':'johndoe@awesome.com', 'active':True,
                    'climit':7777}
        new_data2 = {'code':'A2', 'fname':'Sam', 'lname':'Wise', 'address':'315 Hampshire Dr.', 
                     'phone':'474-555-4477', 'email':'samwise@hobbits.com', 'active':True,
                     'climit':8888}

        for myinput in [new_data, new_data2]:
            basic_operations.add_customer(myinput['code'],
                                          myinput['fname'],
                                          myinput['lname'],
                                          myinput['address'],
                                          myinput['phone'],
                                          myinput['email'],
                                          myinput['active'],
                                          myinput['climit'])

        basic_operations.delete_customer(new_data["code"])

        active_customer = basic_operations.list_active_customers()
        self.assertEqual(active_customer, 1)
