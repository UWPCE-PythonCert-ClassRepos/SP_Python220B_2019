'''Returns total price paid for individual rentals'''
import argparse
import json
import datetime
import math
import logging
import sys

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

def parse_cmd_arguments():
    '''Parses the user inputs'''
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='ouput JSON file',
                        required=False, default=0)

    return parser.parse_args()


def load_rentals_file(filename):
    '''Loads in the JSON file given by user'''
    with open(filename) as file:
        try:
            data = json.load(file)
        except FileNotFoundError:
            logging.debug("FileNotFoundError in load_rentals_file")
            logging.error(("File name %s could not be found", filename))
            sys.exit()
    return data

def calculate_additional_fields(data):
    '''Calculates addtional info from user given file'''
    for value in data.values():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
        except ValueError:
            logging.debug("ValueError in calculate_additional_fields")
            logging.error(("ValueError: time data %s does not match format '%m/%d/%y'", value))
        try:
            value['total_days'] = (rental_end - rental_start).days
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except ValueError:
            logging.debug("ValueError in calculate_additional_fields")
            logging.error("Start Date must be before End Date")
    return data

def save_to_json(filename, data):
    '''Saves output JSON file'''
    with open(filename, 'w') as file:
        json.dump(data, file)

if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    LEVEL = ARGS.debug
    if LEVEL == '0':
        LOGGER.disabled = True
    elif LEVEL == '1':
        LOGGER.setLevel(logging.ERROR)
        FILE_HANDLER.setLevel(logging.ERROR)
        CONSOLE_HANDLER.setLevel(logging.ERROR)
    elif LEVEL == '2':
        LOGGER.setLevel(logging.WARNING)
        FILE_HANDLER.setLevel(logging.WARNING)
        CONSOLE_HANDLER.setLevel(logging.WARNING)
    elif LEVEL == '3':
        LOGGER.setLevel(logging.DEBUG)
        FILE_HANDLER.setLevel(logging.DEBUG)
        CONSOLE_HANDLER.setLevel(logging.DEBUG)
    DATA = load_rentals_file(ARGS.input)
    DATA = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, DATA)
