'''
Returns total price paid for individual rentals
'''
import argparse
import json
import datetime
import math
import logging
import sys


def logger_decorator(func):
    """decorator for logger"""
    def debugging_function(level, *args):
        """this is debugging function"""
        log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
        formatter = logging.Formatter(log_format)

        switcher = {0: logging.CRITICAL,
                    1: logging.ERROR,
                    2: logging.WARNING,
                    3: logging.DEBUG}

        mylevel = switcher.get(int(level), "invalid choice")

        if mylevel == "invalid choice":
            print('Invalid Debug Level, Please enter a number from 0 to 3')
            sys.exit()

        log_file = datetime.datetime.now().strftime("%Y-%m-%d") + '.log'
        if int(level) != 0:
            #To prevent log file creating if not requested.
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.WARNING) #always will be warning or above
            file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(mylevel)
        console_handler.setFormatter(formatter)

        logger = logging.getLogger()
        logger.setLevel(mylevel)
        if int(level) != 0:
            #To prevent log file creating if not requested.
            logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return func(*args)
    return debugging_function



def parse_cmd_arguments():
    """takes arguments for the start of the script"""
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='debug level', required=False, default='0')

    return parser.parse_args()


@logger_decorator
def load_rentals_file(filename):
    """source file is loaded to a variable"""
    with open(filename) as file:
        try:
            data = json.load(file)
        except FileNotFoundError as error:
            logging.error(error)
            logging.debug("No file found")
            data = None
    return data


@logger_decorator
def calculate_additional_fields(data):
    """takes in the data and parse for date duration and etc"""
    for value in data.values():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
        except ValueError as error:
            logging.warning("Missing Data")
            logging.warning(error)
            logging.debug(value)
        value['total_days'] = (rental_end - rental_start).days
        value['total_price'] = value['total_days'] * value['price_per_day']
        if value['total_price'] < 0:
            logging.debug("The total price is negative.")
            logging.warning("rental end date is earlier than rental start")
        try:
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
        except ValueError:
            logging.error("Square root of negative number is not allowed. Check total_price")
            logging.debug(value)
            logging.debug("the total value is %i", value['total_price'])
        try:
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except ZeroDivisionError as error:
            logging.error("Dividing by zero is not allowed")
            logging.debug(value)
            logging.debug(value['units_rented'])

    return data


def save_to_json(filename, data):
    """this fuction saves the output to a file"""
    with open(filename, 'w') as file:
        json.dump(data, file)


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    #debugging_function(ARGS.debug)
    DATA = load_rentals_file(ARGS.debug, ARGS.input)
    DATA = calculate_additional_fields(ARGS.debug, DATA)
    save_to_json(ARGS.output, DATA)
