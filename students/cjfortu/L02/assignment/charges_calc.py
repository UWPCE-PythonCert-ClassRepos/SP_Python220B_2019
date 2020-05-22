'''
Returns total price paid for individual rentals.

Debugging uncovered the following, in order:
1: Start date entries can follow end date entries chronologically, crashing the program.
2: There is a units rented value of zero, also crashing the program.

Logging uncovered the following:
3: There are blank rental end dates.

This module addresses these issues, and meets the remaining assignment requirements.
'''
import argparse
import json
import datetime
import math
import logging
import sys


def parse_cmd_arguments():
    """Ingest arguments into an object."""
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', type=int, help='logging message levels', required=True,
                        choices=[0, 1, 2, 3])

    return parser.parse_args()


def load_rentals_file(filename):
    """Read source file."""
    with open(filename) as file:
        try:
            data = json.load(file)
        except FileNotFoundError:
            sys.exit(0)
    return data


def calculate_additional_fields(data):
    """Determine total days, total price, sqrt total price, and unit cost."""
    keys = list(data.keys())
    for key in list(data.keys()):
        keys.pop(0)
        if key in keys:
            logging.error(f'Duplicated rental numbers, key = {key}')
    for key, value in data.items():
        logging.debug(key)
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
        except ValueError:
            logging.error(f'No start date, key = {key}')
        try:
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
        except ValueError:
            logging.warning(f'No end date, contract still open. key = {key}')
        if rental_end < rental_start:
            logging.error(f'end date before start date, values now in chrono order. key = {key}')
            value['rental_end'], value['rental_start'] = value['rental_start'], value['rental_end']
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
        value['total_days'] = (rental_end - rental_start).days
        value['total_price'] = value['total_days'] * value['price_per_day']
        value['sqrt_total_price'] = math.sqrt(value['total_price'])
        try:
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except ZeroDivisionError:
            logging.error(f'no units rented, user prompted for correct value. key = {key}')
            value['units_rented'] = int(input(f'source file has {value["units_rented"]}'
                                              ' units rented for rental {key},'
                                              ' please enter correct number of units: '))
            value['unit_cost'] = value['total_price'] / value['units_rented']
    return data


def save_to_json(filename, data):
    """Write the output file."""
    with open(filename, 'w') as file:
        json.dump(data, file)


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()

    # Start logging parameters here vvv
    LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
    LOG_FILE = datetime.datetime.now().strftime("%Y-%m-%d") + '.log'
    FORMATTER = logging.Formatter(LOG_FORMAT)
    CONSOLE_HANDLER = logging.StreamHandler()
    LOGGER = logging.getLogger()
    if ARGS.debug == 0:
        logging.disable(logging.NOTSET)
        logging.getLogger().disabled = True
    else:
        FILE_HANDLER = logging.FileHandler(LOG_FILE)
        if ARGS.debug == 1:
            FILE_HANDLER.setLevel(logging.ERROR)
            CONSOLE_HANDLER.setLevel(logging.ERROR)
        if ARGS.debug == 2:
            FILE_HANDLER.setLevel(logging.WARNING)
            CONSOLE_HANDLER.setLevel(logging.WARNING)
        if ARGS.debug == 3:
            FILE_HANDLER.setLevel(logging.WARNING)
            CONSOLE_HANDLER.setLevel(logging.DEBUG)
            LOGGER.setLevel(logging.DEBUG)
        FILE_HANDLER.setFormatter(FORMATTER)
        LOGGER.addHandler(FILE_HANDLER)
    CONSOLE_HANDLER.setFormatter(FORMATTER)
    LOGGER.addHandler(CONSOLE_HANDLER)
    # End logging parameters here ^^^

    DATA = load_rentals_file(ARGS.input)
    DATA = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, DATA)
