"""
Test that ``good_perf.py`` provides the same results as ``poor_perf.py``.
"""

import unittest
import os
import datetime
import good_perf as good
import poor_perf as poor
from unittest import mock

DIR = os.path.dirname(os.path.realpath(__file__))
FILE = os.path.join(DIR, 'data', 'exercise.csv')

NOW = datetime.datetime.now()


class TestGoodBad(unittest.TestCase):
    """Test that good and bad performing code have same results."""

    @mock.patch('poor_perf.datetime')
    @mock.patch('good_perf.datetime')
    def test_analyze(self, datetime_good, datetime_poor):
        """Tests ``analyze``."""

        datetime_good.datetime.now.return_value = NOW
        datetime_poor.datetime.now.return_value = NOW

        with mock.patch("builtins.print") as mock_print:
            poor_res = poor.analyze(FILE)
            poor_print = mock_print.call_args_list

        with mock.patch("builtins.print") as mock_print:
            good_res = good.analyze(FILE)
            good_print = mock_print.call_args_list

        self.assertEqual(poor_print, good_print)
        self.assertEqual(poor_res, good_res)
