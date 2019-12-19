"""
Returns total price paid for individual rentals
12/18/2019, BPA, added logging/debuging
"""

import argparse
import json
import datetime
import math

import sys
import logging
LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = datetime.datetime.now().strftime("%Y-%m-%d") + '.log'

FORMATTER = logging.Formatter(LOG_FORMAT)

FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setLevel(logging.WARNING)
FILE_HANDLER.setFormatter(FORMATTER)

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setLevel(logging.DEBUG)
CONSOLE_HANDLER.setFormatter(FORMATTER)

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLE_HANDLER)

DEBUG_LEVEL = [logging.NOTSET, logging.ERROR, logging.WARNING, logging.DEBUG]

def parse_cmd_arguments():
    """parse command string arguments"""
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='debug enabled/level', default=0)
    return parser.parse_args()


def load_rentals_file(filename):
    """import data"""
    with open(filename) as file:
        try:
            data = json.load(file)
            logging.info("Data has been sucessfully imported")
        except Exception as exc:
            logging.error(f"Data has not been imported; Exception: {exc}")
            sys.exit()
    return data


def calculate_additional_fields(data):
    """calculate additional fields"""
    for key, value in data.items():
        try:
            logging.debug("Format rental start date")
            try:
                rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            except ValueError:
                logging.warning(f"{key}: rental has not initiated")

            logging.debug("Format rental end date")
            try:
                rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            except ValueError:
                logging.warning(f"{key}: rental has not been returned")

            logging.debug("Calculate total days rented")
            value['total_days'] = (rental_end - rental_start).days
            if (value['total_days']) < 0:
                logging.warning(f"{key}: rental start date ({rental_start.strftime('%D')}) " +
                                f"is greater than rental end date ({rental_end.strftime('%D')})")

            logging.debug("Calculate total price on rental")
            value['total_price'] = value['total_days'] * value['price_per_day']
            if value['price_per_day'] < 0:
                logging.warning(f"{key}: invalid price per day ({value['price_per_day']})")

            logging.debug("Take squareroot of total price")
            try:
                value['sqrt_total_price'] = math.sqrt(value['total_price'])
            except ValueError:
                if value['total_price'] < 0:
                    logging.error(f"{key}: invalid total price ({value['total_price']})" +
                                  f", squareroot returns imaginary value")

            logging.debug("Calculate cost per unit")
            try:
                value['unit_cost'] = value['total_price'] / value['units_rented']
            except ZeroDivisionError:
                logging.error(f"{key}: invalid units rented ({value['units_rented']})")

        except Exception as exc:
            logging.critical(f"{key}: Exception has been thrown: {exc}")
            sys.exit()

    return data


def save_to_json(filename, data):
    """export data with calculated fields"""
    with open(filename, 'w') as file:
        json.dump(data, file)
        logging.info("Data has been sucessfully exported")


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    LOGGER.setLevel(DEBUG_LEVEL[int(ARGS.debug)])
    DATA = load_rentals_file(ARGS.input)
    DATA = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, DATA)
