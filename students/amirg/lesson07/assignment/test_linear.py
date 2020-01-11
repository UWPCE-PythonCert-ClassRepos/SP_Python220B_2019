"""
Tests the database module
"""
#pylint: disable=invalid-name
from unittest import TestCase
import linear

class LinearTests(TestCase):
    """
    Tests for the database module
    """


    def test_import_data(self):
        """
        Tests the import_data function
        """
        #directory_path = r"C:/Users/Amir G/SP_Python220B_2019/students/amirg/" \
        #                 r"lesson05/assignment/data"
        directory_path = r"data"

        linear.drop_data()
        list1 = linear.import_data(directory_path, 'products.csv',
                                   'customers.csv')
        self.assertEqual(list1[0][0], 999)
        self.assertEqual(list1[0][1], 0)
        self.assertEqual(list1[0][2], 999)
        self.assertTrue(list1[0][3] > 0)
        self.assertEqual(list1[1][0], 999)
        self.assertEqual(list1[1][1], 0)
        self.assertEqual(list1[1][2], 999)
        self.assertTrue(list1[1][3] > 0)

        linear.drop_data()
        list2 = linear.import_data(directory_path, 'products.csv',
                                   'nothing.csv')
        self.assertEqual(list2[0][0], 999)
        self.assertEqual(list2[0][1], 0)
        self.assertEqual(list2[0][2], 999)
        self.assertTrue(list2[0][3] > 0)
        self.assertEqual(len(list2), 1)
        