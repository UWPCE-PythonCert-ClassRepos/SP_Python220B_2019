'''
Returns total price paid for individual rentals
'''
import argparse
import json
import datetime
import math
import logging
import sys

logger = logging.getLogger(__name__)

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
formatter = logging.Formatter(LOG_FORMAT)
log_file = datetime.datetime.now().strftime("%Y-%m-%d")+'.log'
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(formatter)

def logging_level(original_function):
    """
    sets log levels by taking a single argument
    and matching it to key in the dictionary
    """
    levels = {
        0: logging.NOTSET,
        1: logging.ERROR,
        2: logging.WARNING,
        3: logging.DEBUG
    }

    def logger_func(*args, **kwargs):
        """
        inner function to handle logging levels
        """
        if cli_args.debug:
            try:
                # debug arg found and passing the
                # integer to the logging_level method
                level = levels[cli_args.debug]
                if level == 10:
                    logger.setLevel(level)
                    console_handler = logging.StreamHandler(sys.stdout)
                    console_handler.setFormatter(formatter)
                    logger.addHandler(console_handler)
                else:
                    logger.setLevel(level)
                    logger.addHandler(file_handler)
            except KeyError:
                # If the debug value does not match
                # a key in the log level dict then exit
                # and log the reason for exiting
                logger.setLevel(logging.ERROR)
                logger.addHandler(file_handler)
                logger.error(f"Invalid debug option")
                sys.exit()
            else:
                data = load_rentals_file(cli_args.input)
                data = calculate_additional_fields(data)
        else:
            logger.disabled = True
            data = load_rentals_file(cli_args.input)
            data = calculate_additional_fields(data)
            save_to_json(cli_args.output, data)

        return original_function(*args, **kwargs)

    return logger_func

def parse_cmd_arguments():
    """ Setups parser and returns arguments from the command line """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', type=int, help='logging verbosity', required=False)

    return parser.parse_args()

# @logging_level   
def load_rentals_file(filename=None):
    """ loads the file in json format from a file and returns it as a json object """
    try:
        with open(filename) as file:
            data = json.load(file)
            logger.info(f"file {filename} was loaded successfully")
    except FileNotFoundError:
        logger.error(f"File \"{filename}\" was not found ")
        sys.exit()

    return data

# @logging_level
def calculate_additional_fields(data):
    """ runs calculations based on data input from source file """
    for value in data.values():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            logger.debug(f"rental start: {value['rental_start']}")

            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            logger.debug(f"rental end: {value['rental_end']}")

            # ensure that total days is always positive
            value['total_days'] = abs((rental_end - rental_start).days)
            logger.debug(f"total days: {value['total_days']}")

            # added check to catch this issue of having the start data
            # after the end date, logged the reason, and continued
            if rental_end < rental_start:
                logger.warning(f"rental end is before rental start date")
                # correct the start and end dates
                switch_start = value['rental_end']
                switch_end = value['rental_start']
                value['rental_end'] = switch_end
                value['rental_start'] = switch_start

            value['total_price'] = value['total_days'] * value['price_per_day']
            logger.debug(f"total price: {value['total_price']}")

            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            logger.debug(f"square root price {value['sqrt_total_price']}")

            # Prevent evaluation from breaking when no units rented
            if value['units_rented'] <= 0:
                value['unit_cost'] = 0
                logger.warning(f"no units rented setting unit cost to zero")
            else:
                value['unit_cost'] = value['total_price'] / value['units_rented']

        except ValueError as value_error:
            logger.error(f"Value error caught: {value_error}")
            logger.error(f"Empty value found in {value}")

    return data

# @logging_level
def save_to_json(filename, data):#, debug=None):
    """ writes output to a file in json format """
    with open(filename, 'w') as file:
        logger.debug(f"writing {data} to file")
        json.dump(data, file)
        logger.info(f"file successfully written to {filename}")

# @logging_level
# def test_logging(cli_args):
#     print(f"decorated function")
#     logger.info(f"info logs")
#     logger.warning(f"log level warning logs")
#     logger.debug(f"debug logs")


if __name__ == "__main__":
    cli_args = parse_cmd_arguments()
    test_logging(cli_args)