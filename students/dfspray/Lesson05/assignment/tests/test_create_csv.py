"""
This file will test the creation of csv files in create_csv.py
"""

import logging
import unittest
import os
import sys
sys.path.append('C:/Users/allth/OneDrive/Desktop/Python/Python220/SP_Python220B_2019/'
                'students/dfspray/Lesson05/src')
from src import create_csv

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = 'test_csv.log'
FORMATTER = logging.Formatter(LOG_FORMAT)
FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setLevel(logging.DEBUG)
FILE_HANDLER.setFormatter(FORMATTER)
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.setLevel(logging.DEBUG)

class TestCreateCSV(unittest.TestCase):
    """This class will contain the tests for create_csv.py"""
    def test_create_csv(self):
        """This method will test the successful creation of three csv files in a directory"""
        LOGGER.debug("Removing csv files")
        try:
            LOGGER.debug("Removing customer_data")
            os.remove("/Users/allth/OneDrive/Desktop/Python/Python220/SP_Python220B_2019/students/"
                      "dfspray/Lesson05/assignment/csvs/customer_data.csv")
            LOGGER.debug("Removing product_data")
            os.remove("/Users/allth/OneDrive/Desktop/Python/Python220/SP_Python220B_2019/students/"
                      "dfspray/Lesson05/assignment/csvs/product_data.csv")
            LOGGER.debug("Removing rentals_data")
            os.remove("/Users/allth/OneDrive/Desktop/Python/Python220/SP_Python220B_2019/students/"
                      "dfspray/Lesson05/assignment/csvs/rentals_data.csv")
            LOGGER.debug("Removing csvs directory")
            os.rmdir("/Users/allth/OneDrive/Desktop/Python/Python220/SP_Python220B_2019/students/"
                     "dfspray/Lesson05/assignment/csvs")
        except FileNotFoundError:
            LOGGER.warning("The files weren't originally generated")

        LOGGER.debug("Rewriting csvs")
        create_csv.write_csv()

        directory_location = "/Users/allth/OneDrive/Desktop/Python/Python220/SP_Python220B_2019\
/students/dfspray/Lesson05/assignment/csvs/"
        file_list = ["product_data.csv", "customer_data.csv", "rentals_data.csv"]
        for file in file_list:
            LOGGER.debug("Looking for: %s", directory_location + file)
            self.assertTrue(os.path.exists(directory_location+file))
