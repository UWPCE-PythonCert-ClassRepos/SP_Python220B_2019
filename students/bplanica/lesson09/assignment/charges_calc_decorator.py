"""
Revisit your logging assignment from lesson 2. We are going to make logging selective, by using
decorators.

Add decorator(s) to introduce conditional logging so that a single command line variable can
turn logging on or off for decorated classes or functions.
"""

import argparse
import json
import datetime
import math

import sys
import logging


def parse_cmd_arguments():
    """parse command string arguments"""
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='debug enabled/level', default=0)
    parser.add_argument('-l', '--logging', help='enable logging decorators (0/1)', default=0)
    return parser.parse_args()


def setup_logging(level):
    """setup file and console logging"""
    log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
    log_file = datetime.datetime.now().strftime('%Y-%m-%d') + '.log'
    debug_level = [logging.NOTSET, logging.ERROR, logging.WARNING, logging.DEBUG]
    # debug_level = [logging.NOTSET, logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR,
    #                logging.CRITICAL]

    formatter = logging.Formatter(log_format)

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(debug_level[level])
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def logging_decorator(func):
    """logging decorator - turns off logging for decorated functions"""
    def inner_func(*args):
        if int(ARGS.logging) == 0:
            logging.disable()
            result = func(*args)
            logging.disable(logging.NOTSET)
        elif int(ARGS.logging) > 0:
            result = func(*args)
        return result
    return inner_func


@logging_decorator
def load_rentals_file(filename):
    """import data"""
    with open(filename) as file:
        try:
            data = json.load(file)
            logging.info("Data has been sucessfully imported")
        except json.decoder.JSONDecodeError as exc:
            logging.error("JSON source file contains formatting errors; Exception: %s", exc)
            sys.exit()
    return data


@logging_decorator
def calculate_additional_fields(data):
    """calculate additional fields"""
    for key, value in data.items():
        try:
            logging.debug("Format rental start date")
            try:
                rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            except ValueError:
                logging.warning("%s: rental has not initiated", key)

            logging.debug("Format rental end date")
            try:
                rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            except ValueError:
                logging.warning("%s: rental has not been returned", key)

            logging.debug("Calculate total days rented")
            value['total_days'] = (rental_end - rental_start).days
            if (value['total_days']) < 0:
                logging.warning("%s: rental start date (%s) is greater than rental end date (%s)",
                                key, rental_start.strftime('%D'), rental_end.strftime('%D'))

            logging.debug("Calculate total price on rental")
            value['total_price'] = value['total_days'] * value['price_per_day']
            if value['price_per_day'] < 0:
                logging.warning("%s: invalid price per day (%.02f)", key, value['price_per_day'])

            logging.debug("Take squareroot of total price")
            try:
                value['sqrt_total_price'] = math.sqrt(value['total_price'])
            except ValueError:
                if value['total_price'] < 0:
                    logging.error("%s: invalid total price (%.02f)", key, value['total_price'])

            logging.debug("Calculate cost per unit")
            try:
                value['unit_cost'] = value['total_price'] / value['units_rented']
            except ZeroDivisionError:
                logging.error("%s: invalid units rented (%d)", key, value['units_rented'])

        except ValueError as exc:
            logging.error("An exception has occurred; Exception: %s", exc)
            sys.exit()

    return data


#@logging_decorator
def save_to_json(filename, data):
    """export data with calculated fields"""
    with open(filename, 'w') as file:
        json.dump(data, file)
        logging.info("Data has been sucessfully exported")


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    setup_logging(int(ARGS.debug))
    DATA = load_rentals_file(ARGS.input)
    DATA = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, DATA)
