#!/usr/bin/env python3
"""
Returns total price paid for individual rentals
"""
# Corrected docstring format
import argparse
import json
import datetime
import math
import logging

LOGGER = logging.getLogger()
LOGGING_ENABLED = False


def config_logging(log_level):
    """Configure and set up logging for the program"""
    # Configure logging for the program
    log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
    formatter = logging.Formatter(log_format)
    log_file = datetime.datetime.now().strftime("%Y-%m-%d")+".log"
    logging_level = {0: LOGGER.disabled, 1: logging.ERROR, 2: logging.WARNING, 3: logging.DEBUG}
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(formatter)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging_level.get(int(log_level)))
    console_handler.setFormatter(formatter)
    LOGGER.setLevel(logging_level.get(int(log_level)))
    LOGGER.addHandler(file_handler)
    LOGGER.addHandler(console_handler)


def toggle_logging(function):
    """A Decorator to toggle logging on or off"""
    def toggle(*args, **kwargs):
        if not LOGGING_ENABLED:
            LOGGER.disabled = True
            return function(*args, **kwargs)
    return toggle


def parse_cmd_arguments():
    """Command line input argument parser"""
    # Added Docstring to function
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("-i", "--input", help="input JSON file", required=True)
    parser.add_argument("-o", "--output", help="output JSON file", required=True)
    # Corrected a spelling mistake
    parser.add_argument("-d", "--debug", default=0, help="debugging level", required=False)
    # Line added to turn on debugging with a parameter switch, default is disabled
    return parser.parse_args()


@toggle_logging
def load_rentals_file(filename):
    """Open input data file"""
    # Added Docstring to function
    with open(filename) as file:
        try:
            # Added a try-catch for a missing or invalid input file
            data = json.load(file)
        except FileNotFoundError:
            logging.warning("File Not Found error encountered when loading the input file")
            logging.debug("Input file %s was not found, please check the file location", filename)
    return data


@toggle_logging
def calculate_additional_fields(data):
    """calculate total renal time, total renal cost and append records with new data fields"""
    # Added Docstring to function
    for key, value in data.items():
        # Changed variable name for data items due to scoping issue when using "data.values"
        try:
            # Added a try-catch for invalid date format
            rental_start = datetime.datetime.strptime(value["rental_start"], "%m/%d/%y")
            rental_end = datetime.datetime.strptime(value["rental_end"], "%m/%d/%y")
        except ValueError:
            logging.warning("Value Error found in date fields of input %s", key)
            logging.debug("%s has incorrect date or date format in record %s", key, value)
        value["total_days"] = (rental_end - rental_start).days
        if value["total_days"] < 0:
            # Added a catch for date inconsistency
            logging.warning("Invalid end date found in %s", key)
            logging.debug("Invalid end date of %s found in record %s", rental_end, key)
        value["total_price"] = value["total_days"] * value["price_per_day"]
        try:
            # Added a try-catch for Value Error on math square root error
            value["sqrt_total_price"] = math.sqrt(value["total_price"])
        except ValueError:
            logging.warning("Value Error when calculating the square of"
                            " the total price for record %s", key)
            logging.debug("Value Error on record %s, value %s while "
                          "calculating the square of the total price", key, value)
        try:
            # Added a try-catch for divide by zero error
            value["unit_cost"] = value["total_price"] / value["units_rented"]
        except ZeroDivisionError:
            logging.warning("Tried to divide by Zero while calculating record %s", key)
            logging.debug("Tried to divide by Zero, record %s, value %s", key, value)
    return data


def save_to_json(filename, data):
    """Output the modified data to a new file"""
    # Added Docstring to function
    with open(filename, "w") as file:
        json.dump(data, file)


if __name__ == "__main__":
    # Scoping issue on variables, redefined as global
    ARGS = parse_cmd_arguments()
    config_logging(ARGS.debug)
    # Added the argument to the command line switches for enabling logging
    DATA = load_rentals_file(ARGS.input)
    DATA = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, DATA)
