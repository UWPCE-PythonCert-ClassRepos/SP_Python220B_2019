"""
This file will test the methods in database.py for reading and writing to a mongoDB database
"""

import logging
import unittest
from src import database
from src.database import ImportData
from src import create_csv

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = 'test_database.log'
FORMATTER = logging.Formatter(LOG_FORMAT)
FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setLevel(logging.DEBUG)
FILE_HANDLER.setFormatter(FORMATTER)
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.setLevel(logging.DEBUG)

class TestDatabase(unittest.TestCase):
    """This class will contain all the tests for database.py"""

    def test_meta(self):
        """This method will test import of .csv files to the database"""
        create_csv.write_csv(100)
        setattr(ImportData, "unobstructive_timing_method", database.unobstructive_timing_method)
        test_class = ImportData()
        database.delete_database()
        raw = test_class.unobstructive_timing_method()
        actual = [[type(raw[0][0]), type(raw[0][0]), type(raw[0][0])],
                  [type(raw[0][0]), type(raw[0][0]), type(raw[0][0])],
                  [type(raw[0][0]), type(raw[0][0]), type(raw[0][0])],
                  [type(raw[0][0]), type(raw[0][0]), type(raw[0][0])],
                  [type(raw[0][0]), type(raw[0][0]), type(raw[0][0])],
                  [type(raw[0][0]), type(raw[0][0]), type(raw[0][0])]]

        expected = [[type('something'), type('something'), type('something')],
                    [type('something'), type('something'), type('something')],
                    [type('something'), type('something'), type('something')],
                    [type('something'), type('something'), type('something')],
                    [type('something'), type('something'), type('something')],
                    [type('something'), type('something'), type('something')]]

        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
