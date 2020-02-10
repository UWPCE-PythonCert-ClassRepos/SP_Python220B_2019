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

def error_counter():
    """ Error counter generator """
    cnt = 0
    while True:
        yield cnt
        cnt = cnt + 1

def import_product_csv(directory_name, product_file):
    """ Import Product CSV File
    Import Product CSV File from given path and filename and returns
    a dictionary of the data.

    Args:
        directory_name: Path where CSV file lives (from root directory)
        product_file: File name of product CSV file
    Returns:
        dict: Dictionary of product data from CSV
    """
    directory_name = Path('./'+directory_name)
    file_path = directory_name / product_file
    LOGGER.info("Importing Product CSV file: %s", file_path)
    product_dict = {}
    with open(file_path, "r") as csvfile:
        csv_data = csv.reader(csvfile, delimiter=',')
        
        for idx, row in enumerate(csv_data):
            print(row)
            if idx == 0:
                csv_header = row
            else:
                product_dict.update(_product_file_parser(csv_header, row))

def import_data(directory_name, product_file, customer_file, rentals_file):
    """ 
    Import Data From files

    This function imports the data from the files provided into the database. 

    Args:
        directory_name: Path where csv files live
        product_file: CSV file with product information (line 1 must be header!)
        customer_file: CSV file with customer information (line 1 must be header!)
        rentals_file: CSV file of rental information (line 1 must be header!)
    Returns:
        record_count: # of products, customers and rentals added (in that order)
        error_count: # of errors occured with product, customer and rental add (in that order)
    Raises:
        IOError: Invalid File provided
        IndexError: Mismatched data and header length in file
    """
    directory_name = Path(directory_name)
    record_count = [0, 0, 0]
    
    try:
        pass
        # with open(directory_name / product_file) as csvfile:
        #     csv_header = csv.reader(csvfile, delimiter=',')
    except IOError:
        LOGGER.error('Invalid product file name %s', product_file)
    except IndexError:
        LOGGER.error('Mismatched data and header length')
        LOGGER.error('Header: %s', csv_header)
        LOGGER.error('Data:%s', csv_data)
        


def _product_file_parser(header, p_data):
    """ Parse a line of the product file """
    if len(header) != len(p_data):
        raise IndexError('Data is not the same length as header')
    d_vals = dict(zip(header,p_data))
    LOGGER.info('Created file data: %s', d_vals)
    return d_vals