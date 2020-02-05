""" Tests inventory.py """

from unittest import TestCase
from inventory import add_furniture, single_customer


class TestInventory(TestCase):
    """ Testing inventory.py"""
    def test_add_furniture(self):
        """ testing add_furniture """
        add_furniture('invoice_file.csv', 'Elisa Miles', 'LR04', 'Leather Sofa', 25.00)
        add_furniture('invoice_file.csv', 'Edward Data', 'KT78', 'Kitchen Table', 10.00)
        add_furniture('invoice_file.csv', 'Alex Gonzales', 'BR02', 'Queen Mattress', 17.00)

        with open('invoice_file.csv', 'r') as file:
            csv_contents = []
            for row in file:
                csv_contents.append(row)

        print(csv_contents)
        self.assertEqual(csv_contents[0], ('Elisa Miles,LR04,Leather Sofa,25.0\n'))
        self.assertEqual(csv_contents[1], ('Edward Data,KT78,Kitchen Table,10.0\n'))
        self.assertEqual(csv_contents[2], ('Alex Gonzales,BR02,Queen Mattress,17.0\n'))

    def test_single_customer(self):
        """ testing single_customer """
        customer = single_customer('Eliza Miles', 'Miles.csv')
        customer('invoice_file.csv')

        with open('Miles.csv', 'r') as file:
            csv_contents = []
            for row in file:
                csv_contents.append(row)

        expected = ['Eliza Miles,LR04,Leather Sofa,25.0\n',
                    'Eliza Miles,KT78,Kitchen Table,10.0\n',
                    'Eliza Miles,BR02,Queen Mattress,17.0\n']

        self.assertEqual(csv_contents, expected)
