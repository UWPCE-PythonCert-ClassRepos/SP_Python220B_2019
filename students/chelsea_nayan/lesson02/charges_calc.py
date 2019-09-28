'''
Returns total price paid for individual rentals
'''


#pylint: disable=line-too-long

import argparse
import json
import datetime
import math
import logging

def init_logger(level):
    '''Set up logger and handler'''

    # Set up format for the logger and set up the level of log file name
    log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
    log_file = datetime.datetime.now().strftime("%Y-%m-%d") + ".log"

    # Create formatter
    formatter = logging.Formatter(log_format)

    # Set up deubugger levels
    level_options = {0: logging.CRITICAL,
                     1: logging.ERROR,
                     2: logging.WARNING,
                     3: logging.DEBUG}

    # Check if debugger level is valid
    try:
        log_level = level_options.get(int(level))
    except KeyError:
        print('Error: logging level is not invalid.')
        log_level = logging.CRITICAL

    # Set up a log message handler that outputs to another file
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(formatter)

    # Set up the colsole handler for log messages
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    # Set up root handler
    logger = logging.getLogger()
    logger.setLevel(log_level)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

def parse_cmd_arguments():
    '''Parse through arguments from console'''

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True) # source.json
    parser.add_argument('-o', '--output', help='output JSON file', required=True) # debugger_log.txt
    parser.add_argument('-d', '--debug', help='logging level', required=False, default='0') # set up logging level

    return parser.parse_args()

def load_rentals_file(filename):
    ''' Load rental file'''

    with open(filename) as file:
        try:
            data = json.load(file)
        except FileNotFoundError:
            logging.error('Unable to locate rental file: %s.', filename)
            exit(0)
    return data

def calculate_additional_fields(data):
    '''Loop through json data and calculate total days, total price, sq rt total price, and unit cost for each rental'''

    for value in data.values():

        # Check if rental_start is valid
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
        except ValueError:
            logging.warning('rental_start entry, %s, is invalid.', rental_start)
            logging.debug('rental_start: %s', value.get('rental_start'))

        # Check if rental_end if valid
        try:
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
        except ValueError:
            logging.warning('rental_end entry, %s, is invalid', rental_end)
            logging.debug('rental_end %s', value.get('rental_end'))

        total_day = (rental_end - rental_start).days

        # Check if rent duration (total_day) is valid
        if total_day < 0:
            logging.warning('The rental end date is before the rental start date.')
            logging.debug('rental_start: %s, rental_end: %s', rental_start, rental_end)

        value['total_days'] = total_day
        value['total_price'] = value['total_days'] * value['price_per_day']

        # Check if something else is wrong
        try:
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except ValueError:
            logging.warning('Something wrong with rental_start or rental_end, skipped and continued.')
            continue
        except ZeroDivisionError:
            logging.warning('Cannot divide by 0, skipped and continued.')
            continue

    return data

def save_to_json(filename, data):
    '''Write to json output file'''
    with open(filename, 'w') as file:
        json.dump(data, file)

if __name__ == "__main__":
    args = parse_cmd_arguments()
    init_logger(args.debug) # Turn on debugger
    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)
