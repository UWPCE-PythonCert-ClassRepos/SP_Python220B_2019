"""Returns total price paid for individual rentals"""
import argparse
import json
import datetime
import math
import logging
from functools import wraps

LOGGING_DICT = {"3": logging.DEBUG,
                "2": logging.WARNING,
                "1": logging.ERROR,
                "0": logging.CRITICAL}


def logging_on_off(func, logging):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if logging == "on":
            logging.disable(logging.NOTSET)
        elif logging == "off":
            logging.disable(logging.CRITICAL)
        return func(*args, **kwargs)
    return wrapper


def logging_setup(level):
    """Sets up the logging properties for the log file"""
    log_format = '%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s'
    formatter = logging.Formatter(log_format)

    log_file = datetime.datetime.now().strftime("%Y-%m-%d") + '.log'

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.WARNING)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(level)
    if not logger.hasHandlers():
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


def parse_cmd_arguments():
    """grabs the arguments to be used later"""
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='debug level', required=True)
    parser.add_argument('-L', '--logging', help='logging "on"/"off"', required=True)
    return parser.parse_args()


def load_rentals_file(filename):
    """loads the data file"""
    with open(filename) as file:
        LOG.debug("Loading data file")
        try:
            data = json.load(file)
        except FileNotFoundError:
            LOG.error("error loading data")
    return data


def calculate_additional_fields(data):
    """calculate various derivative fields based on data"""
    LOG.debug("Beginning data calculations")
    for value in data.values():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            value['total_days'] = (rental_end - rental_start).days
            if value['total_days'] < 1:
                LOG.warning("Start date after end date.")
                continue
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            try:
                value['unit_cost'] = value['total_price'] / value['units_rented']
            except ZeroDivisionError:
                LOG.warning("Zero united rented")

        except ValueError:
            LOG.error("Missing data")

    return data


def save_to_json(filename, data):
    """saves the file"""
    with open(filename, 'w') as file:
        LOG.debug("saving data")
        json.dump(data, file)


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    LOG = logging_setup(LOGGING_DICT[ARGS.debug])
    DATA = logging_on_off(load_rentals_file(ARGS.input), ARGS.logging)
    DATA = logging_on_off(calculate_additional_fields(DATA), ARGS.logging)
    logging_on_off(save_to_json(ARGS.output, DATA), ARGS.logging)
