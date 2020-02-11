"""Returns total price paid for individual rentals """

import argparse
import json
import datetime
import math
import logging  # new import


def logger_decorator(func):
    """Decorator for logging"""
    def setup_logger(level, *args):
        """Set up logger and levels"""
        # Set up format for logger messages and file name
        log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
        log_file = datetime.datetime.now().strftime("%Y-%m-%d")+'.log'

        # Set up formatter
        formatter = logging.Formatter(log_format)

        # Set up file handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)

        # Set up console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # Set up logger
        logger = logging.getLogger()
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        # Set up log level
        if level == 0:
            # No debug messages or log file
            logger.setLevel(logging.CRITICAL)  # Made a change to original code

        elif level == 1:
            # Only error messages
            logger.setLevel(logging.ERROR)
            file_handler.setLevel(logging.ERROR)
            console_handler.setLevel(logging.ERROR)

        elif level == 2:
            # Error messages and warnings
            logger.setLevel(logging.WARNING)
            file_handler.setLevel(logging.WARNING)
            console_handler.setLevel(logging.WARNING)

        elif level == 3:
            # Error messages, warnings and debug messages
            logger.setLevel(logging.DEBUG)
            file_handler.setLevel(logging.DEBUG)
            console_handler.setLevel(logging.DEBUG)
        else:
            raise ValueError("Wrong level")

        return func(*args)
    return setup_logger


def parse_cmd_arguments():
    """Parse arguments to get input and output files, and debug level"""
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='logging level', required=False, default='0', choices=range(0,4))
    return parser.parse_args()


@logger_decorator
def load_rentals_file(filename):
    """Load data from input file (source.json)"""
    with open(filename) as file:
        try:
            data = json.load(file)
        except FileNotFoundError:
            logging.error("File does not exist")
    return data


@logger_decorator
def calculate_additional_fields(data):
    """Caculates total days, total price, total square root of price,
    unit cost"""
    for value in data.values():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            value['total_days'] = (rental_end - rental_start).days
            if value['total_days'] < 0:
                raise ValueError("Rental end date is before rental start date")
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            if value['unit_rented'] == 0:
                logging.error("This will cause ZeroDivisionError for unit cost")
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except ValueError as val_err:
            logging.warning(val_err)
            continue
        except KeyError as key_err:
            logging.warning(key_err)
            continue
    return data


@logger_decorator
def save_to_json(filename, data):
    """Saves data to output file (out.json)"""
    with open(filename, 'w') as file:
        json.dump(data, file)


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    INPUT_DATA = load_rentals_file(ARGS.input)
    OUTPUT_DATA = calculate_additional_fields(INPUT_DATA)
    save_to_json(ARGS.output, OUTPUT_DATA)
