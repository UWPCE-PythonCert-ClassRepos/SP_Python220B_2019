"""
Returns total price paid for individual rentals.

Note that many of the dates in 'source' are backwards. They are logged as warnings and skipped in the output.
"""
# pylint: disable=line-too-long

import argparse
import json
import datetime
import math
import logging
import sys

LEVEL_DICT = {'0': logging.CRITICAL,
              '1': logging.ERROR,
              '2': logging.WARNING,
              '3': logging.DEBUG}


def log_build():
    """Add handlers and formatting to LOGGER object."""

    log_format = '%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s'

    formatter = logging.Formatter(log_format)

    log_file = datetime.datetime.now().strftime('%Y-%m-%d') + '.log'

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    log = logging.getLogger()
    log.addHandler(file_handler)
    log.addHandler(console_handler)

    return log



def parse_cmd_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='debug level 0-3', required=True)

    return parser.parse_args()


def load_rentals_file(filename):
    """Return DATA from JSON file at 'filename'."""
    try:
        with open(filename) as file:
            data = json.load(file)
    except FileNotFoundError:
        LOGGER.error('Source file %s not found.', filename)
        sys.exit()
    return data


def calculate_additional_fields(data):
    """From existing values in DATA 'd', generate additional fields."""
    for value in data.values():
        LOGGER.debug('Calculating additional fields for rental %s.', value)
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            value['total_days'] = (rental_end - rental_start).days
            if value['total_days'] < 1:
                LOGGER.warning('Rental %s has length less than 1 day.', value)
                continue
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            if value['units_rented'] == 0:
                LOGGER.warning('Rental %s had zero days assigned', value)
                continue
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except ValueError:
            LOGGER.error('Rental %s missing values', value)
            continue
        LOGGER.debug('Updated rental %s values:\n', value)
        for field in value.values():
            LOGGER.debug('%s:%s', field, [field])
    return data


def save_to_json(filename, data):
    """Save DATA 'd' to JSON file at 'filename'."""
    try:
        with open(filename, 'w') as file:
            json.dump(data, file)
    except IOError:
        LOGGER.error('Error writing DATA to JSON file.')
        sys.exit()


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    LOGGER = log_build()
    LOGGER.setLevel(LEVEL_DICT[ARGS.debug])

    LOGGER.debug('Args passed in:\n%s', ARGS)
    DATA = load_rentals_file(ARGS.input)
    LOGGER.debug('Loaded DATA:\n%s', DATA)
    DATA = calculate_additional_fields(DATA)

    save_to_json(ARGS.output, DATA)
