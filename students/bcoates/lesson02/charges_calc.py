'''
Returns total price paid for individual rentals
'''
import argparse
import json
import datetime
import math
import logging

# Disable 'invalid-name' error as global variables are not CONSTANTS
# pylint: disable=invalid-name

def parse_cmd_arguments():
    """ Parse command line arguments """

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='debug log level (0-3)', required=False, default=0)

    return parser.parse_args()

def configure_logger(level):
    """ Configure logging settings based on provided value """

    log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
    log_file = datetime.datetime.now().strftime("%Y-%m-%d")+'.log'
    formatter = logging.Formatter(log_format)
    logger = logging.getLogger()

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    if level == '1':
        logger.setLevel(logging.ERROR)
        file_handler.setLevel(logging.ERROR)
        console_handler.setLevel(logging.ERROR)
    elif level == '2':
        logger.setLevel(logging.WARNING)
        file_handler.setLevel(logging.WARNING)
        console_handler.setLevel(logging.WARNING)
    elif level == '3':
        logger.setLevel(logging.DEBUG)
        file_handler.setLevel(logging.WARNING)
        console_handler.setLevel(logging.DEBUG)

def load_rentals_file(filename):
    """ Loads a JSON file and returns the data """

    try:
        with open(filename) as file:
            logging.debug("Loading rentals file")
            data = json.load(file)
    except FileNotFoundError:
        logging.error("Error loading file")
        exit(1)
    except json.decoder.JSONDecodeError:
        logging.error("Source file has invalid JSON")
        exit(1)

    return data

def calculate_additional_fields(data):
    """ Calculate additional data based on imported values """

    for key, value in data.items():
        logging.debug("Processing record:  %s", key)
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
        except ValueError:
            logging.warning("Date missing or improper format")

        try:
            logging.debug("Calculating pricing data")
            value['total_days'] = (rental_end - rental_start).days
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
            logging.debug("Successfully calculated pricing data")
        except ValueError:
            logging.warning("Rental start date (%s) is later than end date (%s)", \
                value['rental_start'], value['rental_end'])

    return data

def save_to_json(filename, data):
    """ Save the updated data to a file """

    try:
        logging.debug("Saving file to disk")
        with open(filename, 'w') as file:
            json.dump(data, file)
    except IOError:
        logging.error("Unable to save file")
        exit(1)

if __name__ == "__main__":
    args = parse_cmd_arguments()
    configure_logger(args.debug)
    input_data = load_rentals_file(args.input)
    output_data = calculate_additional_fields(input_data)
    save_to_json(args.output, output_data)
