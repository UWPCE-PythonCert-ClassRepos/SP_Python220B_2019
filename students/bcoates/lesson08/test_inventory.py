""" Tests functions in the inventory module """

from unittest import TestCase
from inventory import add_furniture, single_customer

class InventoryTests(TestCase):
    """ Define a class for testing inventory functions """

    def test_add_furniture(self):
        """ Tests adding furniture to the CSV file """

        expected_content = ['Elisa Miles,LR04,Leather Sofa,25\n',
                            'Edward Data,KT78,Kitchen Table,10\n',
                            'Alex Gonzales,BR02,Queen Mattress,17\n']

        add_furniture("rented_items.csv", "Elisa Miles", "LR04", "Leather Sofa", 25)
        add_furniture("rented_items.csv", "Edward Data", "KT78", "Kitchen Table", 10)
        add_furniture("rented_items.csv", "Alex Gonzales", "BR02", "Queen Mattress", 17)

        with open("rented_items.csv", "r") as csv_file:
            content = csv_file.readlines()

        self.assertEqual(expected_content, content)


    def test_single_customer(self):
        """ Tests importing items from a CSV for a single user """

        expected_content = ['Elisa Miles,LR04,Leather Sofa,25\n',
                            'Edward Data,KT78,Kitchen Table,10\n',
                            'Alex Gonzales,BR02,Queen Mattress,17\n',
                            'Susan Wong,LR04,Leather Sofa,25.00\n',
                            'Susan Wong,KT78,Kitchen Table,10.00\n',
                            'Susan Wong,BR02,Queen Mattress,17.00\n']

        create_invoice = single_customer("Susan Wong", "rented_items.csv")
        create_invoice("test_items.csv")

        with open("rented_items.csv", "r") as csv_file:
            content = csv_file.readlines()

        self.assertEqual(expected_content, content)
        