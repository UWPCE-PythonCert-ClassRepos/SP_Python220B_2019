"""
Returns total price paid for individual rentals
"""
import argparse
import json
import datetime
import math
import logging

# LOGGER
LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = datetime.datetime.now().strftime("%Y-%m-%d") + ".log"
FORMATTER = logging.Formatter(LOG_FORMAT)

FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setFormatter(FORMATTER)

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setFormatter(FORMATTER)

LOGGER = logging.getLogger()
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLE_HANDLER)


def parse_cmd_arguments():
    """ Parse Command Line Argument

    Parses the provided command line argument provided.
    -i --input Input file name
    -o --output Output file name
    -d --debug Debug log level

    """
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("-i", "--input", help="input JSON file", required=True)
    parser.add_argument("-o", "--output", help="ouput JSON file", required=True)
    parser.add_argument(
        "-d", "--debug", help="debug log level", required=True, type=int
    )
    return parser.parse_args()


def set_logging_level(level):
    """ Set Logging Level
    Sets the logging level provided in CLI.

    0: No debug messages or log file.
    1: Only error messages.
    2: Error messages and warnings.
    3: Error messages, warnings and debug messages.

    """
    if level == 0:
        FILE_HANDLER.setLevel(logging.NOTSET)
        CONSOLE_HANDLER.setLevel(logging.NOTSET)
        LOGGER.setLevel(logging.NOTSET)
        logging.disable()
    elif level == 1:
        FILE_HANDLER.setLevel(logging.ERROR)
        CONSOLE_HANDLER.setLevel(logging.NOTSET)
        LOGGER.setLevel(logging.ERROR)
    elif level == 2:
        FILE_HANDLER.setLevel(logging.WARNING)
        CONSOLE_HANDLER.setLevel(logging.NOTSET)
        LOGGER.setLevel(logging.WARNING)
    elif level == 3:
        FILE_HANDLER.setLevel(logging.WARNING)
        CONSOLE_HANDLER.setLevel(logging.DEBUG)
        LOGGER.setLevel(logging.DEBUG)
    else:
        raise ValueError("Level must be between 0 - 3")
    logging.debug("Set Logging Level")


def load_rentals_file(filename):
    """ Load file
    Loads the rental file (filename) provided with CLI option -i
    """
    logging.debug("Load Rental Files: %s", filename)
    try:
        with open(filename) as file:
            data = json.load(file)
    except IOError:
        logging.error("File '%s' not found", filename)
        exit(0)
    return data


def calculate_additional_fields(data):
    """ Appends to data
    For all data loaded from file, appends the following additional data
    to the original data:
    total_days: Total number of days rented
    total_price: Cost of rental from total number of days
    sqrt_total_price: Square root of the total price
    unit_cost: Cost of rental for a single unit
    """
    logging.debug("Calculate Additional Fields")
    # for value in data.values():
    remove_list = []
    for key, value in data.items():
        try:
            rental_start = datetime.datetime.strptime(value["rental_start"], "%m/%d/%y")
            rental_end = datetime.datetime.strptime(value["rental_end"], "%m/%d/%y")
            total_days = rental_end - rental_start
        except ValueError:
            logging.warning("Datetime must be in format m/d/y")
            logging.debug("Rental date improperly formatted in {value}")
            total_days = datetime.timedelta(days=-1)

        if total_days < datetime.timedelta(0):
            logging.error("Rental length must be > 0, currently is %s", total_days)
            value["total_days"] = -1
        else:
            value["total_days"] = total_days.days

        try:
            value["total_price"] = value["total_days"] * value["price_per_day"]
            value["sqrt_total_price"] = round(math.sqrt(value["total_price"]), 2)
            value["unit_cost"] = round(value["total_price"] / value["units_rented"], 2)
        except ValueError as e_val:
            logging.error("Exception in data: %s", e_val)
            logging.error("Removing %s from Output", value)
            remove_list.append(key)

    if remove_list:
        for key in remove_list:
            del data[key]
    return data


def save_to_json(filename, data):
    """ Save output file
    Saves output file with name provided in CLI option -o
    """
    logging.debug("Saving to file: %s", filename)
    with open(filename, "w") as file:
        json.dump(data, file)


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    set_logging_level(ARGS.debug)
    RENTAL_DATA = load_rentals_file(ARGS.input)
    RENTAL_DATA = calculate_additional_fields(RENTAL_DATA)
    save_to_json(ARGS.output, RENTAL_DATA)
