'''Returns total price paid for individual rentals.'''

import argparse
import json
import datetime
import math
import logging
import sys

# pylint: disable E1121: too-many-function-args

def parse_cmd_arguments():
    '''
    Parse command line arguments:
    -i Input file name.
    -o Output file name.
    -d Debug log level (default=0).
    '''
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)

    # Adds a debugging option to the program, disabled by default (0)
    parser.add_argument('-d', '--debug', type=int, default=0, choices=range(0, 4),
                        help='debug level (0-3)', required=False)

    return parser.parse_args()

def logging_setup(func):
    '''Decorator function for logging'''
    def enable_logging(level, *args, **kwargs):
        '''
        Enables logging using -d or --debug equal to options (0-3); default=0:
        0: No debug messages.
        1: Only error messages.
        2: Error messages and warnings.
        3: Error messages, warnings and debug messages.
        '''
        log_file = datetime.datetime.now().strftime("%Y-%m-%d")+'.log'
        log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"

        formatter = logging.Formatter(log_format)

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.WARNING)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)

        logger = logging.getLogger()

        if level == 1:
            logger.setLevel(logging.ERROR)
        elif level == 2:
            logger.setLevel(logging.WARNING)
        elif level == 3:
            logger.setLevel(logging.DEBUG)
        else:
            logger.disabled = True

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        return func(*args, **kwargs)
    return enable_logging

@logging_setup
def load_rentals_file(filename):
    '''Loads rental input (-o) filename.'''
    with open(filename) as file:
        try:
            data = json.load(file)
        except FileNotFoundError:
            logging.error('%s not found', file)
            sys.exit(0)

    return data

@logging_setup
def calculate_additional_fields(data):
    '''
    Calculates the prices for each rental from the input file:
     total_days: Total number of days the item was rented.
     total_price: Total price of the rental for the total_days.
     sqrt_total_price: Square root of the total_price.
     unit_cost: Cost of each rental item.
    '''
    for value in data.values():
        try:
            # Help debugging by adding product code in the debugging log
            item = value['product_code']

            # Checks if rental_start date is missing and logs it
            # None were initially found but missing rental_end dates are an issue
            if not value['rental_start']:
                logging.warning('%s No rental_start date for: %s', item, value)
                continue
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            logging.debug('%s rental_start date  : %s', item, rental_start)

            # Checks if rental_end date is missing and logs it
            # Found rental_end dates missing
            if not value['rental_end']:
                logging.warning('%s No rental_end date for: %s', item, value)
                continue
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            logging.debug('%s rental_end date    : %s', item, rental_end)

            # Checks if rental_end date is before rental_start date and logs it
            # Found rental_end dates earlier than the rental_start dates, creating a negative value
            if (rental_end - rental_start).days < 0:
                logging.error('%s rental end date is before the start date:'
                              ' start: %s end: %s', item, rental_start, rental_end)
                continue
            # Checks if total_days is zero
            # Found total_days = 0
            if (rental_end - rental_start).days == 0:
                logging.warning('%s total_days = 0: start: %s end: %s',
                                item, rental_start, rental_end)
                value['total_days'] = 1
            else:
                value['total_days'] = (rental_end - rental_start).days
            logging.debug('%s total_days are     : %s', item, value['total_days'])

            value['total_price'] = value['total_days'] * value['price_per_day']
            logging.debug('%s total_price is     : %s', item, value['total_price'])

            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            logging.debug('%s sqrt_total_price is: %s', item, value['sqrt_total_price'])

            value['unit_cost'] = value['total_price'] / value['units_rented']
            logging.debug('%s unit_cost is       : %s', item, value['unit_cost'])
        except ValueError:
            logging.error('Failure to process rental: %s', value)
            sys.exit(0)

    return data

def save_to_json(filename, data):
    '''Saves the data to the output (-o) filename.'''
    with open(filename, 'w') as file:
        json.dump(data, file)

if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    DATA = load_rentals_file(ARGS.debug, ARGS.input)
    DATA = calculate_additional_fields(ARGS.debug, DATA)
    save_to_json(ARGS.output, DATA)
