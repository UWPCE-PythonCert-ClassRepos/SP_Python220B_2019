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

    # Setup the console log handler with level to debug as general debug information
    # should always go to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    # Create the logger not concerned about the log level as it will be controlled via each handler
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def parse_cmd_arguments():
    """ Parse input """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='output JSON file', required=True)
    parser.add_argument('-d', '--debug', default=0, help='set the debug level', required=False)

    return parser.parse_args()


def load_rentals_file(filename):
    """ Read the data from the supplied json file
    :param filename: json file containing the rental data
    :return dictionary containing the rental data loaded from a json file """

    logging.debug("Trying to open the %s", filename)
    try:
        with open(filename) as file:
            try:
                data = json.load(file)
            except ValueError:
                logging.error("A VALUE ERROR occurred while trying to load the json file.",
                              exc_info=True)
                exit(0)
            except OSError:
                logging.error("An OS Error occurred while trying to load the json file.",
                              exc_info=True)
                exit(0)
    except FileNotFoundError:
        logging.error("A problem occured when trying to open the file:", exc_info=True)
        exit(0)
    return data


def calculate_additional_fields(data):
    """ Return data regarding a rental item
    :param data: dictionary containing the rental data
    :return dictionary containing the processed data """

    logging.debug("Calculating the field data")
    for key, value in data.items():
        logging.debug("Process data for record: %s %s\n", key, value)
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            logging.debug("Rental start date: %s for entry %s", rental_start, key)
        except ValueError:
            logging.error("The entry %s does not contain a valid start date %s:",
                          key, rental_start, exc_info=True)

        try:
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            logging.debug("Rental end date: %s for entry %s", rental_end, key)
        except ValueError:
            logging.error("The entry %s does not contain a valid end date %s:",
                          key, rental_end, exc_info=True)

        value['total_days'] = (rental_end - rental_start).days
        logging.debug("Total days: %s  for entry %s", value['total_days'], key)
        if value['total_days'] < 0:
            logging.error("Total rental days for entry %s is less than 0: %s",
                          key, value['total_days'])

        value['total_price'] = value['total_days'] * value['price_per_day']
        logging.debug("Total rental price: %s for entry %s", value['total_price'], key)

        try:
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            logging.debug("Total square root price: %s for entry %s",
                          value['sqrt_total_price'], key)
        except ValueError:
            logging.error("A VALUE ERROR occurred when trying to calculate the square root of"
                          " the total price %s for entry %s:",
                          value['total_price'], key, exc_info=True)

        try:
            value['unit_cost'] = value['total_price'] / value['units_rented']
            logging.debug("Unit cost: %s for entry %s", value['unit_cost'], key)
        except ZeroDivisionError:
            logging.error("A ZERO DIVISION ERROR occurred when trying to divided the"
                          " %s (total price) by %s (units rented) for entry %s",
                          value['total_price'], value['units_rented'], key)
    return data


def save_to_json(filename, data):
    """ Save rental data to json file """
    logging.debug("Saving the output file: %s", filename)
    try:
        with open(filename, 'w') as file:
            json.dump(data, file)
    except IOError:
        logging.error("An IO ERROR occurred when trying to write the file %s",
                      filename, exc_info=True)


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    setup_logging(ARGS.debug)
    DATA = load_rentals_file(ARGS.input)
    DATA = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, DATA)
