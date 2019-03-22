'''
Returns total price paid for individual rentals
'''
import argparse
import json
import datetime
import math
import logging


def init_logger(level):
    """sets up logger"""
    # Convert string to int for log level
    level = int(level)

    # Format log
    log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s \
                    %(message)s"
    log_file = datetime.datetime.now().strftime('%Y-%m-%d')+'.log'

    # Attach formater
    formatter = logging.Formatter(log_format)

    # Add file handler and only log to file
    # when level is WARNING or above
    file_handler = logging.FileHandler(log_file)
#    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(formatter)

    # Add console handler
    console_handler = logging.StreamHandler()
#    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    # Add handles to logger
    logger = logging.getLogger()
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Setup log level according to user selection
    # 0: No debug messages or log file.
    if level == 0:
        logger.setLevel(logging.CRITICAL)

    # 1: Only error messages.
    if level == 1:
        logger.setLevel(logging.ERROR)
        console_handler.setLevel(logging.ERROR)
        file_handler.setLevel(logging.ERROR)

    # 2: Error messages and warnings.
    elif level == 2:
        logger.setLevel(logging.WARNING)
        console_handler.setLevel(logging.WARNING)

    # 3: Error messages, warnings and debug messages.
    elif level == 3:
        logger.setLevel(logging.DEBUG)
        console_handler.setLevel(logging.DEBUG)


def parse_cmd_arguments():
    '''
    Parse command line arguments
    '''
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='debug level', required=True)

    return parser.parse_args()


def load_rentals_file(filename):
    '''
    Load input file
    '''
    with open(filename) as file:
        try:
            data = json.load(file)
        except ValueError as ex:
            logging.error(ex)
    return data


def calculate_additional_fields(data):
    '''
    Calculate additional fields based on source.json file
    '''
    for value in data.values():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'],
                                                      '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'],
                                                    '%m/%d/%y')
            value['total_days'] = (rental_end - rental_start).days
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except ValueError as ex:
            if "math domain error" in str(ex):
                logging.error('total_price is negative: %s',
                              value['total_price'])
#                              + str(value['total_price']))
            elif 'does not match format' in str(ex):
                logging.warning(ex)

    return data


def save_to_json(filename, data):
    '''
    Save results to JSON file
    '''
    with open(filename, 'w') as file:
        json.dump(data, file)


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    init_logger(ARGS.debug)
#    logging.debug(ARGS)
    DATA = load_rentals_file(ARGS.input)
    RESULT = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, RESULT)
