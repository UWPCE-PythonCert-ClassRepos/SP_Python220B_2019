'''
Returns total price paid for individual rentals 
'''
import argparse
import json
import datetime
import math
import logging


def logger_decorator(function):
    """

    :param function:
    :return:
    """
    def init_logger(level,*args,**kwargs):

        """
        Sets logging level
        :param level:
        :return:
        """
        level = int(level)
        log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s \
                        %(message)s"
        log_file = datetime.datetime.now().strftime("%Y-%m-%d") + '.log'
        formatter = logging.Formatter(log_format)

        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger = logging.getLogger()
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        # Level 0: No debug messages or log file.
        if level == 0:
            logger.setLevel(logging.CRITICAL)
        # Level 1: Only error messages.
        elif level == 1:
            logger.setLevel(logging.ERROR)
            console_handler.setLevel(logging.ERROR)
            file_handler.setLevel(logging.ERROR)
        # Level 2: Error messages and warnings.
        elif level == 2:
            logger.setLevel(logging.WARNING)
            console_handler.setLevel(logging.WARNING)
            file_handler.setLevel(logging.WARNING)
        # Level 3: Error messages, warnings and debug messages.
        elif level == 3:
            logger.setLevel(logging.DEBUG)
            console_handler.setLevel(logging.NOTSET)
            file_handler.setLevel(logging.WARNING)
        # Incorrect input
        else:
            print('Invalid Debug Level, Please enter a number from 0 to 3')
            exit(0)
        return function(*args,**kwargs)
    return init_logger

def parse_cmd_arguments():
    """
    Module that defines required arguments
    """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='Debug Level', required=True)
    return parser.parse_args()

@logger_decorator
def load_rentals_file(filename):
    """

    :param filename:
    :return:
    """
    try:
        with open(filename) as file:
            data = json.load(file)
    except FileNotFoundError as error:
        logging.error(error)
        logging.debug('File not found error')
        data = None

    return data

@logger_decorator
def calculate_additional_fields(data):
    """

    :param data:
    :return: data with total days, and price
    """
    if data is None:
        logging.warning('No data found!')
        logging.debug('Data is none in calculate_additional_fields function')
        return None
    for value in data.values():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
        except ValueError as error:
            logging.warning(error)
            logging.debug(value)
        value['total_days'] = (rental_end - rental_start).days
        if value['total_days'] < 0:
            logging.error('total_days is negative, which means your rental_end occurs before start')
            logging.debug('Product Code is: {}'.format(value['product_code']))
            logging.debug('Total days is:{}'.format(value['total_days']))
            logging.debug('Value is:{}'.format(value))
        value['total_price'] = value['total_days'] * value['price_per_day']
        try:
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
        except ValueError as error:
            logging.error("Can't square root negative number. Check total_price")
            logging.debug(value)
            logging.debug(value['total_price'])
        try:
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except ZeroDivisionError as error:
            logging.error("Can't divide by zero")
            logging.debug(value['units_rented'])

    return data

@logger_decorator
def save_to_json(filename, data):
    """
    output results to json
    """
    with open(filename, 'w') as file:
        if data is None:
            logging.debug('There is no data to export')
        json.dump(data, file)


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    logger(ARGS.debug)
    logging.debug(ARGS)
    DATA = load_rentals_file(ARGS.input)
    DATA = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, DATA)
