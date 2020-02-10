# Advanced Programming in Python -- Lesson 2 Assignment 1
# Jason Virtue
# Start Date 2/7/2020

'''
Returns total price paid for individual rentals
'''

import argparse
import json
import datetime
import math
import logging

'''
There are two bugs in the program when reading in the data file
    1. Some rental items have not been returned so their end date are before the start date
    This causes the total_days of a rental to be negative.
    2. Some rental items have missing values for end_date.

The fixes for these issues are as follows;
    1. The sqr_root_total_price can not square a negative value.  The program throws an error
    and went into the exception section of the function.  The first version of the program would return
    a system error code of 0 and abort the program without any error codes.
    2. The rental_end contains missing values and needed to handle this exception similar to #1
'''

def parse_cmd_arguments():
    """Reads parameters from command line
       Command line   python -m charges_calc --input source.json --output out.json
       -i = input file
       -o = output file
       -d = debugging Level
    """
    parser = argparse.ArgumentParser(description='Process data')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='Debugging level', required=False, default='0')
    logging.info("End to parsing arguments from command line")
    return parser.parse_args()

def init_logger(logger_level):
    '''Function to Initialize logger'''

    log_format = '%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s'
    log_file = 'charges_calc_'+datetime.datetime.now().strftime('%Y-%m-%d')+'.log'

    formatter = logging.Formatter(log_format)

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    if logger_level == '0':
        logger.setLevel(logging.CRITICAL)
        console_handler.setLevel(logging.CRITICAL)
        file_handler.setLevel(logging.CRITICAL)

    if logger_level == '1':
        logger.setLevel(logging.ERROR)
        console_handler.setLevel(logging.ERROR)
        file_handler.setLevel(logging.ERROR)

    if logger_level == '2':
        logger.setLevel(logging.WARNING)
        console_handler.setLevel(logging.WARNING)
        file_handler.setLevel(logging.WARNING)

    if logger_level == '3':
        logger.setLevel(logging.DEBUG)
        console_handler.setLevel(logging.DEBUG)
        file_handler.setLevel(logging.DEBUG)

def load_rentals_file(filename):
    """Function reads data file as input"""
    with open(filename) as file:
        try:
            data = json.load(file)
        except:
            logging.error('Input argument not found in command line')
            logging.debug('Missing input file from command line')
            logging.debug('Program exits with error due to no input argument')
            exit(0)
    logging.info("End to loading data file into program")
    return data

def calculate_additional_fields(data):
    """Fuction reads data file and dervives new fields"""
    for value in data.values():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            if rental_end < rental_start:
                logging.warning("rental_end is a date before rental_start")
                continue
            value['total_days'] = (rental_end - rental_start).days
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except:
            logging.debug("Exception logged for %s", str(value))
    logging.info("End to derviving new fields from data file")
    return data

def save_to_json(filename, data):
    """Method writes data files out to main directory"""
    with open(filename, 'w') as file:
        try:
            json.dump(data, file)
        except:
            logging.error('Output file not found in main directory')
            logging.debug('Missing output file from command line')
            logging.debug('Program exits with error due to no output argument')
            exit(0)
    logging.info("End to saving file to main directory")

if __name__ == "__main__":
    args = parse_cmd_arguments()
    init_logger(args.debug)
    logging.info("Start to load data file into program")
    data = load_rentals_file(args.input)
    logging.info("Start to dervive new fields from data file")
    data = calculate_additional_fields(data)
    logging.info("Start to save file to main directory")
    save_to_json(args.output, data)
    logging.error("*************************ENDOFPROGRAM*******************")
