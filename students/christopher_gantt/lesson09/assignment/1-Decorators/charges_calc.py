'''
    Chapter 9, Using decorators for logging

    Setup such that:
        default value --d 0, logging set to only show critical level logs
        default value --ld 'on', all decorated functions will display debug level logs
        logging level for all functions can be changed using cmd line -d
        logging for decorated functions can be turned on or off using cmd line -ld
'''
import argparse
import json
import datetime
import math
import logging


LOG_FORMAT = '%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s'
LOG_FILE = datetime.datetime.now().strftime('%Y-%m-%d')+'.log'

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
    '''
        parses command line arguments

        to run this script on command line, you need to include input and output

        cmd line example with all arguments:
        $ python charges_calc.py -i source.json -o out.json -d (int, 0-3) -ld off
    '''
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='debugger level selection',
                        required=False, default='0')
    parser.add_argument('-ld', '--logging_decorated',
                        help='logging for decorated functions, "on" or "off"',
                        required=False, default='on')

    return parser.parse_args()


def set_log_level(level):
    '''
        sets the levels of the LOGGER according to the default value of 0,
        or to the value entered in the command line
    '''
    if level == '0':
        LOGGER.setLevel(logging.CRITICAL)
        CONSOLE_HANDLER.setLevel(logging.CRITICAL)
        FILE_HANDLER.setLevel(logging.CRITICAL)

    if level == '1':
        LOGGER.setLevel(logging.ERROR)
        CONSOLE_HANDLER.setLevel(logging.ERROR)
        FILE_HANDLER.setLevel(logging.ERROR)

    if level == '2':
        LOGGER.setLevel(logging.WARNING)
        CONSOLE_HANDLER.setLevel(logging.WARNING)
        FILE_HANDLER.setLevel(logging.WARNING)

    if level == '3':
        LOGGER.setLevel(logging.DEBUG)
        CONSOLE_HANDLER.setLevel(logging.DEBUG)
        FILE_HANDLER.setLevel(logging.WARNING)


def decorator_logging(func):
    '''Allows logging to be turned off for decorated functions'''
    def init_logger(*args):
        if ARGS.logging_decorated == 'off':
            LOGGER.setLevel(logging.CRITICAL)
            CONSOLE_HANDLER.setLevel(logging.CRITICAL)
            FILE_HANDLER.setLevel(logging.CRITICAL)
        else:
            LOGGER.setLevel(logging.DEBUG)
            CONSOLE_HANDLER.setLevel(logging.DEBUG)
            FILE_HANDLER.setLevel(logging.DEBUG)

        data = func(*args)
        set_log_level(ARGS.debug)

        return data
    return init_logger


@decorator_logging
def load_rentals_file(filename):
    '''loads the input json file'''
    try:
        with open(filename) as file:
            data = json.load(file)
        logging.debug('file loading successful')
    except FileNotFoundError:
        logging.error('Input json file was not found')
        logging.debug('Error at load_rentals_file(ARGS.input)')
        logging.debug('Script stops when encountering this error')
        exit(0)
    return data


@decorator_logging
def calculate_additional_fields(data):
    '''
    adds additional calculations to data for total_days, total_price,
    sqrt_total_price and unit_cost
    '''
    for key, value in data.items():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
        except ValueError:
            logging.warning("a rental date for %s does not match format m/d/y", key)
            logging.debug('change or add rental date for %s: %s', key, value)
            continue

        if (rental_end - rental_start).days < 1:
            logging.warning('rental end is before rental start for %s', key)
            logging.debug('rental end must be after rental start')
            continue
        else:
            value['total_days'] = (rental_end - rental_start).days
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
    return data


def save_to_json(filename, data):
    '''saves data to a json file'''
    with open(filename, 'w') as file:
        json.dump(data, file)
    logging.debug('file saved')


if __name__ == '__main__':
    ARGS = parse_cmd_arguments()
    set_log_level(ARGS.debug)
    DATA = load_rentals_file(ARGS.input)
    DATA_W_AF = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, DATA_W_AF)
