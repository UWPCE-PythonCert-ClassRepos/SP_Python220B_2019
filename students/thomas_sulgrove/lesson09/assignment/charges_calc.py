"""
Returns total price paid for individual rentals
"""

import argparse
import json
import datetime
import math
import logging

# Dictionary for debug levels
DEBUG_LEVEL_DICT = {1: logging.ERROR, 2: logging.WARNING, 3: logging.DEBUG}


def parse_cmd_arguments():
    """
    Parse the user inputs
    :return: The user arguments
    """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='output JSON file', required=True)
    parser.add_argument('-d', '--debug', type=int,
                        help='debug level', required=False)
    parser.add_argument('-l', '--logging', type=bool,
                        help='logging', required=False)
    return parser.parse_args()


def setup_logging(logging_level=None):
    """
    Setup logging for the script
    :param logging_level: logging arg from the user, defaults to None
    :return: NOTHING!
    """
    if logging_level:

        # Set up file name and format
        log_file_name = datetime.datetime.now().strftime("%Y-%m-%d")+'.log'
        log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
        formatter = logging.Formatter(log_format)

        # set up console logging
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # Set up file logging
        file_handler = logging.FileHandler(log_file_name)
        file_handler.setFormatter(formatter)

        # Engage the logging
        logger = logging.getLogger()
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        # Get the level from the dictionary and pass into logger
        debug_level = DEBUG_LEVEL_DICT[logging_level]
        console_handler.setLevel(debug_level)
        logger.setLevel(debug_level)

        # Set the file level to be warning at the min or the level selected if higher.
        # debug writes to file still
        file_handler.setLevel(DEBUG_LEVEL_DICT[2])
        return

    # If Logging arg is None then disable
    logging.disable(logging.CRITICAL)


def logging_switch(func):
    """decorator to disable logging"""
    def wrapper(*args, **kwargs):
        logging.disabled = not ARGS.logging
        return func(*args, **kwargs)
    return wrapper


@logging_switch
def load_rentals_file(filename):
    """
    Load the file that the user inputs
    :param filename: file name that the user has imputed
    :return: the data from the json file
    """
    with open(filename) as file:
        try:
            data = json.load(file)
        except FileNotFoundError:
            exit(0)
    return data


@logging_switch
def calculate_additional_fields(data):
    """
    Do all the calculations from the input file.
    :param data: data from the json the user imputed
    :return: data plus the additional fields
    """
    for key, value in data.items():
        logging.debug("Processing value: %s", value)
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            logging.debug("Processed rental_start as: %s", rental_start)

            # Some end dates are empty
            if not value['rental_end']:
                logging.warning("Skipping %s, rental is still ongoing or data entry error", key)
                continue
            else:
                rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
                logging.debug("Processed rental_end as: %s", rental_end)

            # some end dates come before the start date
            if (rental_end - rental_start).days < 0:
                logging.warning("Skipping %s, has start date greater than end date", key)
                continue
            else:
                value['total_days'] = (rental_end - rental_start).days
                logging.debug("Processed total_days as: %s", value['total_days'])

            value['total_price'] = value['total_days'] * value['price_per_day']
            logging.debug("Processed total_price as: %s", value['total_price'])

            value['sqrt_total_price'] = round(math.sqrt(value['total_price']), 2)
            logging.debug("Processed sqrt_total_price as: %s", value['sqrt_total_price'])

            value['unit_cost'] = value['total_price'] / value['units_rented']
            logging.debug("Processed unit_cost as: %s", value['unit_cost'])
        except ValueError:
            logging.critical("Failed processing value: %s", value)
            exit(0)
    return data


@logging_switch
def save_to_json(filename, data):
    """
    Save the file with the new data tho the file that the user has specified
    :param filename: User specified filename
    :param data: data from input file plus the additional fields
    :return: NOTHING!
    """
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    setup_logging(ARGS.debug)
    DATA = load_rentals_file(ARGS.input)
    DATA = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, DATA)
