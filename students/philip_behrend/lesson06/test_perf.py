""" This module tests the performance functions """

from unittest import TestCase
import datetime
import random
from expand_data import *
from good_perf import *
from poor_perf import *

class ExpandDataTests(TestCase):
    """ This class tests expand_data module """

    def test_read_csv(self):
        """Test read_csv"""
        expected = ['5df44a54-8cca-4928-bc53-caabb23cf329', '1', '2', '3', '4', '05/26/2015', '']
        result = read_csv('exercise.csv')
        self.assertEqual(expected, result[0])

    def test_invalid_read_csv(self):
        """Test invalid read csv"""
        self.assertRaises(FileNotFoundError, read_csv, 'exercise_null.csv')

    def test_gen_random_date(self):
        """Test gen random date"""
        result = gen_random_date(random.random(), start='1/1/2010', end='1/1/2019',
                                 dt_format='%m/%d/%Y')
        result_date = datetime.datetime.strptime(result, '%m/%d/%Y')
        self.assertIsInstance(result, str)
        self.assertGreaterEqual(result_date, datetime.datetime.strptime('1/1/2010', '%m/%d/%Y'))
        self.assertLessEqual(result_date, datetime.datetime.strptime('1/1/2019', '%m/%d/%Y'))

    def test_write_output(self):
        """Test write data"""
        test_data = [['5df44a54-8cca-4928-bc53-caabb23cf329', '1', '2',
                      '3', '4', '05/26/2015', ''],
                     ['bc337622-119c-445d-9282-e4b980201c03', '2',
                      '3', '4', '5', '08/02/2011', 'ao']]

        write_output(test_data, 'test_output.csv')
        result = read_csv('test_output.csv')
        self.assertEqual(result, test_data)

class PerformanceTests(TestCase):
    """Tests for good and poor performance"""

    def test_good_perf(self):
        """good perf test"""
        expected = (datetime.datetime(2019, 12, 17, 22, 23, 11, 889367),
                    datetime.datetime(2019, 12, 17, 22, 23, 17, 159832),
                    {'2013': 111276,
                     '2014': 111009,
                     '2015': 111327,
                     '2016': 111264,
                     '2017': 221476,
                     '2018': 0},
                    499619)
        result = analyze("exercise_out.csv")
        self.assertEqual(expected[2], result[2])
        self.assertEqual(expected[3], result[3])
