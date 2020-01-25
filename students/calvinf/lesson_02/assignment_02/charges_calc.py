'''
Returns total price paid for individual rentals
'''
import sys
import argparse
import json
import datetime
import math
import logging

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = datetime.datetime.now().strftime("%Y-%m-%d")+".log"
FORMATTER = logging.Formatter(LOG_FORMAT)

CONSOLE_HANDLER = logging.StreamHandler()
# Get the root logger
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)
CONSOLE_HANDLER.setFormatter(FORMATTER)


def setup_file_log(level):
    '''
    Method to set file logging level for the script.
    0: No debug messages or log file.
    1: Only error messages.
    2: Error messages and warnings.
    3: Error messages, warnings and debug messages.
    '''
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(level)
    file_handler.setFormatter(FORMATTER)
    LOGGER.addHandler(file_handler)


def setup_console_log(level):
    '''
    Method to set the Console logging level for the script.
    0: No debug messages or log file.
    1: Only error messages.
    2: Error messages and warnings.
    3: Error messages, warnings and debug messages.
    '''
    CONSOLE_HANDLER.setLevel(level)
    LOGGER.addHandler(CONSOLE_HANDLER)


def setup_logging_debug(mode):
    '''
    Method to set the logging level for the script.
    0: No debug messages or log file.
    1: Only error messages.
    2: Error messages and warnings.
    3: Error messages, warnings and debug messages.
    '''
    if mode == 3:
        setup_file_log(logging.WARNING)
        setup_console_log(logging.DEBUG)
    elif mode == 2:
        setup_file_log(logging.WARNING)
        setup_console_log(logging.WARNING)
    elif mode == 1:
        setup_file_log(logging.ERROR)
        setup_console_log(logging.ERROR)
    else:
        LOGGER.disabled = True


def parse_cmd_arguments():
    '''
    Parse the arguments passed into the script
    for file inputs and logging level.
    '''
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file',
                        required=True)
    parser.add_argument('-d', '--debug', help='Turn on debugging',
                        required=False, default=0, type=int)
    return parser.parse_args()


def load_rentals_file(filename):
    ''' Method to read in the file for processing '''
    try:
        logging.debug('Reading file: {}'.format(filename))
        with open(filename) as file:
            in_data = json.load(file)
    except FileNotFoundError:
        logging.error("File not found")
        sys.exit(1)
    return in_data


def calculate_additional_fields(data):
    ''' Calculates the input from the json file '''
    logging.debug('Starting calculations for additional fields')
    for value in data.values():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            # Warnig that value is missing
            if len(value['rental_end']) < 5:
                logging.warning(':Rental end date value is missing.')
            # time data '' does not match format '%m/%d/%y blank date
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            # time delta producing negative
            logging.debug('calculating total days:')
            value['total_days'] = abs((rental_end - rental_start).days)
            logging.debug('calculating total price:')
            value['total_price'] = value['total_days'] * value['price_per_day']
            # value error occurs when squaring negative number
            if value['total_price'] < 0:
                logging.warning('Total price is a negative number')
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            if value['units_rented'] == 0:
                logging.warning('Units rented value is zero')
                logging.debug('calculating unit cost:')
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except ZeroDivisionError:
            logging.error(":Dividing by zero to calculate unit cost")
        except ValueError:
            logging.error(":Value error -missing values")
    return data


def save_to_json(filename, data):
    ''' Writes the output to filesystem as a json file '''
    logging.debug('Starting save_to_json function')
    try:
        logging.debug('Writing to file: {}'.format(filename))
        with open(filename, 'w') as out_file:
            json.dump(data, out_file)
    except IOError:
        logging.error("Problems writing to file")
        sys.exit(1)


if __name__ == "__main__":
    args = parse_cmd_arguments()
    setup_logging_debug(args.debug)
    file_data = load_rentals_file(args.input)
    result_data = calculate_additional_fields(file_data)
    save_to_json(args.output, result_data)
