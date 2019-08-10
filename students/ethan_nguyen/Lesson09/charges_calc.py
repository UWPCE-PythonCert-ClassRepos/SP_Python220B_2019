'''
Returns total price paid for individual rentals
'''
# pylint: disable=line-too-long, c0301
import argparse
import json
import datetime
import math
import logging


def parse_cmd_arguments():
    """
    function to parse input and check for input requirements
    """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file',
                        required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file',
                        required=True)
    parser.add_argument('-d', '--debug', help='logging for debug',
                        required=True)

    return parser.parse_args()

ARGS = parse_cmd_arguments()
LOGLEV = int(ARGS.debug)


def logger_decorator(level):
    """
    decorator for the logger
    """
    def logged_func(func):
        """
        set up logger
        """
        def wrapper(*args):
            """
            function to set up logger and handler
            """
            logger = logging.getLogger()
            # create a logger object
            if level > 0:
                if level == 1:
                    logger.setLevel(logging.ERROR)
                elif level == 2:
                    logger.setLevel(logging.WARNING)
                else:
                    logger.setLevel(logging.DEBUG)
            else:
                logging.disable(logging.ERROR)  # disable all logging

            log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s \
                            %(message)s"

            formatter = logging.Formatter(log_format)

            log_file = datetime.datetime.now().strftime("%Y-%m-%d")+".log"
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            file_handler.setLevel(logging.WARNING)

            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            console_handler.setFormatter(formatter)

            logger.addHandler(file_handler)
            logger.addHandler(console_handler)

            if args:
                print("\twith args: {}".format(args))
            print("Function {} called".format(func.__name__))
            return func(*args)
        return wrapper

    return logged_func


@logger_decorator(LOGLEV)
def load_rentals_file(filename):
    """
    function to check and load json file
    """
    logging.debug("Load input json file")
    try:
        with open(filename) as file:
            try:
                data = json.load(file)
            except ValueError:
                logging.error("Decoding JSON has failed")
                exit(0)
    except FileNotFoundError:
        logging.error(f"File {filename} not found")
        exit(0)

    return data


@logger_decorator(LOGLEV)
def calculate_additional_fields(data):
    """
    function to loop through json data and calculate required fields
    """
    logging.debug("Start calculating additional fields")
    for value in data.values():
        logging.debug(f"Proccessing record {value}")

        try:
            rental_start = datetime.datetime.strptime(
                value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(
                value['rental_end'], '%m/%d/%y')
            total_day = (rental_end - rental_start).days
            if total_day < 0:
                logging.warning("Negative total day.  Let take absolute of it")
                total_day = abs(total_day)
            if total_day == 0:
                logging.warning(f"Rental start and end date are the same.  Let set \
                            total rental days to 1 {value}")
                total_day = 1
            value['total_days'] = total_day
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except ValueError:
            logging.warning(f"Missing rental start or end date. Value was {value}. \
                            Skipped this record gracefully.")
            continue
        except ZeroDivisionError:
            logging.warning(f"Tried to divide by zero. Value was {value}. Recovered \
                            gracefully.")
            continue
    return data


@logger_decorator(LOGLEV)
def save_to_json(filename, data):
    """
    function to save json to disk
    """
    logging.debug("Save output to json")
    try:
        with open(filename, 'w') as file:
            json.dump(data, file)
    except IOError:
        logging.error(f"Problem dumping {filename} file")
        exit(0)


if __name__ == "__main__":

    DATA = load_rentals_file(ARGS.input)
    DATA = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, DATA)
