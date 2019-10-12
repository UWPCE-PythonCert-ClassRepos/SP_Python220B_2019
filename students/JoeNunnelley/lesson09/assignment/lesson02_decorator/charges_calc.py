#! /usr/bin/env python3

"""
Returns total price paid for individual rentals

Revisit your logging assignment from lesson 2. We are going to make
logging selective, by using decorators.

Add decorator(s) to introduce conditional logging so that a single
command line variable can turn logging on or off for decorated
classes or functions
"""
import argparse
import datetime
import json
import logging
import math


LOGGER = logging.getLogger()


def setup_logging(_log_level=None):
    """
        Accepts None (no -d sent in) and 1 - 3.
        All other values are invalid including 0
        None: No debug messages or log file.
        1: Only error messages.
        2: Error messages and warnings.
        3: Error messages, warnings and debug messages.
        *  No debug message to logfile
    """
    log_level = logging.INFO
    if _log_level is None:
        print('No debug logging')
        LOGGER.addHandler(logging.NullHandler())
    elif int(_log_level) == 1:
        print('Error message logging')
        log_level = logging.ERROR
    elif int(_log_level) == 2:
        print('Error and Warning messages logging')
        log_level = logging.WARNING
    elif int(_log_level) == 3:
        print('Error, Warning and Debug message logging')
        log_level = logging.DEBUG
    else:
        print("Invalid log_level. Expected values 1 - 3. "
              "This argument is optional.")
        exit(1)

    if _log_level:
        log_file = datetime.datetime.now().strftime("%Y-%m-%d")+'.log'
        log_format = "%(asctime)s %(filename)s:%(lineno)-3d " \
                     "%(levelname)s %(message)s"
        formatter = logging.Formatter(log_format)
        file_handler = logging.FileHandler(log_file, mode='w')

        # We don't want to log DEBUG messages to the log file
        if log_level == logging.DEBUG:
            file_handler.setLevel(logging.WARNING)
        else:
            file_handler.setLevel(log_level)

        file_handler.setFormatter(formatter)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        LOGGER.setLevel(log_level)
        LOGGER.addHandler(console_handler)
        LOGGER.addHandler(file_handler)


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

    parser.add_argument('-d',
                        '--debug',
                        help='set the log output level (1-3)',
                        required=False)

    return parser.parse_args()


def load_rentals_file(filename):
    """ this function loades the json file list of rentals """
    with open(filename) as file:
        try:
            data = json.load(file)
        except FileNotFoundError:
            LOGGER.error("Missing file %s", filename)
            exit(1)
    return data


def calculate_additional_fields(data):
    """ this function creates secondary data points from the primary ones """
    cleaned_data = {}
    for key, value in data.items():
        try:
            # The data provided in the input file is radically incorrect
            # in several way:
            # 1.) start and end dates are frequently backward in that
            #     the start date happens after the end date.
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
            # 8.) This input file is significantly messed up and should
            #     be fixed.
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
                cleaned_data.update({key: value})
                LOGGER.debug("Added validated item to scrubbed dataset:\n%s",
                             value)
            else:
                LOGGER.debug("Skipping item due to invalid data issues:\n%s",
                             value)
        except ValueError as value_error:
            LOGGER.error("%s\n%s", value_error, value)
    #        exit(1)

    return cleaned_data


def check_value_set(value):
    """
    function to attempt to validate the inputs are within
    expected values / ranges. If problems with an entry are
    found, it will not make it into the output file. It will
    be noted in the debug log so that the source file may
    be repaired by the file originator.
    """
    validated = True
    try:
        LOGGER.debug("Checking for missing values")
        assert value['price_per_day'], 'missing price_per_day'
        assert value['product_code'], 'missing product code'
        assert value['rental_start'], 'missing rental_start value'
        assert value['rental_end'], 'missing rental_end value'
        assert value['units_rented'] is not None, 'missing units_rented value'
    except AssertionError as assert_error:
        LOGGER.warning("Data missing check failed: %s\n%s",
                       assert_error,
                       value)
        validated = False

    try:
        LOGGER.debug("Checking values make sense")
        assert value['price_per_day'] >= 0, 'invalid price_per_day'
        start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
        end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
        assert start <= end, 'invalid rental dates'
        assert value['units_rented'] >= 0, 'invalid units_rented value'
    except AssertionError as assert_error:
        LOGGER.error("Data acceptability check failed: %s\n%s",
                     assert_error,
                     value)
        validated = False

    return validated


def save_to_json(filename, data):
    """ this function will save the data to a json file """
    # checking to sef if we got a valid data object back to write
    if data:
        LOGGER.debug("Saving file %s", filename)
        with open(filename, 'w') as file:
            json.dump(data, file, indent=2)
    else:
        LOGGER.warning("Data is invalid. Skipping file writing")


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    setup_logging(ARGS.debug)
    DATA = load_rentals_file(ARGS.input)
    DATA = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, DATA)
