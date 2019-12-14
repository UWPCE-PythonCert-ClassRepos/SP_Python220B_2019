"""
Returns total price paid for individual rentals. Command inputs are input .json file (-i), output
.json file (-o), and logging level (-d). Logging level is defined from 0 to 3:
0: No logging (default)
1: Error messages only, to terminal and logfile (charges_calc_YYYY_MM_DD.log)
2: Warning and error messages only, to terminal and logfile.
3: Debug, warning, and error messages to terminal, warning and error only to logfile.
"""
import sys
import argparse
import json
import datetime
import math
import logging

LOG_FORMAT = '%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s'
LOG_FILE = 'charges_calc_'+datetime.datetime.now().strftime('%Y-%m-%d')+'.log'

FORMATTER = logging.Formatter(LOG_FORMAT)

FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setLevel(logging.WARNING)
FILE_HANDLER.setFormatter(FORMATTER)

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setLevel(logging.DEBUG)
CONSOLE_HANDLER.setFormatter(FORMATTER)

LOGGER = logging.getLogger()
LOGGER.addHandler(CONSOLE_HANDLER)


def parse_cmd_arguments():
    """Define command line input arguments"""
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='output JSON file', required=True)
    parser.add_argument('-d', '--debug', help='set debugging output', default=0, type=int)

    return parser.parse_args()


def set_logger_level(debug_level):
    """Sets the logger level"""
    if debug_level == 1:
        LOGGER.addHandler(FILE_HANDLER)
        LOGGER.setLevel(logging.ERROR)
    elif debug_level == 2:
        LOGGER.addHandler(FILE_HANDLER)
        LOGGER.setLevel(logging.WARNING)
    elif debug_level == 3:
        LOGGER.addHandler(FILE_HANDLER)
        LOGGER.setLevel(logging.DEBUG)
    else:
        logging.disable(logging.CRITICAL)


def load_rentals_file(filename):
    """Loads data for processing from input .json file."""
    try:
        with open(filename) as file:
            data = json.load(file)
    except FileNotFoundError:
        logging.error('Input file %s not found.', filename)
        sys.exit(0)
    except json.decoder.JSONDecodeError:
        logging.error('Input .json file %s did not load successfully.', filename)
        sys.exit(0)
    else:
        logging.debug('Input file %s successfully loaded. Total data length: %d.', filename,
                      len(data))
    return data


def calculate_additional_fields(data):
    """Calculates total rental days, total rental price, sqrt rental price, and unit cost."""
    for value in data.values():
        logging.debug('Calculating additional fields for product code: %s', value['product_code'])
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
        except ValueError:
            logging.warning('Rental start date missing or in incorrect format: (%s) for product'
                            ' code: %s.', value['rental_start'], value['product_code'])
            continue
        try:
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
        except ValueError:
            logging.warning('Rental end date missing or in incorrect format: (%s) for product'
                            ' code: %s.', value['rental_end'], value['product_code'])
            continue
        value['total_days'] = (rental_end - rental_start).days
        if value['total_days'] < 0:
            logging.error('Negative rental period found (%d days) for product code: %s. Rental '
                          'start date: %s, ''rental end date: %s.', value['total_days'],
                          value['product_code'], value['rental_start'], value['rental_end'])
            continue
        value['total_price'] = value['total_days'] * value['price_per_day']
        value['sqrt_total_price'] = math.sqrt(value['total_price'])
        value['unit_cost'] = value['total_price'] / value['units_rented']
    logging.debug('Additional field calculations complete.')
    return data


def save_to_json(filename, data):
    """Writes data to .json output file"""
    with open(filename, 'w') as file:
        json.dump(data, file)
    logging.debug('Successfully wrote data to %s.', filename)


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    set_logger_level(ARGS.debug)
    DATA = load_rentals_file(ARGS.input)
    DATA = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, DATA)
