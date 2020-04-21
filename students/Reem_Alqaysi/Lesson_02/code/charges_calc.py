
"""
Returns total price paid for individual rentals
"""
import argparse
import json
import datetime
import math
import logging


def init_logger(level):
    """Initialize settings for log file"""
    # Name of the log file with time stamp
    log_file = 'charges_calc' + datetime.datetime.now().strftime("%Y-%m-%d") + '.log'
    # log format
    log_format = "%(asctime)s%(filename)s:%(lineno)-3d%(levelname)s %(message)s"
    # Create a formatter using format string
    formatter = logging.Formatter(log_format)

    # Create a log message handler that sends output to the log_file
    file_handler = logging.FileHandler(log_file)
    # Set the formatter for this log message handler to the formatter created above
    file_handler.setFormatter(formatter)

    # Add console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Get the root logger
    logger = logging.getLogger()
    # Add handler to the root logger's handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # No debug messages or log file, default
    logger.setLevel(logging.CRITICAL)
    if int(level) == 1:
        # Only error messages
        logger.setLevel(logging.ERROR)
        file_handler.setLevel(logging.ERROR)
        console_handler.setLevel(logging.ERROR)
    elif int(level) == 2:
        # Error messages and warnings
        logger.setLevel(logging.WARNING)
        file_handler.setLevel(logging.WARNING)
        console_handler.setLevel(logging.WARNING)
    elif int(level) == 3:
        # Error messages, warnings, and debug messages
        logger.setLevel(logging.DEBUG)
        file_handler.setLevel(logging.WARNING)
        console_handler.setLevel(logging.DEBUG)


def parse_cmd_arguments():
    """
    Gather arguments from command line. Debug level defaults to 0 if not provided
    """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='output JSON file', required=True)
    parser.add_argument('-d', '--debug', help='debug level', required=False, default=0)

    return parser.parse_args()


def load_rentals_file(filename):
    """
    Open passed filename and use json.load to read to read_data object and return it
    Critical error is logged and program exited if file not found or incorrect value
    """
    try:
        with open(filename) as file:
            read_data = json.load(file)
    except FileNotFoundError:
        logging.critical("Can't find '%s'", filename)
        logging.debug("Error in load_rentals_file()")
        exit(0)
    except ValueError:
        logging.critical("'%s' is either empty or in the wrong format", filename)
        logging.debug("Error in load_rentals_file")
        exit(0)
    return read_data


def calculate_additional_fields(data):
    """ calculate rental data """
    logging.debug("Calculating additional rental data...")

    for key, value in data.items():
        # get rental start date
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
        except ValueError:
            logging.error("Invalid date format for rental start")

        # get rental end date
        try:
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
        except ValueError:
            logging.error("Invalid date format for rental end")

        if rental_start > rental_end:
            logging.warning("Start date cannot be after end date, Rental start date: %s ,Rental end date: %s ", rental_start, rental_end)
        # calculate total rental days
        value['total_days'] = (rental_end - rental_start).days
        # calculate total rental price
        value['total_price'] = value['total_days'] * value['price_per_day']
        logging.debug("Total rental price: %s", value['total_price'])

        # calculate square root of the total rental price
        try:
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
        except ValueError:
            logging.error("Could not compute square root price for %s (value error)", key)
        except KeyError:
            logging.error("Could not compute square root of %s (key error)", key)

        # calculate unit rental cost
        try:
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except ZeroDivisionError:
            logging.error("Could not compute unit cost of %s (divide by 0 error)", key)

    return data

def save_to_json(filename, input_data):
    """Save info from input_data to filename in json format"""
    with open(filename, 'w') as file:
        json.dump(input_data, file)


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    init_logger(ARGS.debug)
    DATA = load_rentals_file(ARGS.input)
    DATA = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, DATA)
