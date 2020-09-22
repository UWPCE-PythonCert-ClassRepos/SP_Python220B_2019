"""
Returns total price paid for individual rentals

Logging in this module can be enabled with an optional command line option:
"-d {0, 1, 2, 3}", where
  0: No debug messages or log file.
  1: Only error messages.
  2: Error messages and warnings.
  3: Error messages, warnings and debug messages.

The log messages are saved to a file whose file name has time stamp, e.g.,
<charges_calc_2020-08-04.log>. Only error and warning messages are saved to the
log file. Debug information are printed to the console in addition to error and
warning messages.
"""

import sys
import argparse
import json
import datetime
import math
import logging
import functools


def parse_cmd_arguments():
    """ Process command line options """
    parser = argparse.ArgumentParser(description='Rental Price Processing')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='output JSON file', required=True)
    parser.add_argument('-l', '--log', type=int, choices=[0, 1],
                        help='logging switch (0: turn off logging; 1: turn on logging)')

    return parser.parse_args()


def setup_logging():
    """ Configure logging functions """
    # Get the "root" logger.
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    log_file = 'charges_calc_' + datetime.datetime.now().strftime('%Y-%m-%d') + '.log'

    log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
    # Create a "formatter" using the format string
    formatter = logging.Formatter(log_format)

    # Create a log message handler that sends output to log_file
    file_handler = logging.FileHandler(log_file, mode='w')
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Create a log message handler that sends output to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


def set_logging(logging_switch):
    """ Turn on/off logging decorator """
    def decorator_set_logging(func):

        @functools.wraps(func)
        def wrapper_set_logging(*args, **kwargs):
            if logging_switch == 0:
                logging.disable(logging.CRITICAL)

            return func(*args, **kwargs)

        return wrapper_set_logging

    return decorator_set_logging


@set_logging(parse_cmd_arguments().log)
def load_rentals_file(filename):
    """ Read rental data from a JSON file """
    logging.getLogger(__name__).debug('Calling load_rentals_file(%s)', filename)

    with open(filename) as file:
        try:
            data = json.load(file)
        except FileNotFoundError:
            logging.error('File %s not found in load_rentals_file, filename')
            sys.exit()
    return data


@set_logging(parse_cmd_arguments().log)
def calculate_additional_fields(data):
    """ Calculate additional fields in the rental record """
    logger = logging.getLogger(__name__)
    logger.debug('Calling calculate_additional_fields(data)')

    # Changed the iterator to "key" instead of value because we want to identify
    # specific records that have errors.
    # If data is missing or inconsistent, skip that record
    for key in data:
        value = data[key]

        if value['rental_start'] == '':
            logger.warning('rental_start value is missing at %s, skip this record', key)
            # skip the incomplete data record
            continue
        rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')

        if value['rental_end'] == '':
            logger.warning('rental_end value is missing at %s, skip this record', key)
            # skip the incomplete data record
            continue
        rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')

        if rental_end < rental_start:
            logger.error('rental_end is before rental_start at %s, skip this record', key)
            # skip the wrong data record
            continue
        value['total_days'] = (rental_end - rental_start).days

        if value['price_per_day'] < 0:
            logger.error('price_per_day is negative at %s, skip this record', key)
            # skip the wrong data record
            continue
        value['total_price'] = value['total_days'] * value['price_per_day']

        value['sqrt_total_price'] = math.sqrt(value['total_price'])

        # since value['units_rented'] is in the denominator, check for zero
        if value['units_rented'] == 0:
            logger.error('units_rented is zero at %s, skip this record', key)
            # skip this record
            continue
        value['unit_cost'] = value['total_price'] / value['units_rented']

    return data


@set_logging(parse_cmd_arguments().log)
def save_to_json(filename, data):
    """ Write the modified rental data with additional fields to a file """
    logging.getLogger(__name__).debug('Calling save_to_json(%s, data)', filename)

    with open(filename, 'w') as file:
        json.dump(data, file)


if __name__ == "__main__":
    arguments = parse_cmd_arguments()
    setup_logging()
    rental_data = load_rentals_file(arguments.input)
    rental_data_processed = calculate_additional_fields(rental_data)
    save_to_json(arguments.output, rental_data_processed)
