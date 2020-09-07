"""test the good_perf module"""

# pylint: disable=E1111
# pylint: disable=import-error
# pylint: disable=W0614
# pylint: disable-msg=R0913
# pylint: disable-msg=too-many-locals
# pylint: disable=R0904
# pylint: disable=import-error

from unittest import TestCase
from unittest.mock import patch
import unittest.mock
import logging
import peewee as pw
import lesson6.good_perf as gp
import lesson6.generate_csv as gc


class GoodPerfUnitTests(TestCase):
    """unit testing good_perf"""

    def test_analyze(self):
        """test the analysis function"""

        pass

    def test_csv(self):
        """test the csv function"""

        pass

    def test_analyze_handler(self):
        """test the analyze handler function"""

        pass

    def test_contract_source_data(self):
        """test the analyze handler function"""

        pass

    @classmethod
    def test_exit_program(cls):
        """text exit program"""

        with patch('sys.exit') as mock_exit_program:
            gp.exit_program()
            assert mock_exit_program.called
