'''
Returns total price paid for individual rentals
'''
import argparse
import json
import datetime
import math
import logging

def logging_func(level):
    '''Function to determine logging level output.

    Debug: General comments, indicating where in the script flow we are.
    Should be shown on screen only (i.e., never saved to logfile).

    Warning: Used for missing elements in the source data that force a change
    in the flow. Shown on screen and on the log file.

    Error: Used for inconsistencies in the source data that will cause the script
    to crash or report incorrect results. Shown on screen and on the log file.'''

    #formatting and file name
    log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
    formatter = logging.Formatter(log_format)
    log_file = datetime.datetime.now().strftime('%Y-%m-%d')+'.log'
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    #Level 0 = No debug messages or log file
    if level == '0':
        logger.setLevel(logging.CRITICAL)

    #Level 1 = Only error messages
    if level == '1':
        logger.setLevel(logging.ERROR)
        console_handler.setLevel(logging.ERROR)
        file_handler.setLevel(logging.ERROR)

    #Level 2 = Error messages and warnings
    if level == '2':
        logger.setLevel(logging.WARNING)
        console_handler.setLevel(logging.WARNING)
        file_handler.setLevel(logging.WARNING)

    #Level 3 = Error messages, warnings and debug messages
    if level == '3':
        logger.setLevel(logging.DEBUG)
        console_handler.setLevel(logging.DEBUG)
        file_handler.setLevel(logging.WARNING)

#charges_calc functions
def parse_cmd_arguments():
    '''Setup for argparse'''
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='debug level (0, 1, 2, 3,)', required=True)

    return parser.parse_args()


def load_rentals_file(filename):
    '''loads in rental information'''
    with open(filename) as file:
        try:
            data = json.load(file)
        except FileNotFoundError:
            logging.error('%s not found', file)
            exit(0)

    return data

def calculate_additional_fields(data):
    '''takes rental information and calculates additional information'''
    for value in data.values():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
        except ValueError:
            logging.warning('Rental start date does not match %m/%d/%y format')
            continue
        try:
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
        except ValueError:
            logging.warning('Rental end date does not match %m/%d/%y format')
            continue
        value['total_days'] = (rental_end - rental_start).days
        #logging.debug('Customer has a %s day rental', value['total_days'])
        if value['total_days'] < 0:
            logging.error('0 or negative day rental')
        else:
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']

    return data

def save_to_json(filename, data):
    '''saves a new json rental info file'''
    with open(filename, 'w') as file:
        json.dump(data, file)

if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    logging_func(ARGS.debug)
    DATA = load_rentals_file(ARGS.input)
    logging.debug('Data file loaded.')
    DATA = calculate_additional_fields(DATA)
    logging.debug('Calculations completed.')
    save_to_json(ARGS.output, DATA)
    logging.debug('File saved.')
