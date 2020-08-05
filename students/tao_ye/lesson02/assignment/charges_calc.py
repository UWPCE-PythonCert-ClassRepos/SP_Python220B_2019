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


def parse_cmd_arguments():
    """
    Process command line options
    """
    parser = argparse.ArgumentParser(description='Rental Price Processing')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', type=int, choices=[0, 1, 2, 3],
                        help='debug level (0: no debug messages or log file; \
                                           1: only error messages; \
                                           2: error messages and warnings; \
                                           3: error messages, warnings and debug messages.)')

    return parser.parse_args()


def setup_logging(debug_level=0):
    """
    Configure logging functions
    """
    log_file = 'charges_calc_' + datetime.datetime.now().strftime('%Y-%m-%d') + '.log'

    log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
    # Create a "formatter" using the format string
    formatter = logging.Formatter(log_format)

    # Create a log message handler that sends output to log_file
    file_handler = logging.FileHandler(log_file, mode='w')
    file_handler.setLevel(logging.WARNING)
    # Set the formatter for this log message handler.
    file_handler.setFormatter(formatter)

    # Create a log message handler that sends output to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    # Get the "root" logger.
    logger = logging.getLogger()

    if debug_level == 1:
        logger.setLevel(logging.ERROR)
    elif debug_level == 2:
        logger.setLevel(logging.WARNING)
    elif debug_level == 3:
        logger.setLevel(logging.DEBUG)
    # Add file and console handler to the "root" logger.
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def load_rentals_file(filename):
    """
    Read rental data from a JSON file
    """
    logging.debug('Calling load_rentals_file(%s)', filename)

    with open(filename) as file:
        try:
            data = json.load(file)
        except FileNotFoundError:
            logging.error('File %s not found in load_rentals_file, filename')
            sys.exit()
    return data


def calculate_additional_fields(data):
    """
    Calculate additional fields in the rental record
    """
    logging.debug('Calling calculate_additional_fields(data)')

    # Changed the iterator to "key" instead of value because we want to identify
    # specific records that have errors.
    # If data is missing or inconsistent, skip that record
    for key in data:
        value = data[key]

        if value['rental_start'] == '':
            logging.warning('rental_start value is missing at %s, skip this record', key)
            # skip the incomplete data record
            continue
        rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')

        if value['rental_end'] == '':
            logging.warning('rental_end value is missing at %s, skip this record', key)
            # skip the incomplete data record
            continue
        rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')

        if rental_end < rental_start:
            logging.error('rental_end is before rental_start at %s, skip this record', key)
            # skip the wrong data record
            continue
        value['total_days'] = (rental_end - rental_start).days

        if value['price_per_day'] < 0:
            logging.error('price_per_day is negative at %s, skip this record', key)
            # skip the wrong data record
            continue
        value['total_price'] = value['total_days'] * value['price_per_day']

        value['sqrt_total_price'] = math.sqrt(value['total_price'])

        # since value['units_rented'] is in the denominator, check for zero
        if value['units_rented'] == 0:
            logging.error('units_rented is zero at %s, skip this record', key)
            # skip this record
            continue
        value['unit_cost'] = value['total_price'] / value['units_rented']

    return data


def save_to_json(filename, data):
    """
    Write the modified rental data with additional fields to a file
    """
    logging.debug('Calling save_to_json(%s, data)', filename)

    with open(filename, 'w') as file:
        json.dump(data, file)


if __name__ == "__main__":
    args = parse_cmd_arguments()
    if args.debug is not None and args.debug != 0:
        setup_logging(args.debug)
    else:
        logging.disable(logging.CRITICAL)
    rental_data = load_rentals_file(args.input)
    rental_data_processed = calculate_additional_fields(rental_data)
    save_to_json(args.output, rental_data_processed)
