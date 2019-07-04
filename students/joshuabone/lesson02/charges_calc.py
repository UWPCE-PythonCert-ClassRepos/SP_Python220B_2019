"""
Returns total price paid for individual rentals.

Note that logging can be enabled from the command line using the --d or --debug
argument flags with the following options:

0: No debug messages or log file.
1: Only error messages.
2: Error messages and warnings.
3: Error messages, warnings and debug messages.

If logging is enabled, all log messages will be written to a .log file in this
directory named according to the current date, e.g. '2019-01-01.log'.
Additionally, both log and debug (if enabled) messages will be printed to
console.
"""

import argparse
import json
import datetime
import math
import logging

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
DEBUG_LEVELS = {1: logging.ERROR, 2: logging.WARNING, 3: logging.DEBUG}


def parse_cmd_arguments():
    """Parse the command line arguments using the argparse module."""
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='debug level', required=False)

    return parser.parse_args()


def load_rentals_file(filename):
    """Load the rentals file."""
    logging.debug("Opening rentals file: %s", filename)
    with open(filename) as file:
        try:
            local_data = json.load(file)
        except ValueError:
            logging.critical("Could not load rentals file: %s", filename)
            exit(0)
    return local_data


def calculate_additional_fields(local_data):
    """Calculate additional fields."""
    for value in local_data.values():
        logging.debug("Calculating additional fields for %s", value)
        try:
            logging.debug("Parsing rental_start from %s",
                          value['rental_start'])
            rental_start = datetime.datetime.strptime(value['rental_start'],
                                                      '%m/%d/%y')
            logging.debug("Parsed rental_start: %s", rental_start)

            if not value['rental_end']:
                logging.warning("Field rental_end missing for entry %s. "
                                "Skipping additional calculated fields.",
                                value)
                continue

            logging.debug("Parsing rental_end from %s", value['rental_end'])
            rental_end = datetime.datetime.strptime(value['rental_end'],
                                                    '%m/%d/%y')
            logging.debug("Parsed rental_end: %s", rental_end)

            value['total_days'] = (rental_end - rental_start).days
            logging.debug("Calculated total_days: %s", value['total_days'])

            if value['total_days'] < 0:
                logging.warning("Total days was negative for entry %s. "
                                "Skipping additional calculated fields.",
                                value)
                continue

            value['total_price'] = value['total_days'] * value['price_per_day']
            logging.debug("Calculated total_price: %s", value['total_price'])

            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            logging.debug("Calculated sqrt_total_price: %s",
                          value['sqrt_total_price'])

            value['unit_cost'] = value['total_price'] / value['units_rented']
            logging.debug("Calculated unit_cost: %s", value['unit_cost'])
        except ValueError:
            logging.critical("Failed to calculate additional fields for %s",
                             value)
            exit(0)
    return local_data


def save_to_json(filename, data_to_save):
    """Save to JSON format."""
    with open(filename, 'w') as file:
        json.dump(data_to_save, file)


def setup_logging(debug_arg):
    """Sets up the logging from the optional user-supplied argument."""
    if debug_arg is not None and int(debug_arg) in DEBUG_LEVELS.keys():
        formatter = logging.Formatter(LOG_FORMAT)

        log_file_name = datetime.datetime.now().strftime("%Y-%m-%d")+'.log'
        file_handler = logging.FileHandler(log_file_name)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger = logging.getLogger()
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        debug_level = DEBUG_LEVELS[int(debug_arg)]
        console_handler.setLevel(debug_level)
        logger.setLevel(debug_level)

        # Do not send debug messages to file.
        file_handler.setLevel(max(logging.INFO, debug_level))
    else:
        logging.disable(logging.CRITICAL)


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    setup_logging(ARGS.debug)
    DATA = load_rentals_file(ARGS.input)
    DATA = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, DATA)
