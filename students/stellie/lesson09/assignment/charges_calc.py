# Stella Kim
# Assignment 9: Advanced Language Constructs

"""Returns total price paid for individual rentals using Decorators"""

import argparse
import json
import datetime
import math
import logging
import sys


# Format logs
LOG_FORMAT = '%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s'
LOG_FILE = datetime.datetime.now().strftime('%Y-%m-%d') + '.charges_calc.log'

# Setup logging format
FORMATTER = logging.Formatter(LOG_FORMAT)

# Setup handlers
FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setFormatter(FORMATTER)
CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setFormatter(FORMATTER)

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)


def logging_decorator(func):
    """Logging Decorator"""

    def logging_handler(level, *args):
        """
        Setup logging with the following debug level requirements:
        # 0: No debug messages or log file.
        # 1: Only error messages.
        # 2: Error messages and warnings.
        # 3: Error messages, warnings and debug messages.

        Debug level should contain general comments, warnings display missing
        elements and errors are shown for inconsistencies in source data.
        """

        log_levels = {0: logging.NOTSET, 1: logging.ERROR, 2: logging.WARNING,
                      3: logging.DEBUG}
        try:
            if level == 0:
                LOGGER.disabled = True
            else:
                LOGGER.setLevel(log_levels[level])
        except KeyError:
            print('Debugging level is invalid.  Level must be between 0-3.')
            sys.exit()

        LOGGER.addHandler(FILE_HANDLER)
        LOGGER.addHandler(CONSOLE_HANDLER)

        result = func(*args)
        return result

    return logging_handler


def parse_cmd_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file',
                        required=True)
    parser.add_argument('-d', '--debug', help='debug levels 0-3', default=0,
                        type=int, required=False)

    return parser.parse_args()


@logging_decorator
def load_rentals_file(filename):
    """Load source data file"""
    with open(filename) as file:
        try:
            data = json.load(file)
            logging.debug('File %s has loaded successfully.\n', filename)
        except FileNotFoundError:
            logging.error('File %s not found.\n', filename)
            sys.exit()
    return data


@logging_decorator
def calculate_additional_fields(data):
    """Calculate additional values based on data file values"""
    for value in data.values():
        # Log each item in source data
        logging.debug('Calculate additional fields for data item: %s',
                      value['product_code'])
        try:
            if not value['rental_start']:  # no date present
                logging.warning('No rental_start value to convert %s to '
                                'datetime.\n', value['product_code'])
                continue

            if not value['rental_end']:  # no date present
                logging.warning('No rental_end value to convert %s to '
                                'datetime.\n', value['product_code'])
                continue

            rental_start = datetime.datetime.strptime(value['rental_start'],
                                                      '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'],
                                                    '%m/%d/%y')

            if rental_start > rental_end:  # dates are reversed in source data
                logging.error('Rental end date is listed incorrectly as '
                              'before rental start date for item: %s.\n'
                              'Rental_start: %s\nRental_end: %s',
                              value['product_code'], value['rental_start'],
                              value['rental_end'])
            # Choose to take rental diff assuming user error in source data
            value['total_days'] = abs(rental_end - rental_start).days
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])

            if value['units_rented'] > 0:  # no units rented
                value['unit_cost'] = value['total_price'] /\
                                     value['units_rented']
            else:
                logging.warning('No units were rented for item: %s.\n',
                                value['product_code'])
                continue

            logging.debug('Item: %s has successfully processed.\n', value)
        except ValueError:
            logging.error('Failed to process item: %s.\n', value)
            sys.exit()

    return data


def save_to_json(filename, data):
    """Save additional data to file"""
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
        logging.debug('Data output file: %s has been created.\n', filename)


if __name__ == '__main__':
    ARGS = parse_cmd_arguments()
    LEVEL = ARGS.debug
    DATA = load_rentals_file(LEVEL, ARGS.input)
    DATA = calculate_additional_fields(LEVEL, DATA)
    save_to_json(ARGS.output, DATA)
