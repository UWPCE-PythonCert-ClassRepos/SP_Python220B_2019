
import csv
import os
from unittest import TestCase
from inventory import add_furniture, single_customer


class TestInventory(TestCase):

    def test_add_furniture(self):

        os.remove('space_items.csv')

        """tests add_furniture function"""

        add_furniture('space_items.csv', 'Star Lord', 'C100', 'saber', 25)
        add_furniture('space_items.csv', 'Thanos', 'DT100',
                      'infinity stone', 20)
        add_furniture('space_items.csv', 'Root Tree',
                      'AC100', 'fertilizer', 20)
        add_furniture('space_items.csv', 'Iron Man', 'R100',
                      'fuel', 30)

        with open('space_items.csv', 'r') as space_items:
            csv_reader = csv.reader(space_items)
            next(csv_reader)
            thanos_row = next(csv_reader)

        self.assertEqual(thanos_row, ['Thanos', 'DT100',
                         'infinity stone', '20'])

    def test_single_customer(self):

        os.remove('space_items.csv')

        """tests single_customer function """
        spider_man = single_customer('Peter Parker', 'space_items.csv')
        spider_man('test_items.csv')

        with open('space_items.csv', 'r') as space_items:
            csv_reader = csv.reader(space_items)
            spider_row = next(csv_reader)

        self.assertEqual(spider_row, ['Peter Parker', 'LR04',
                         'Leather Cape', '25'])

        with open('space_items.csv', 'r') as space_items:
            csv_reader = csv.reader(space_items)
            test_row = (next(reversed(list(csv_reader))))

        self.assertEqual(test_row, ['Peter Parker', 'BR02',
                         'Queen Mattress', '17'])
