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
DEBUG = None
LOG_LEVEL_DEFAULT = int(logging.CRITICAL / 10)


def setup_logging():
    """
        Accepts None (no -d sent in) and 1 - 3.
        All other values are invalid including 0
        None and 0: No debug messages or log file.
        1: Debug message level.
        2: Info message level
        3: Warning mesage level.
        4: Error message level.
        5: Critical message level.
        *  No debug message to logfile
    """
    if LOG_LEVEL_DEFAULT is None or LOG_LEVEL_DEFAULT == 0:
        print('No debug logging')
        LOGGER.addHandler(logging.NullHandler())
    elif int(LOG_LEVEL_DEFAULT) == 1:
        print('Debug level message logging')
        log_level = logging.DEBUG
    elif int(LOG_LEVEL_DEFAULT) == 2:
        print('Info level message logging')
        log_level = logging.INFO
    elif int(LOG_LEVEL_DEFAULT) == 3:
        print('Warning level messages logging')
        log_level = logging.WARNING
    elif int(LOG_LEVEL_DEFAULT) == 4:
        print('Error level message logging')
        log_level = logging.ERROR
    elif int(LOG_LEVEL_DEFAULT) == 5:
        print('Critical level message logging')
        log_level = logging.CRITICAL
    else:
        print("Invalid log_level. Expected values 0 - 5. "
              "This argument is optional.")
        exit(1)

    log_file = datetime.datetime.now().strftime("%Y-%m-%d")+'.log'
    log_format = "%(asctime)s %(filename)s:%(lineno)-3d " \
                 "%(levelname)s %(message)s"
    formatter = logging.Formatter(log_format)
    file_handler = logging.FileHandler(log_file, mode='w')

    # We don't want to log DEBUG messages to the log file
    if LOG_LEVEL_DEFAULT == logging.DEBUG:
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

    LOGGER.info('Logger Setup')


def set_debug(func):
    """
    Function to temporarily turn on debug logging
    """
    def wrapper(*args, **kwargs):
        current_level = LOGGER.level
        if DEBUG:
            print('>> Overriding Default Log Level <<')
            for handler in LOGGER.handlers:
                handler.setLevel(logging.DEBUG)
            LOGGER.setLevel(logging.DEBUG)

            func(*args, **kwargs)

            for handler in LOGGER.handlers:
                handler.setLevel(current_level)
            LOGGER.setLevel(current_level)

        else:
            func(*args, **kwargs)

    return wrapper


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

    parser.add_argument('-l',
                        '--log_level',
                        help='set the log output level (0-5)',
                        required=False)

    parser.add_argument('-d',
                        '--debug',
                        help='turn on debug output',
                        action='store_true',
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


@set_debug
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
            LOGGER.critical("%s\n%s", value_error, value)
            exit(1)

    return cleaned_data


@set_debug
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
        LOGGER.warning("Data acceptability check failed: %s\n%s",
                       assert_error,
                       value)
        validated = False

    return validated


@set_debug
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
    LOG_LEVEL_DEFAULT = ARGS.log_level if ARGS.log_level else LOG_LEVEL_DEFAULT
    setup_logging()
    DEBUG = ARGS.debug if ARGS.debug else None
    DATA = load_rentals_file(ARGS.input)
    DATA = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, DATA)
