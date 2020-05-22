"""
Returns total price paid for individual rentals.

Note that many of the dates in 'source' are backwards.
They are logged as warnings and skipped in the output.
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


def parse_cmd_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='debug level 0-3', required=True)

    return parser.parse_args()


ARGS = parse_cmd_arguments()


def function_log(func):
    """Decorator"""
    def log_build(*args):
        """Add handlers and formatting to log object."""

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

        log.setLevel(LEVEL_DICT[ARGS.debug])

        return func(*args)
    return log_build


@function_log
def load_rentals_file(filename):
    """Return data from JSON file at 'filename'."""
    try:
        with open(filename) as file:
            data = json.load(file)
    except FileNotFoundError:
        logging.error('Source file %s not found.', filename)
        sys.exit()
    return data


@function_log
def calculate_additional_fields(data):
    """From existing values in data 'd', generate additional fields."""
    for value in data.values():
        logging.debug('Calculating additional fields for rental %s.', value)
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            value['total_days'] = (rental_end - rental_start).days
            if value['total_days'] < 1:
                logging.warning('Rental %s has length less than 1 day.', value)
                continue
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            if value['units_rented'] == 0:
                logging.warning('Rental %s had zero days assigned', value)
                continue
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except ValueError:
            logging.error('Rental %s missing values', value)
            continue
        logging.debug('Updated rental %s values:\n', value)
        for field in value.values():
            logging.debug('%s:%s', field, [field])
    return data


@function_log
def save_to_json(filename, data):
    """Save data 'd' to JSON file at 'filename'."""
    try:
        with open(filename, 'w') as file:
            json.dump(data, file)
    except IOError:
        logging.error('Error writing data to JSON file.')
        sys.exit()


@function_log
def main():
    """Main function call."""
    logging.debug('Args passed in:\n%s', ARGS)
    data = load_rentals_file(ARGS.input)
    logging.debug('Loaded data:\n%s', data)
    data = calculate_additional_fields(data)

    save_to_json(ARGS.output, data)

if __name__ == "__main__":
    main()
