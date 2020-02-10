#!/usr/bin/env python3

"""
Returns total price paid for individual rentals
"""

import argparse
import json
import datetime
import math
import sys
import logging

# pylint: disable= W0621, C0103


def logger_setup(level):
    """A function to format the logging parameters"""

    log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
    log_file = datetime.datetime.now().strftime("%Y-%m-%d") + ".log"

    formatter = logging.Formatter(log_format)

    levels = {0: logging.CRITICAL, 1: logging.ERROR, 2: logging.WARNING,
              3: logging.INFO, 4: logging.DEBUG}
    log_level = levels.get(level)

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(log_level)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def parse_cmd_arguments():
    """A function to parse command arguements"""
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='debug level', required=False, type=int, default=0)

    return parser.parse_args()


def load_rentals_file(filename):
    """A function to load rentals files"""
    with open(filename) as file:
        try:
            data_json = json.load(file)
        except FileNotFoundError:
            logging.error('This file cannot be found: %s', filename)
            sys.exit(0)
    return data_json


def calculate_additional_fields(data):
    """A function to calculate additional fields and ensure data is working properly."""
    for value in data.values():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
        except ValueError:
            logging.warning('Rental start is invalid.')
            logging.debug('rental_start: %s', value['rental_start'])

        try:
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
        except ValueError:
            logging.warning('Rental end is invalid')
            logging.debug('rental_end: %s', value['rental_end'])

        value['total_days'] = (rental_end - rental_start).days
        if value['total_days'] < 0:
            logging.warning('Rental end data is before start date for: %s', value['product_code'])
        value['total_price'] = value['total_days'] * value['price_per_day']

        try:
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
        except ValueError:
            logging.warning('Could not calculate square root of total price.')
            continue

        try:
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except ValueError:
            logging.warning('Could not find unit cost, total price, and/or units rented')
            continue
        except ZeroDivisionError:
            logging.warning('Cannot divide by 0.')
            continue

    return data


def save_to_json(filename, data):
    """A function to save to json file format."""
    with open(filename, 'w') as file:
        json.dump(data, file)


if __name__ == "__main__":
    args = parse_cmd_arguments()
    logger_setup(args.debug)
    data_json = load_rentals_file(args.input)
    data_final = calculate_additional_fields(data_json)
    save_to_json(args.output, data_final)
