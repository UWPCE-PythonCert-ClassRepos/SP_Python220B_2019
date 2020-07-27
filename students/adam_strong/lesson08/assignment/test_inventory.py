#!/usr/bin/env python
""""
test_inventory.py
"""

from unittest import TestCase
import pathlib
from inventory import *

check_csv = ['Elisa Miles,LR04,Leather Sofa,25\r\n',
             'Edward Data,KT78,Kitchen Table,10\r\n',
             'Alex Gonzales,QM,Queen Mattress,17\r\n']

check_csv2 = ['Susan Wong,PD5X,Power Drill 5Xt,2\r\n',
              'Susan Wong,SLD2,Solar Lamp D2,3\r\n',
              'Susan Wong,SLEDX,Solar LED X50,5\r\n',
              'Susan Wong,COU,Blue Couch,10\r\n',
              'Susan Wong,SCRS,Screwdriver Set,1\r\n',
              'Susan Wong,CWD5,Cleanswell Drier,10\r\n',
              'Susan Wong,CWW1,Cleanswell Washer,12\r\n',
              'Susan Wong,CW8000,Cleanswell 8000,30\r\n']

check_csv3 = ['Elisa Miles,LR04,Leather Sofa,25\r\n',
              'Edward Data,KT78,Kitchen Table,10\r\n',
              'Alex Gonzales,QM,Queen Mattress,17\r\n',
              'Susan Wong,PD5X,Power Drill 5Xt,2\r\n',
              'Susan Wong,SLD2,Solar Lamp D2,3\r\n',
              'Susan Wong,SLEDX,Solar LED X50,5\r\n',
              'Susan Wong,COU,Blue Couch,10\r\n',
              'Susan Wong,SCRS,Screwdriver Set,1\r\n',
              'Susan Wong,CWD5,Cleanswell Drier,10\r\n',
              'Susan Wong,CWW1,Cleanswell Washer,12\r\n',
              'Susan Wong,CW8000,Cleanswell 8000,30\r\n']


class AddFurnitureTests(TestCase):
    '''Tests the add_furniture() functionality'''

    def test_add_furniture_creates_csv(self):
        '''Tests that a single call to this function creates an inventory csv'''
        add_furniture("test_temp.csv", "Elisa Miles", "LR04", "Leather Sofa", 25)
        testpth = pathlib.Path('./')
        testdest = testpth.absolute() / 'test_temp.csv'
        assert os.path.isfile(testdest) is True

    def test_add_multiple_entries(self):
        '''Tests that multiple calls to add_furniture() yield multiple rows in csv'''
        add_furniture("test_temp.csv", "Elisa Miles", "LR04", "Leather Sofa", 25)
        add_furniture("test_temp.csv", "Edward Data", "KT78", "Kitchen Table", 10)
        add_furniture("test_temp.csv", "Alex Gonzales", "QM", "Queen Mattress", 17)
        contents = read_csv('test_temp.csv')
        assert contents == check_csv

    def tearDown(self):
        '''Deletes a csv file'''
        delete_csv('test_temp.csv')


class SingleCustomerTests(TestCase):
    '''Tests the single_customer() functionality'''

    def test_single_customer_only(self):
        '''Tests use of the single_customer()'''
        create_invoice = single_customer("Susan Wong", "test_temp.csv")
        create_invoice("test_items.csv")
        contents = read_csv('test_temp.csv')
        assert contents == check_csv2

    def test_integration(self):
        '''Tests use of add_furniture() with single_customer()'''
        add_furniture("test_temp.csv", "Elisa Miles", "LR04", "Leather Sofa", 25)
        add_furniture("test_temp.csv", "Edward Data", "KT78", "Kitchen Table", 10)
        add_furniture("test_temp.csv", "Alex Gonzales", "QM", "Queen Mattress", 17)
        create_invoice = single_customer("Susan Wong", "test_temp.csv")
        create_invoice("test_items.csv")
        contents = read_csv('test_temp.csv')
        assert contents == check_csv3

    def tearDown(self):
        '''Deletes a csv file'''
        delete_csv('test_temp.csv')

class ErrorCatching(TestCase):
    '''Tests the FileNotFoundError'''

    def test_no_read_file(self):
        '''Tests the error output for read_csv()'''
        contents = read_csv('doesnotexist.csv')
        assert contents == 'The file slated to be read: "doesnotexist.csv" does not exist'

    def test_no_file_to_delete(self):
        '''Tests the error output for delete_csv()'''
        deletion = delete_csv('doesnotexist.csv')
        assert deletion == 'The file slated for removal: "doesnotexist.csv" doesnt exist'
