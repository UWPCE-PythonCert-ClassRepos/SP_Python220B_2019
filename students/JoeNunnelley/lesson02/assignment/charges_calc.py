#! /usr/bin/env python3

"""
Returns total price paid for individual rentals
"""
import argparse
import datetime
import json
import logging
import math

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"
FORMATTER = logging.Formatter(LOG_FORMAT)
FILE_HANDLER = logging.FileHandler('charges_calc.log')
FILE_HANDLER.setLevel(logging.DEBUG)
FILE_HANDLER.setFormatter(FORMATTER)

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setLevel(logging.WARNING)
CONSOLE_HANDLER.setFormatter(FORMATTER)

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(CONSOLE_HANDLER)
LOGGER.addHandler(FILE_HANDLER)


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
            LOGGER.error("Missing file %s", filename)
            exit(0)
    return data


def calculate_additional_fields(data):
    """ this function creates secondary data points from the primary ones """
    clean_data = True
    for value in data.values():
        try:
            # The data provided in the input file is radically incorrect
            # in several way:
            # 1.) start and end dates are frequently backward in that
            #     the start date happens after the end date. By my
            #     count 998 out of 999 rental dates are reversed.
            # 2.) we are not doing any bounds checking on any of the
            #     following values:
            #    a.) price_per_day
            #   `b.) unit_cost
            #    c.) dates
            # 3.) we are not catching errors that might come about
            #     because a string cannot be cast to a date
            # 4.) we are not ensuring that total_price is >= 0 before
            #     we try to run sqrt() on it which is an invalid
            #     mathematical operation
            # 5.) we are not checking that units_rented is a
            #     number > 0 which will cause a divide by zero if
            #     attempted on a value <= 0
            # 6.) we are not checking that values exist in the dataset
            #     before attempting to access them. Potental NullValue
            #     error
            # 7.) we are calculating additional fields over the entire
            #     set which makes allowing valid entries through more
            #     difficult than in these operations were atomic.
            if check_value_set(value):
                rental_start = (datetime
                                .datetime
                                .strptime(value['rental_start'],
                                          '%m/%d/%y'))
                rental_end = (datetime
                              .datetime
                              .strptime(value['rental_end'],
                                        '%m/%d/%y'))
                value['total_days'] = (rental_end - rental_start).days
                value['total_price'] = (value['total_days'] *
                                        value['price_per_day'])
                value['sqrt_total_price'] = math.sqrt(value['total_price'])
                value['unit_cost'] = (value['total_price'] /
                                      value['units_rented'])
            else:
                LOGGER.debug("Skipping item due to invalid data issues:\n%s",
                             value)
                clean_data = False
        except ValueError as value_error:
            LOGGER.error(value_error)
            exit(0)

    return data if clean_data else None


def check_value_set(value):
    """
    function to attempt to validate the inputs are within
    expected values / ranges
    """
    try:
        LOGGER.debug("Checking price_per_day value")
        assert value['price_per_day'] and value['price_per_day'] >= 0
        LOGGER.debug("Checking product_code value")
        assert value['product_code']
        LOGGER.debug("Making sure rental date values are present")
        assert value['rental_start'] and value['rental_end']
        LOGGER.debug("Checking rental date values make sense")
        start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
        end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
        assert start < end
        LOGGER.debug("Checking units_rented value")
        assert value['units_rented'] and value['units_rented'] >= 0
        return True
    except AssertionError:
        LOGGER.warning("Data validation failed")
        return False


def save_to_json(filename, data):
    """ this function will save the data to a json file """
    # checking to sef if we got a valid data object back to write
    if data:
        LOGGER.debug("Saving file %s", filename)
        with open(filename, 'w') as file:
            json.dump(data, file)
    else:
        LOGGER.warning("Data is invalid. Skipping file writing")


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    DATA = load_rentals_file(ARGS.input)
    DATA = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, DATA)
