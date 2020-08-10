'''
doesnt work when i put it in the subfolder 'tests''

if i indent the 'customers' dicts under def setup they dont get recognized
in the lower down methods, something to do with 'self'

the db gets created without being explicitly told to do so
'''
from basic_opps_dict2 import (delete_customer, add_customer, search_customer,
                             update_customer_credit, list_active_customers)
from peewee import *
from customer_model import db, Customer
from unittest import TestCase


class test_basic_opps_dict(TestCase):
    '''sdsdf'''

    def setup(self):
        '''sdfdsf'''
        db.drop_tables([Customer])
        db.create_tables([Customer])
        # self.database.close()
        # Customer.drop_table()
        # Customer.create_table()
    customer2 = {
        '_name': 'Gangsta',
        '_last_name': 'Gibbs',
        '_home_address': '420 Fake Blvd',
        '_phone_number': '206-699-4200',
        '_email_address': 'ggibbs@washington.edu',
        '_status': True,
        '_poverty_score': 900}
    customer3 = {
        '_name': 'Skinny',
        '_last_name': 'Suge',
        '_home_address': '69 Fake Ave',
        '_phone_number': '206-690-4000',
        '_email_address': 'ssuge@washington.edu',
        '_status': True,
        '_poverty_score': 690}
    customer1 = {
        '_name': 'Freddie',
        '_last_name': 'Gibbs',
        '_home_address': '123 Fake St',
        '_phone_number': '206-360-4200',
        '_email_address': 'fgibbs@washington.edu',
        '_status': True,
        '_poverty_score': 420
        }

    def test_add_customer(self):
        add_customer(**self.customer1)
        check = Customer.get(Customer.name == 'Freddie')
        self.assertEqual(check.last_name, 'Gibbs')

    def test_del_customer(self):
        delete_customer('Freddie')
        after_delete = search_customer('Freddie')
        self.assertEqual(after_delete, {})

    def test_find_customer(self):
        add_customer(**self.customer2)
        search_customer('Gangsta')
        check = Customer.get(Customer.name == 'Gangsta')
        self.assertEqual(check.poverty_score, 900)

    def test_update_credit(self):
        add_customer(**self.customer3)
        update_customer_credit('Skinny', 100)
        check = Customer.get(Customer.name == 'Skinny')
        self.assertEqual(check.poverty_score, 100)
