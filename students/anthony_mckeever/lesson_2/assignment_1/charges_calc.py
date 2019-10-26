# Advanced Programming In Python - Lesson 2 Assigmnet 1: Automated Testing
# RedMine Issue - SchoolOps-12
# Code Poet: Anthony McKeever
# Start Date: 10/24/2019
# End Date: 10/25/2019

'''
Returns total price paid for individual rentals
'''

import argparse
import datetime
import json
import logging
import math
import sys

from argparse import RawTextHelpFormatter


def parse_cmd_arguments():
    """ Return arguments parsed from argparse """
    debug_help = str('Sets the logging level.' +
                     '\nAccepted values:'
                     '\n\t0 - None (default)' +
                     '\n\t1 - errors only' +
                     '\n\t2 - errors and warnings,' +
                     '\n\t3 - errors, warnings and debug messages')

    parser = argparse.ArgumentParser(description='Process some integers.',
                                     formatter_class=RawTextHelpFormatter)
    parser.add_argument('-i', '--input',
                        help='input JSON file', required=True)
    parser.add_argument('-o', '--output',
                        help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', type=int, default=0, help=debug_help)

    return parser.parse_args()


def set_logging(level):
    """
    Setup logging based on the level provided in arguments.

    :level: The level of logging to use.
    """
    log_level = parse_log_level(level)

    if log_level == logging.NOTSET:
        logging.disable()
        return

    log_file = datetime.datetime.now().strftime("%Y-%m-%d")+'.log'
    formatter = str("%(asctime)s %(filename)s:%(lineno)-3d " +
                    "%(levelname)s %(message)s")
    log_format = logging.Formatter(formatter)

    file_handler = get_handler(logging.FileHandler, log_level,
                               log_format, log_file)
    console_handler = get_handler(logging.StreamHandler, log_level, log_format)

    logger = logging.getLogger()
    logger.setLevel(log_level)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def get_handler(handler, log_level, formatter, file=None):
    """
    Return  a logging handler.

    :handler:       The handler type to create.
    :log_level:     The logging level to set.
    :formatter:     The formatter for the logging.
    :file:          The file name for the logging (default=None)
    """
    return_handler = handler(file)
    return_handler.setLevel(log_level)
    return_handler.setFormatter(formatter)
    return return_handler


def parse_log_level(level):
    """
    Parses the logging level from the debug integer as set in the arguments.

    :level: The logging level to parse.
    """
    log_levels = {0: logging.NOTSET,
                  1: logging.ERROR,
                  2: logging.WARNING,
                  3: logging.DEBUG}

    log_level = log_levels.get(level)

    if log_level is None:
        raise ValueError(f"Logging level {level} has no implementation.")

    return log_level


def load_rentals_file(filename):
    """
    Read a JSON file with rental settings.

    :filename:  The file to parse.
    """
    logging.info("Enter load_rentals_file")

    try:
        with open(filename) as file:
            data = json.load(file)

    except OSError as os_error:
        logging.error(os_error)
        logging.debug("Unable to load file: %s", filename)
        sys.exit(1)  # Exit with code to tell OS a problem occured.

    logging.debug("%s loaded successfully", filename)
    logging.info("Exit load_rentals_file")
    return data


def calculate_additional_fields(data):
    """
    Calculates additional values and appends them to the data.
    Additional Fields added:
        total_days: Calculated from rental_end - rental_start
        total_price: Calculated from total_days * price_per_day
        sqrt_total_price: Calculated from math.sqrt(total_price)
        unit_cost:  Calculated from total_price / units_rented

    :data:  The data to process.
    """
    logging.info("Enter calculate_additional_fields")

    for value in data.values():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'],
                                                      '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'],
                                                    '%m/%d/%y')

            if rental_end < rental_start:
                logging.warning("rental_end is a date before rental_start")
                logging.debug("Warning logged for %s.", str(value))
                logging.debug("This value was not processed.")
                continue

            value['total_days'] = (rental_end - rental_start).days
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except ValueError as value_error:
            logging.error(value_error)
            logging.debug("Exception logged for %s", str(value))

    logging.info("Exit calculate_additional_fields")
    return data


def save_to_json(filename, data):
    """
    Saves the data to a file.

    :filename:  The name of the file to write
    :data:      The data to write to the file.
    """
    logging.info("Enter save_to_json")

    try:
        with open(filename, 'w') as file:
            json.dump(data, file)

    except OSError as os_error:
        logging.error(os_error)
        logging.debug("Unable to save file: %s", filename)

        sys.exit(1)  # Exit with code to tell OS a problem occured.

    logging.debug("Data saved to %s successfully.", filename)
    logging.info("Exit save_to_json")


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    set_logging(ARGS.debug)

    DATA = load_rentals_file(ARGS.input)
    DATA = calculate_additional_fields(DATA)

    save_to_json(ARGS.output, DATA)
