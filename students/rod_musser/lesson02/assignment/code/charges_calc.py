'''
Returns total price paid for individual rentals
'''
import argparse
import json
from json import JSONDecodeError
import datetime
import math
import logging
import sys


def parse_cmd_arguments():
    """
    Parses command arguments passed in.
    """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', type=int, help='debug level', default=0, required=False)

    return parser.parse_args()


def load_rentals_file(filename):
    """
    Loads the rental data

    :param filename: Path and filename of rental data
    """
    with open(filename) as file:
        try:
            data = json.load(file)
        except JSONDecodeError:
            sys.exit(0)
    return data


def calculate_additional_fields(data):
    """
    Take in rental data and compute calculated data for each rental.

    :param data: Dict of rental data with rental code as the key and the value
    being a dictionary of rental data.
    """
    for rental_code, value in data.items():
        try:
            logging.debug("Processig rental id %s.", rental_code)
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            if not rental_end:
                logging.warning("Invalid data.  Rental id %s has not ended.", rental_code)
                continue
            value['total_days'] = (rental_end - rental_start).days
            if value['total_days'] < 0:
                logging.warning("Invalid data for rental id %s."
                                "Rental start date of %s is after rental end date of %s",
                                rental_code, datetime.datetime.strftime(rental_start, '%Y-%m-%d'),
                                datetime.datetime.strftime(rental_end, '%Y-%m-%d'))
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except ValueError as v_e:
            logging.error(v_e)

    return data


def save_to_json(filename, data):
    """
    Write processed data to a file in json format.

    :param filename: Name of file to write data to
    :param data: Dictonary of rental data to write
    """

    with open(filename, 'w') as file:
        json.dump(data, file)


def configure_logging(log_level):
    """
    Set the logging level

    :param log_level: Integer to set logging level to
    """
    # Convert log level to numeric value of logging level
    if log_level == 1:
        log_level = logging.ERROR
    elif log_level == 2:
        log_level = logging.WARNING
    elif log_level == 3:
        log_level = logging.DEBUG

    log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
    formatter = logging.Formatter(log_format)

    log_file = datetime.datetime.now().strftime("%Y-%m-%d") + '.log'
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    logger = logging.getLogger()
    if log_level == 0:
        logger.disabled = True
    logger.setLevel(log_level)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


if __name__ == "__main__":
    args = parse_cmd_arguments()
    configure_logging(args.debug)
    rental_data = load_rentals_file(args.input)
    rental_data = calculate_additional_fields(rental_data)
    save_to_json(args.output, rental_data)
