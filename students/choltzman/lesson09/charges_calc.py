# pylint: disable=invalid-name,consider-using-sys-exit,too-many-function-args
"""
Returns total price paid for individual rentals
"""
import argparse
import json
import logging
import math
from datetime import datetime


def logging_decorator(func):
    """Decorator for adding logging to a function"""
    def wrapper(level, *args):
        # setup logging
        LOG_FMT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"  # pylint: disable=line-too-long
        FORMATTER = logging.Formatter(LOG_FMT)
        LOG_FILE = datetime.now().strftime("%Y-%m-%d") + ".log"

        FILE_HANDLER = logging.FileHandler(LOG_FILE)
        FILE_HANDLER.setLevel(logging.WARNING)
        FILE_HANDLER.setFormatter(FORMATTER)

        CONSOLE_HANDLER = logging.StreamHandler()
        CONSOLE_HANDLER.setLevel(logging.DEBUG)
        CONSOLE_HANDLER.setFormatter(FORMATTER)

        LOGGER = logging.getLogger()
        LOGGER.setLevel(logging.DEBUG)
        LOGGER.addHandler(FILE_HANDLER)
        LOGGER.addHandler(CONSOLE_HANDLER)

        if level == '0':
            LOGGER.disabled = True
        else:
            # choose log level from input
            if level == '1':
                loglevel = logging.ERROR
            elif level == '2':
                loglevel = logging.WARNING
            elif level == '3':
                loglevel = logging.DEBUG
            else:
                logging.warning("Unknown log level: %s", level)
                exit(1)
            # set log level
            LOGGER.setLevel(loglevel)
            FILE_HANDLER.setLevel(loglevel)
            CONSOLE_HANDLER.setLevel(loglevel)

        return func(*args)

    return wrapper


def parse_cmd_arguments():
    """Parse arguments from the commandline."""
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', required=True,
                        help='input JSON file')
    parser.add_argument('-o', '--output', required=True,
                        help='ouput JSON file')
    parser.add_argument('-d', '--debug', required=False, default='0',
                        choices=['0', '1', '2', '3'],
                        help="sets verbosity of debug messages (0-3)")

    return parser.parse_args()


@logging_decorator
def load_rentals_file(filename):
    """Read input file and parse its JSON."""
    logging.debug("Reading input data from %s", filename)
    try:
        with open(filename) as file:
            try:
                data = json.load(file)
            except json.decoder.JSONDecodeError as e:
                logging.critical("Error when reading JSON from file: %s", e)
                exit(1)
        return data
    except IOError:
        logging.critical("Unable to open file %s", filename)
        exit(1)


@logging_decorator
def calculate_additional_fields(data):
    """Parse input data to populate additional output fields."""
    logging.debug("Parsing additional fields from input data")
    for key, value in data.items():
        logging.debug("Parsing value: %s", value)

        # parse start and end dates
        try:
            rental_start = datetime.strptime(value['rental_start'], '%m/%d/%y')
            logging.debug("rental_start = %s", rental_start)
        except ValueError as e:
            logging.error("Product '%s' has improper start date: %s", key, e)
            continue
        try:
            rental_end = datetime.strptime(value['rental_end'], '%m/%d/%y')
            logging.debug("rental_end = %s", rental_end)
        except ValueError as e:
            logging.error("Product '%s' has improper end date: %s", key, e)
            continue

        # sanity check date order
        if rental_start > rental_end:
            logging.error("Product '%s' has a start date after its end date",
                          key)
            continue

        # parse remaining values
        try:
            value['total_days'] = (rental_end - rental_start).days
            logging.debug("value['total_days'] = %s", value['total_days'])
            value['total_price'] = value['total_days'] * value['price_per_day']
            logging.debug("value['total_price'] = %s", value['total_price'])
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            logging.debug("value['sqrt_total_price'] = %s",
                          value['sqrt_total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except ValueError as e:
            # catchall error message for unanticipated failure states
            logging.critical("Unexpected error when parsing: %s", e)
            exit(1)

    return data


@logging_decorator
def save_to_json(filename, data):
    """Write output JSON to file."""
    logging.debug("Writing output data to %s", filename)
    try:
        with open(filename, 'w') as file:
            json.dump(data, file)
    except IOError:
        logging.critical("Unable to write output to file %s", filename)
        exit(1)


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    DATA = load_rentals_file(ARGS.debug, ARGS.input)
    DATA = calculate_additional_fields(ARGS.debug, DATA)
    save_to_json(ARGS.debug, ARGS.output, DATA)
