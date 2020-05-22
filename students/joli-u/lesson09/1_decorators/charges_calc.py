'''
charges_calc.py
Assignment 9
Joli Umetsu
PY220
'''
import argparse
import json
import datetime
import math
import logging
import sys


LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = datetime.datetime.now().strftime('%Y-%m-%d')+".log"

FORMATTER = logging.Formatter(LOG_FORMAT)

FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setLevel(logging.WARNING)
FILE_HANDLER.setFormatter(FORMATTER)

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setLevel(logging.DEBUG)
CONSOLE_HANDLER.setFormatter(FORMATTER)

DEBUG_LEVEL = {'0': logging.CRITICAL, '1': logging.ERROR, '2': logging.WARNING, '3': logging.DEBUG}


def conditional_logging(func):
    """ Decorator for selective logging """
    def setup_logging(level, *args, **kwargs):
        """ Sets the logging level on console/file """
        logger = logging.getLogger()
        logger.setLevel(DEBUG_LEVEL[level])
        logger.addHandler(FILE_HANDLER)
        logger.addHandler(CONSOLE_HANDLER)

        return func(*args, **kwargs)

    return setup_logging


def parse_cmd_arguments():
    """ Parses user inputs """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='output JSON file', required=True)
    parser.add_argument('-d', '--debug', help='logging level: 0-3', required=False, default='0')

    return parser.parse_args()


@conditional_logging
def load_rentals_file(filename):
    """ Loads the rental data input """
    logging.debug("Loading input file %s...", filename)
    try:
        with open(filename) as file:
            try:
                data = json.load(file)
            except ValueError:
                logging.error("Could not locate input file (value error)")
                sys.exit()
    except FileNotFoundError:
        logging.error("Could not locate input file (file did not exist)")
        sys.exit()

    return data


@conditional_logging
def calculate_additional_fields(data):
    """ Calculates rental data """
    logging.debug("Calculating additional rental data...")
    for key, value in data.items():
        logging.debug("*** Processing data for rental %s...***", key)

        # get rental start date
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            logging.debug("[Rental start date: %s...]", rental_start)
        except ValueError:
            logging.error("Invalid date format for rental start")

        # get rental end date
        try:
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            logging.debug("[Rental end date: %s...]", rental_end)
        except ValueError:
            logging.error("Invalid date format for rental end")

        if rental_start > rental_end:
            logging.warning("Start date cannot occur after end date")

        # calculate total rental days
        value['total_days'] = (rental_end - rental_start).days
        logging.debug("Total rental days: %s", value['total_days'])

        # calculate total rental price
        value['total_price'] = value['total_days'] * value['price_per_day']
        logging.debug("Total rental price: %s", value['total_price'])

        # calculate square root of the total rental price
        try:
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            logging.debug("Sqrt rental price: %s", value['sqrt_total_price'])
        except ValueError:
            logging.error("Could not compute square root price for %s (value error)", key)
        except KeyError:
            logging.error("Could not compute square root of %s (key error)", key)

        # calculate unit rental cost
        try:
            value['unit_cost'] = value['total_price'] / value['units_rented']
            logging.debug("Unit cost: %s", value['unit_cost'])
        except ZeroDivisionError:
            logging.error("Could not compute unit cost of %s (divide by 0 error)", key)

    return data


@conditional_logging
def save_to_json(filename, data):
    """ Saves the output file """
    logging.debug("Saving output file %s...", filename)
    with open(filename, 'w') as file:
        json.dump(data, file)


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    DATA = load_rentals_file(ARGS.debug, ARGS.input)
    DATA = calculate_additional_fields(ARGS.debug, DATA)
    save_to_json(ARGS.debug, ARGS.output, DATA)
