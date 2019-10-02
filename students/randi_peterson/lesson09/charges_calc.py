"""
Returns total price paid for individual rentals
"""

import argparse
import json
import datetime
import math
import logging


def log_decorator(func):
    """Create decorator for log"""
    def make_logger(lvl, *args):
        """Creates logging for file"""
        log_format = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"
        log_file = datetime.datetime.now().strftime("%Y-%m-%d")+'.log'

        formatter = logging.Formatter(log_format)

    #   File handler set up
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)

    #   Console handler set up
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

    #   Get logger
        logger = logging.getLogger()
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    #   Select level based on user input

    #   Only critical messages
        if lvl == '0':
            #   Disable logging
            logger.disabled = True
            file_handler.disabled = True

    #   Error messages
        if lvl == '1':
            logger.setLevel(logging.ERROR)
            file_handler.setLevel(logging.ERROR)
            console_handler.setLevel(logging.ERROR)

    #   Error messages, warnings
        if lvl == '2':
            logger.setLevel(logging.WARNING)
            file_handler.setLevel(logging.WARNING)
            console_handler.setLevel(logging.WARNING)

    #   Error messages, warnings, debug messages
        if lvl == '3':
            logger.setLevel(logging.DEBUG)
            file_handler.setLevel(logging.DEBUG)
            console_handler.setLevel(logging.DEBUG)

        return func(*args)
    return make_logger


def parse_cmd_arguments():
    """Parses command arguments, debugger added"""
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='logging level', required=False, default='3')
    return parser.parse_args()


@log_decorator
def load_rentals_file(filename):
    """Loads rental files, unchanged from original provided code"""
    with open(filename) as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            exit(0)
    return data


@log_decorator
def calculate_additional_fields(data):
    """Calculates addition info with given data, modified for logging"""
    for key, value in data.items():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            try:
                rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
#           Capture if rental end column is entirely missing
            except KeyError:
                logging.warning("No rental_end key found for %s", key)

#       Capture the value error caused by no return date or other errors
        except ValueError:
            logging.error("Date format is incorrect for %s, maybe no return date", key)
            logging.debug("calculate_additional_fields function encountered a ValueError")
        try:
            value['total_days'] = (rental_end - rental_start).days
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']

#       Capture the value error caused by the start date being after the end date
        except ValueError:
            logging.debug("calculate_additional_fields function encountered a ValueError")
            logging.warning("Start date is later than end date for %s", key)
    return data


@log_decorator
def save_to_json(filename, data):
    """Saves to output file, unchanced"""
    try:
        with open(filename, 'w') as file:
            json.dump(data, file)

    except FileNotFoundError:
        logging.error("File was not saved due to File Not Found")

    except IOError:
        logging.error("File was not saved due to an input/output issue")


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    logging.debug('Logger is active')
    DATA_INPUT = load_rentals_file(ARGS.debug, ARGS.input)
    DATA_OUTPUT = calculate_additional_fields(ARGS.debug, DATA_INPUT)
    save_to_json(ARGS.debug, ARGS.output, DATA_OUTPUT)
    logging.debug('Data has been saved!')
