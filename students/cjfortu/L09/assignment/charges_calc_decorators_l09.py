'''
L02 baseline:

Returns total price paid for individual rentals.

Debugging uncovered the following, in order:
1: Start date entries can follow end date entries chronologically, crashing the program.
2: There is a units rented value of zero, also crashing the program.

Logging uncovered the following:
3: There are blank rental end dates.

This module addresses these issues, and meets the remaining assignment requirements.


L09 changes:
The command line arguments will set a *unique* logging level *per* function.
Hence the following is possible:

load_rentals_file logging set to either 0, 1, 2, 3
calculate_additional_fields logging set to either 0, 1, 2, 3
save_to_jason logging set to either 0, 1, 2, 3
'''
import argparse
import json
import datetime
import math
import logging
import sys


def parse_cmd_arguments():
    """
    Ingest arguments into an object.

    Added arguments which set logging for each function.
    """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d_l', '--debug_lrf', type=int, help='logging for load_rentals_file',
                        required=True, choices=[0, 1, 2, 3])
    parser.add_argument('-d_c', '--debug_caf', type=int,
                        help='logging for calculate_additional_fields', required=True,
                        choices=[0, 1, 2, 3])
    parser.add_argument('-d_s', '--debug_stj', type=int, help='logging for save_to_json',
                        required=True, choices=[0, 1, 2, 3])

    return parser.parse_args()


def choose_logging_level(function):
    """
    Choose logging level per function.
    """
    def set_logging_params(debug_level, *args, **kwargs):
        """
        Set logging parameters per command line argument.
        """
        log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
        log_file = datetime.datetime.now().strftime("%Y-%m-%d") + '.log'
        formatter = logging.Formatter(log_format)
        console_handler = logging.StreamHandler()
        logger = logging.getLogger()
        logging.getLogger().disabled = False
        if debug_level == 0:
            logging.disable(logging.NOTSET)
            logging.getLogger().disabled = True
        else:
            file_handler = logging.FileHandler(log_file)
            if debug_level == 1:
                file_handler.setLevel(logging.ERROR)
                console_handler.setLevel(logging.ERROR)
                logger.setLevel(logging.ERROR)
            if debug_level == 2:
                file_handler.setLevel(logging.WARNING)
                console_handler.setLevel(logging.WARNING)
                logger.setLevel(logging.WARNING)
            if debug_level == 3:
                file_handler.setLevel(logging.WARNING)
                console_handler.setLevel(logging.DEBUG)
                logger.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        return function(*args, **kwargs)

    return set_logging_params


@choose_logging_level
def load_rentals_file(filename):
    """
    Read source file.

    First route through choose_logging_level.
    """
    with open(filename) as file:
        try:
            data = json.load(file)
            logging.debug('File loaded.')
        except FileNotFoundError:
            logging.error('Invalid file path.')
            sys.exit(0)
    return data


@choose_logging_level
def calculate_additional_fields(data):
    """
    Determine total days, total price, sqrt total price, and unit cost.

    First route through choose_logging_level.
    """
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


@choose_logging_level
def save_to_json(filename, data):
    """
    Write the output file.

    First route through choose_logging_level.
    """
    with open(filename, 'w') as file:
        try:
            json.dump(data, file)
            logging.debug('File written.')
        except Exception as exc:
            logging.error('There was an exception.')
            print(exc)


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    DATA = load_rentals_file(ARGS.debug_lrf, ARGS.input)
    DATA = calculate_additional_fields(ARGS.debug_caf, DATA)
    save_to_json(ARGS.debug_stj, ARGS.output, DATA)
