"""
Returns total price paid for individual rentals
"""

import argparse
import json
import datetime
import math
import logging


#pylint: disable=too-many-function-args

def logging_setup(func):
    """ Adds a Decorator to log functions differently """
    def debug_setup(debug_level, *args):
        """ Sets the logging file name and levels """
        # create log format to use for logging
        log_format = '%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s'
        formatter = logging.Formatter(log_format)

        # create and set file name for log file
        log_file = datetime.datetime.now().strftime('%Y-%m-%d')+'.log'

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger = logging.getLogger()
        logger.addHandler(console_handler)

        # setting the logger

        if debug_level == 1:
            logger.setLevel(logging.ERROR)
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            file_handler.setLevel(logging.ERROR)
            console_handler.setLevel(logging.ERROR)
            logger.addHandler(file_handler)

        elif debug_level == 2:
            logger.setLevel(logging.WARNING)
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            file_handler.setLevel(logging.WARNING)
            console_handler.setLevel(logging.WARNING)
            logger.addHandler(file_handler)

        elif debug_level == 3:
            logger.setLevel(logging.DEBUG)
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            file_handler.setLevel(logging.DEBUG)
            console_handler.setLevel(logging.DEBUG)
            logger.addHandler(file_handler)

        elif debug_level == 0:
            logger.disabled = True

        else:
            logger.error('Incorrect Debug Level')
            raise ValueError
        return func(*args)
    return debug_setup


def parse_cmd_arguments():
    """ Gets input file, output file, and debug level. """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='output JSON file', required=True)
    parser.add_argument('-d', '--debug', help='debug_level', required=False, type=int, default=0)

    return parser.parse_args()


@logging_setup
def load_rentals_file(filename):
    """ Loads input file """
    with open(filename) as file:
        try:
            data_info = json.load(file)
        except:
            logging.warning('File does not exist')
            raise FileNotFoundError

    return data_info


@logging_setup
def calculate_additional_fields(data_info):
    """ Sorts data in input file """
    for value in data_info.values():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            value['total_days'] = (rental_end - rental_start).days
            if value['total_days'] < 0:
                logging.warning('%s: Rental End date is before Rental Start date!',
                                value['product_code'])
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except ValueError:
            logging.warning('%s: Cannot squareroot negative number!', value['product_code'])
            continue
        except ZeroDivisionError:
            logging.warning('%s: There are no units rented for this item.', value['product_code'])
            continue

    return data_info


@logging_setup
def save_to_json(filename, data):
    """ Saves data into to new json file """
    with open(filename, 'w') as file:
        json.dump(data, file)


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    DATA = load_rentals_file(ARGS.debug, ARGS.input)
    DATA = calculate_additional_fields(ARGS.debug, DATA)
    save_to_json(ARGS.debug, ARGS.output, DATA)
