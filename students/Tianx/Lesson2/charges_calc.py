"""
Returns total price paid for individual rentals

logging with command line --debug or -d

0: No debug messages or log file.
1: Only error messages.
2: Error messages and warnings.
3: Error messages, warnings and debug messages.

All logs are written to a .log file in this directory as well as the console
"""
import argparse
import json
import datetime
import math
import logging


def logger(debug_level):
    """Setting up logging level"""
    LOG_FORMAT = '%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s'
    LOG_FILE = 'charges_calc_'+datetime.datetime.now().strftime('%Y-%m-%d')+'.log'

    FORMATTER = logging.Formatter(LOG_FORMAT)
    FILE_HANDLER = logging.FileHandler(LOG_FILE, mode="w")
    FILE_HANDLER.setFormatter(FORMATTER)

    CONSOLE_HANDLER = logging.StreamHandler()
    CONSOLE_HANDLER.setFormatter(FORMATTER)
    LOGGER = logging.getLogger()
    LOGGER.addHandler(FILE_HANDLER)
    LOGGER.addHandler(CONSOLE_HANDLER)

    if debug_level == '0':
        LOGGER.disabled = True
    elif debug_level == '1':
        LOGGER.setLevel(logging.ERROR)
        FILE_HANDLER.setLevel(logging.ERROR)
        CONSOLE_HANDLER.setLevel(logging.ERROR)
    elif debug_level == '2':
        LOGGER.setLevel(logging.WARNING)
        FILE_HANDLER.setLevel(logging.WARNING)
        CONSOLE_HANDLER.setLevel(logging.WARNING)
    elif debug_level == '3':
        LOGGER.setLevel(logging.DEBUG)
        FILE_HANDLER.setLevel(logging.WARNING)
        CONSOLE_HANDLER.setLevel(logging.DEBUG)
    else:
        logging.debug("ValueError!")
        logging.error("Debug level should be 0-3")


def parse_cmd_arguments():
    """Defining command line input args"""
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='input debug', required=False,
                        type=int, default=0)

    return parser.parse_args()


def load_rentals_file(filename):
    """Loading data from the input Json file."""
    with open(filename) as file:
        try:
            data = json.load(file)
            logging.debug('Data has been loaded, no error')
        except FileNotFoundError:
            logging.error('File not found. Unable to load file from %s', filename)
            exit(0)
        except json.decoder.JSONDecodeError:
            logging.error('Unable to load file from %s', filename)
            exit(0)
    return data


def calculate_additional_fields(data):
    """Calculate additional fields """
    for value in data.values():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
        except ValueError:
            logging.warning('Invalid or missing rental_start date: %s'
                            'product code: %s.', value['rental_start'], value['product_code'])
            logging.debug('Error in calculate_additional_fields')
            continue
        try:
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
        except ValueError:
            logging.warning('Invalid or missing rental_end date: %s'
                            'product code: %s.', value['rental_end'], value['product_code'])
            logging.debug('Error in calculate_additional_fields')
            continue
        value['total_days'] = (rental_end - rental_start).days
        if value['total_days'] < 0:
            logging.error('End date %s is before the Start date %s.',value['rental_end'],
                            value['rental_start'])
        value['total_price'] = value['total_days'] * value['price_per_day']
        if value['price_per_day'] < 0:
            logging.warning("price cannot be negative", value['price_per_day'])
            logging.debug("total_price: %s", value['total_price'])
        try:
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            logging.debug("sqrt_total_price: %s", value['sqrt_total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
            logging.debug("unit_cost: %s", value['unit_cost'])
        except ValueError:
            logging.warning('Value Error in calculation')
        except ZeroDivisionError:
            logging.warning('Unites_rented is Zero')
            continue
    return data


def save_to_json(filename, data):
    """Save data to output file"""
    with open(filename, 'w') as file:
        json.dump(data, file)


if __name__ == "__main__":
    args = parse_cmd_arguments()
    logger(args.debug)
    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)
