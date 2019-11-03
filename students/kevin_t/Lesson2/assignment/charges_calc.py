"""
Returns total price paid for individual rentals
"""
import sys
import argparse
import json
import datetime
import math
import logging

def setup_logger(level):
    """ Sets up logger according to user determined level """
    log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
    log_file = datetime.datetime.now().strftime("%Y-%m-%d")+'.log'

    formatter = logging.Formatter(log_format)

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    if level == '0':
        logger.setLevel(logging.CRITICAL)

    elif level == '1':
        logger.setLevel(logging.ERROR)
        file_handler.setLevel(logging.ERROR)
        console_handler.setLevel(logging.ERROR)

    elif level == '2':
        logger.setLevel(logging.WARNING)
        file_handler.setLevel(logging.WARNING)
        console_handler.setLevel(logging.WARNING)

    elif level == '3':
        logger.setLevel(logging.DEBUG)
        file_handler.setLevel(logging.DEBUG)
        console_handler.setLevel(logging.DEBUG)

    else:
        print('Please select a debug level of 0, 1, 2 or 3')
        sys.exit(0)


def parse_cmd_arguments():
    """ Parses user input into variables """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='output JSON file', required=True)
    parser.add_argument('-d', '--debug', help='set debug levels', required=False, default=3)
    return parser.parse_args()


def load_rentals_file(filename):
    """ Opens input file """
    with open(filename) as file:
        try:
            data = json.load(file)
        except IOError:
            sys.exit(0)
    return data

def calculate_additional_fields(data):
    """ Generate more information about the rental """
    for key, value in data.items():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
        except ValueError:
            logging.error('rental_start error %s', key)
        try:
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
        except ValueError:
            logging.error('rental_end error %s', key)
        try:
            value['total_days'] = (rental_end - rental_start).days
        except ValueError:
            logging.error('total_days calc error %s', key)
        try:
            value['total_price'] = value['total_days'] * value['price_per_day']
        except ValueError:
            logging.error('total_price calc error %s', key)
        try:
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
        except ValueError:
            logging.error('sqrt_total_price calc error %s', key)
        try:
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except ZeroDivisionError:
            logging.error('unit_cost calc error %s', key)

    return data

def save_to_json(filename, data):
    """ Save output data into file """
    with open(filename, 'w') as file:
        json.dump(data, file)

if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    setup_logger(ARGS.debug)
    DATA = load_rentals_file(ARGS.input)
    DATA = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, DATA)
