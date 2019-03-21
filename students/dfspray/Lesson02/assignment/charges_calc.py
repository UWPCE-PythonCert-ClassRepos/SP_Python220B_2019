'''
Returns total price paid for individual rentals
'''
import argparse
import json
import datetime
import math
import logging

def init_logger(level):
    """Creates a method for initiating the log file and settings"""

    # Convert string to int for log level
    level = int(level)

    # Format log
    log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
    log_file = datetime.datetime.now().strftime('%Y-%m-%d')+'.log'

    # Attach formater
    formatter = logging.Formatter(log_format)

    # Add file handler and only log to file
    # when level is WARNING or above
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(formatter)

    # Add console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    # Add handles to logger
    logger = logging.getLogger()
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Setup log level according to user selection
    # 0: No debug messages or log file.
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
    # Debug messages don't output to log file
    elif level == 3:
        logger.setLevel(logging.DEBUG)
        console_handler.setLevel(logging.DEBUG)
        file_handler.setLevel(logging.WARNING)

def parse_cmd_arguments():
    '''
    Parse command line arguments
    '''
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', nargs='?', const=0,
                        type=int, default=0, help='debug level')

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
            logging.warning("rental start date doesn't match 'm/d/y' format in %s", key)
            logging.debug("Occurred in calculate_additional_fields method")
        try:
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
        except ValueError:
            logging.warning("rental end date doesn't match 'm/d/y' format in %s", key)
            logging.debug("Occurred in calculate_additional_fields method")
        value['total_days'] = (rental_end - rental_start).days
        if value['total_days'] < 0:
            logging.warning("rental start is before the rental end in %s", key)
            logging.debug("Occurred in calculate_additional_fields method")
        try:
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except ValueError as ex:
            if "math domain error" in str(ex):
                logging.warning('total_price is negative: %s for %s', value["total_price"], key)
                logging.debug("Occurred in calculate_additional_fields method")
            elif 'does not match format' in str(ex):
                logging.warning(ex)
                logging.debug("Occurred in calculate_additional_fields method")

    return data

def save_to_json(filename, data):
    '''
    Save results to JSON file
    '''
    try:
        with open(filename, 'w') as file:
            json.dump(data, file)
    except FileNotFoundError:
        logging.error("Can't locate requested file")
        logging.debug("Occurred in load_rentals_file method")

if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    init_logger(ARGS.debug)
    logging.debug(ARGS)
    DATA = load_rentals_file(ARGS.input)
    RESULT = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, RESULT)
