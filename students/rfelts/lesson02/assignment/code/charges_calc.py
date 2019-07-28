"""
Returns total price paid for individual rentals
"""
import argparse
import json
import datetime
import math
import logging


def setup_logging(log_level):
    """ Setup logging for the console and to a file """

    # Setup the log format
    log_format = "%(asctime)s %(filename)s:%(lineno) - 3d %(levelname)s %(message)s"
    formatter = logging.Formatter(log_format)

    # Set logging level in the handler to
    logging_levels = {0: logging.CRITICAL, 1: logging.ERROR, 2: logging.WARNING, 3: logging.DEBUG}

    # Create the log file
    log_file = datetime.datetime.now().strftime("%Y-%m-%d")+".log"

    # Setup the log file handler with level specified by the user
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging_levels.get(int(log_level)))
    file_handler.setFormatter(formatter)

    # Setup the console log handler with level to debug as general debug information should always go to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    # Create the logger not concerned about the log level as it will be controlled via each handler
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def parse_cmd_arguments():
    """ Return the arguments found in the json file """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='output JSON file', required=True)
    parser.add_argument('-d', '--debug', default=0, help='set the debug level', required=False)

    return parser.parse_args()


def load_rentals_file(filename):
    """ Return the data from the rental file
    :return data from json file """

    logging.debug("Trying to open the %s", filename)
    try:
        with open(filename) as file:
            try:
                data = json.load(file)
            except Exception:
                logging.error("A problem occured when trying to load the file:", exc_info=True)
                exit(0)
    except FileNotFoundError:
        logging.error("A problem occured when trying to open the file:", exc_info=True)
        exit(0)
    return data


def calculate_additional_fields(data):
    """ Return data regarding a rental item
    :return """

    logging.debug("Calculating the field data")
    for value in data.values():
        logging.debug("Process data for record: %s", value)
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            logging.debug("Rental start date: %s", rental_start)

            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            logging.debug("Rental end date: %s", rental_end)

            value['total_days'] = (rental_end - rental_start).days
            logging.debug("Total rental days: %s", value['total_days'])

            value['total_price'] = value['total_days'] * value['price_per_day']
            logging.debug("Total rental price: %s", value['total_price'])

            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            logging.debug("Total square root price: %s", value['sqrt_total_price'])

            value['unit_cost'] = value['total_price'] / value['units_rented']
            logging.debug("Unit cost: %s", value['unit_cost'])

        except:
            exit(0)

    return data


def save_to_json(filename, data):
    """ Save rental data to json file """
    logging.debug("Saving the output file: %s", filename)
    with open(filename, 'w') as file:
        json.dump(data, file)


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    setup_logging(ARGS.debug)
    DATA = load_rentals_file(ARGS.input)
    DATA = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, DATA)
