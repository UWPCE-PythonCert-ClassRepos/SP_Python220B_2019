"""
Returns total price paid for individual rentals
"""

import argparse
import json
import datetime
import math
import logging
import sys

LOG_FORMAT = '%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s'
LOG_FILE = '{}.log'.format(datetime.datetime.now().strftime('%Y-%m-%d'))
formatter = logging.Formatter(LOG_FORMAT)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

file_handler = logging.FileHandler(LOG_FILE)
file_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.addHandler(console_handler)
logger.addHandler(file_handler)

def set_logging_level(level):
    """
    Set logging level
        0: No debug messages or log file.
        1: Only error messages.
        2: Error messages and warnings.
        3: Error messages, warnings and debug messages.
    """
    if level == 0:
        console_handler.setLevel(logging.NOTSET)
        file_handler.setLevel(logging.NOTSET)
        logger.setLevel(logging.NOTSET)
        logging.disable()
    elif level == 1:
        console_handler.setLevel(logging.ERROR)
        file_handler.setLevel(logging.ERROR)
        logger.setLevel(logging.ERROR)
    elif level == 2:
        console_handler.setLevel(logging.WARNING)
        file_handler.setLevel(logging.WARNING)
        logger.setLevel(logging.WARNING)
    elif level == 3:
        console_handler.setLevel(logging.DEBUG)
        file_handler.setLevel(logging.INFO)
        logger.setLevel(logging.DEBUG)
    else:
        print('Please select a debug level: 0, 1, 2, or 3.')
        sys.exit(0)


def parse_cmd_arguments():
    """ parsing the command-line arguments """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='set debug level, defaul 0 - no debugging',
                        default=0, required=False)
    return parser.parse_args()

def load_rentals_file(filename):
    """ load json data file """
    with open(filename) as file:
        try:
            data = json.load(file)
        except FileNotFoundError as err:
            logging.error('%s', err)
            sys.exit(0)
    return data

def calculate_additional_fields(data):
    """ calculate fields """
    list_error_data = []

    for name, value in data.items():
        logging.info('Working on %s', name)
        product_code = value['product_code']

        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
        except ValueError as err:
            list_error_data.append(name)
            logging.error('Unsuported data format for rental_start. %s', err)
            logging.error('Removing %s from output.', name)

        try:
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
        except ValueError as err:
            list_error_data.append(name)
            logging.error('Unsuported data format for rental_start. %s', err)
            logging.error('Removing %s from output.', name)

        value['total_days'] = (rental_end - rental_start).days

        if int(value['total_days'] < 0):
            list_error_data.append(name)
            logging.error('total_days: %d for product_code: %s.', value['total_days'], product_code)
            logging.error('Removing %s from output.', name)
        else:
            logging.debug('total days: %s', value['total_days'])

            value['total_price'] = value['total_days'] * value['price_per_day']
            logging.debug('total_price: %d', value['total_price'])

            try:
                value['sqrt_total_price'] = math.sqrt(value['total_price'])
            except ValueError as err:
                list_error_data.append(name)
                logging.error('sqrt_total_price error: %s', value['total_price'])
                logging.error('Removing %s from output.', name)

            try:
                value['unit_cost'] = value['total_price'] / value['units_rented']
            except ZeroDivisionError as err:
                list_error_data.append(name)
                logging.error('units_rented error: %s', err)
                logging.error('Removing %s from output.', name)

    # remove data with error
    if len(list_error_data) > 0:
        for name in list_error_data:
            del data[name]
    return data

def save_to_json(filename, data):
    """ save json data file """
    with open(filename, 'w') as file:
        json.dump(data, file)
        logging.debug('File saved - %s', filename)

if __name__ == "__main__":
    args = parse_cmd_arguments()
    json_data = load_rentals_file(args.input)
    calc_data = calculate_additional_fields(json_data)
    save_to_json(args.output, calc_data)
