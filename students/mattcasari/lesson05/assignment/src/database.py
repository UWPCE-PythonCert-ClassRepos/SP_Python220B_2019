"""Lesson 05: HP Norton MongoDB"""

# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=too-many-arguments
# pylint: disable=broad-except

import pymongo
import csv
import logging
from pathlib import Path

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = "db.log"
FORMATTER = logging.Formatter(LOG_FORMAT)

FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setFormatter(FORMATTER)
FILE_HANDLER.setLevel(logging.INFO)

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setFormatter(FORMATTER)
CONSOLE_HANDLER.setLevel(logging.DEBUG)

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLE_HANDLER)



def import_data(directory_name, product_file, customer_file, rentals_file):
    directory_name = Path(directory_name)
    try:
        with open(directory_name / product_file) as csvfile:
            csv_header = csv.reader(csvfile, delimiter=',')
    except IOError:
        LOGGER.error('Invalid product file name %s', product_file)
        raise IOError('Invalid product file name %s', product_file)


def _product_file_parser(header, p_data):
    """ Parse a line of the product file """
    d_vals = dict(zip(header,p_data))
    LOGGER.info('Created file data: %s', d_vals)
    return d_vals