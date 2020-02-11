'''
Returns total price paid for individual rentals

charges_calc.py
joli umetsu
py220
'''
import argparse
import json
import datetime
import math
import logging
import sys


# define dictionary of debug levels
DEBUG_LEVEL = {'0': logging.CRITICAL, '1': logging.ERROR, '2': logging.WARNING, '3': logging.DEBUG}

def setup_logging(level):
    """ set console and file logging levels based on user passed in arguments """

    # given format for log messages
    log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
    formatter = logging.Formatter(log_format)

    # given filename format for log files
    log_file = datetime.datetime.now().strftime("%Y-%m-%d")+'.log'

    # set up log message handler sent to file with level input
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(formatter)

    # set up console log message; level of message set to debug (always shown on screen)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(DEBUG_LEVEL[level])
    console_handler.setFormatter(formatter)

    # set up root handler and add file and console handlers
    logger = logging.getLogger()
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

def parse_cmd_arguments():
    """ parse user inputs """

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='debug level', required=False, default='0')

    return parser.parse_args()


def load_rentals_file(filename):
    """ load the input file with rental data """
    logging.debug("Loading input file %s...", filename)

    try:
        with open(filename) as file:
            try:
                data = json.load(file)
            except ValueError:
                logging.error("Could not locate input file (value error)")
                sys.exit()
    except FileNotFoundError:
        logging.error("Could not locate input file (file did not exist)")
        sys.exit()

    return data

def calculate_additional_fields(data):
    """ calculate rental data """
    logging.debug("Calculating additional rental data...")

    for key, value in data.items():
        logging.debug("*** Processing data for rental %s...***", key)

        # get rental start date
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            logging.debug("[Rental start date: %s...]", rental_start)
        except ValueError:
            logging.error("Invalid date format for rental start")

        # get rental end date
        try:
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            logging.debug("[Rental end date: %s...]", rental_end)
        except ValueError:
            logging.error("Invalid date format for rental end")

        if rental_start > rental_end:
            logging.warning("Start date cannot occur after end date")

        # calculate total rental days
        value['total_days'] = (rental_end - rental_start).days
        logging.debug("Total rental days: %s", value['total_days'])

        # calculate total rental price
        value['total_price'] = value['total_days'] * value['price_per_day']
        logging.debug("Total rental price: %s", value['total_price'])

        # calculate square root of the total rental price
        try:
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            logging.debug("Sqrt rental price: %s", value['sqrt_total_price'])
        except ValueError:
            logging.error("Could not compute square root price for %s (value error)", key)
        except KeyError:
            logging.error("Could not compute square root of %s (key error)", key)

        # calculate unit rental cost
        try:
            value['unit_cost'] = value['total_price'] / value['units_rented']
            logging.debug("Unit cost: %s", value['unit_cost'])
        except ZeroDivisionError:
            logging.error("Could not compute unit cost of %s (divide by 0 error)", key)

    return data


def save_to_json(filename, data):
    """ save the output file """
    logging.debug("Saving output file %s...", filename)

    with open(filename, 'w') as file:
        json.dump(data, file)

if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    LOGGER = setup_logging(ARGS.debug)
    logging.debug("Arguments %s passed in...", ARGS)
    LOGGER.setLevel(DEBUG_LEVEL[ARGS.debug])
    DATA = load_rentals_file(ARGS.input)
    DATA = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, DATA)
