'''
Unit tests
'''


import sys
# Add path to files
sys.path.append('/home/ejgrandeo/uwpython/SP_Python220B_2019/students/eric_grandeo/lesson03')



from unittest import TestCase
from customers_model import Customers, database
#import basic_operations

#importing errors again
class TestBasicOperations(TestCase):
    def test_create_db(self):
        database.create_tables([Customers])


        
    
