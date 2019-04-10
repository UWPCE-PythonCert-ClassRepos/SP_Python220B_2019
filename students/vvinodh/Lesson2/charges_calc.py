'''
Returns total price paid for individual rentals 
'''
import argparse
import json
import datetime
import math
import logging

def init_logger(level):
    """Initialize setting for log file"""
    #Converting string input ot integer to interpret as log level
    level = int(level)

    #Using the following format for your log messages per requirement
    log_format = ("%(asctime)s %(filename)s:%(lineno)-3d"
                  "%(levelname)s %(message)s")

    #Use the following filename format to timestamp your log files
    log_file = datetime.datetime.now().strftime('%Y-%m-%d')+'.log'
    formatter = logging.Formatter(log_format)


    # Handling level 2
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(formatter)

    # Add console handler & handles to logger
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # If condition handles log level 0 through 3 and zero has no debug message

    if level == 0:
        logger.disabled = True
        file_handler.disabled = True

    # 1: Only error messages.
    elif level == 1:
        logger.setLevel(logging.ERROR)
        console_handler.setLevel(logging.ERROR)
        file_handler.setLevel(logging.ERROR)

    # 2: Error messages and warnings.
    elif level == 2:
        logger.setLevel(logging.WARNING)
        console_handler.setLevel(logging.WARNING)
        file_handler.setLevel(logging.WARNING)

    # 3: Error messages, warnings and debug messages.

    elif level == 3:
        logger.setLevel(logging.DEBUG)
        console_handler.setLevel(logging.DEBUG)
        file_handler.setLevel(logging.WARNING)


def parse_cmd_arguments():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='output JSON file', required=True)
    parser.add_argument('-d', '--debug', help='debug level',\
                        required=False, default=0)

    return parser.parse_args()


def load_rentals_file(filename):
    '''
    Load input file
    '''
    try:
        with open(filename) as file:
            data = json.load(file)
    except FileNotFoundError:
        logging.error("Can't locate requested file")
        logging.debug("Occurred in load_rentals_file method")
    except ValueError:
        logging.error("Missing data in file")
        logging.debug("Occurred in load_rentals_file method")
    return data

def calculate_additional_fields(data):
    '''
    Calculate additional fields based on source.json file
    '''
    for key, value in data.items():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
        except ValueError:
            logging.warning("rental start date mismatch 'm/d/y' format in %s", key)
            logging.debug("Track calculate_additional_fields")
        try:
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
        except ValueError:
            logging.warning("rental end date mismatch 'm/d/y' format in %s", key)
            logging.debug("Track calculate_additional_fields")
        value['total_days'] = (rental_end - rental_start).days
        if value['total_days'] < 0:
            logging.warning("rental start is before the rental end in %s", key)
            logging.debug("Track calculate_additional_fields")
        try:
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except ValueError as ex:
            if "math domain error" in str(ex):
                logging.warning('''total_price is negative: %s for %s, sqrt_total_price \
    and unit_cost may be omitted''', value["total_price"], key)
                logging.debug("Track calculate_additional_fields")
            elif 'does not match format' in str(ex):
                logging.warning(ex)
                logging.debug("Track calculate_additional_fields")
    return data


def save_to_json(filename, data):

    '''
    Save results to JSON file
    '''
    try:
        with open(filename, 'w') as file:
            json.dump(data, file)
    except FileNotFoundError:
        logging.error("Missing file")
        logging.debug("Track load_rentals_file")

if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    init_logger(ARGS.debug)
    CALC = calculate_additional_fields(load_rentals_file(ARGS.input))
    save_to_json(ARGS.output, CALC)
