#! /usr/bin/env python3

"""
Returns total price paid for individual rentals
"""
import argparse
import datetime
import json
import logging
import math

log_format = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"
formatter = logging.Formatter(log_format)
file_handler = logging.FileHandler('charges_calc.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)
console_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(console_handler)
logger.addHandler(file_handler)

def parse_cmd_arguments():
    """ this function parses the command line arguments """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i',
                        '--input',
                        help='input JSON file',
                        required=True)
    parser.add_argument('-o',
                        '--output',
                        help='ouput JSON file',
                        required=True)

    return parser.parse_args()


def load_rentals_file(filename):
    """ this function loades the json file list of rentals """
    with open(filename) as file:
        try:
            data = json.load(file)
        except FileNotFoundError:
            logger.error("Missing file {}".format(filename))
            exit(0)
    return data


def calculate_additional_fields(data):
    """ this function creates secondary data points from the primary ones """
    for value in data.values():
        try:
            if check_value_set(value):
                rental_start = datetime.datetime.strptime(value['rental_start'],
                                                      '%m/%d/%y')
                rental_end = datetime.datetime.strptime(value['rental_end'],
                                                    '%m/%d/%y')
                value['total_days'] = (rental_end - rental_start).days
                value['total_price'] = value['total_days'] * value['price_per_day']
                value['sqrt_total_price'] = math.sqrt(value['total_price'])
                value['unit_cost'] = value['total_price'] / value['units_rented']
            else:
                logger.debug("Skipping item due to invalid data issues:\n{}".format(value))
        except ValueError as ve:
            logger.error(ve)
            exit(0)

    return data

def check_value_set(value):
  """ function to validate the inputs are within allowable value ranges """
  try:
    logger.debug("Checking price_per_day value")
    assert value['price_per_day'] and value['price_per_day'] >= 0
    logger.debug("Checking product_code value")
    assert value['product_code']
    logger.debug("Making sure rental date values are present")
    assert value['rental_start'] and value['rental_end']
    logger.debug("Checking rental date values make sense")
    start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
    end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
    assert start < end
    logger.debug("Checking units_rented value")
    assert value['units_rented'] and value['units_rented'] >= 0
    return True
  except AssertionError:
    logger.warning("Data validation failed")
    return False


def save_to_json(filename, data):
    """ this function will save the data to a json file """
    logger.debug("Saving file {}".format(filename))
    with open(filename, 'w') as file:
        json.dump(data, file)


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    DATA = load_rentals_file(ARGS.input)
    DATA = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, DATA)
