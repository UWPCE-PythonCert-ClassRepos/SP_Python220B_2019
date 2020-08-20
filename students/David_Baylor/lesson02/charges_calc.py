'''
Returns total price paid for individual rentals
'''
import argparse
import json
import datetime
import math
import logging


def none():
    """
    returns a 50 setting only critical messages to be shown.
    This disables all logging messages
    """
    return 50
def errs():
    """returns 40 setting only errors to be shown"""
    return 40
def errs_warnings():
    """returns 30 setting errors and warnings to be shown"""
    return 30
def errs_warnings_debug():
    """returns 10 displaying everyething from debug up."""
    return 10

debug_options = {"0": none,
                 "1": errs,
                 "2": errs_warnings,
                 "3": errs_warnings_debug}

def debug_setting(level):
    """sets the debugger level"""
    return debug_options.get(level)()

def parse_cmd_arguments():
    """parses the arguments passed in from the comand line"""
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='debuger setting', default="0")

    return parser.parse_args()


def load_rentals_file(filename):
    """opens the rental files with the input data"""
    try:
        with open(filename) as file:
            try:
                data = json.load(file)
                logging.debug("Input file opened")
            except json.decoder.JSONDecodeError:
                logging.error("Input file not json")
    except FileNotFoundError:
        logging.error("Input file not found")
    return data

def calculate_additional_fields(data):
    """calculates additional feilds of data"""
    for key in data.keys():
        value = data[key]
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            value['total_days'] = (rental_end - rental_start).days
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except ValueError:
            logging.error("Rental %s end date before start date. Tried to take the squair root of"\
                " a negetive number.", key)
        except ZeroDivisionError:
            logging.error("Rental %s number of units rented is 0. Tried to divide by 0.", key)
        except KeyError:
            logging.warning("Missing data in rental %s", key)

    logging.debug("All aditional data calculated.")
    return data

def save_to_json(filename, data):
    """saves the new data to an output file"""
    with open(filename, 'w') as file:
        json.dump(data, file)
    logging.debug("Output file created.")

if __name__ == "__main__":
    args = parse_cmd_arguments()

    LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
    log_file = datetime.datetime.now().strftime("%Y-%m-%d")+'.log'

    formatter = logging.Formatter(LOG_FORMAT)

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)


    logger = logging.getLogger()
    logger.setLevel(debug_setting(args.debug))
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


    DATA = load_rentals_file(args.input)
    DATA = calculate_additional_fields(DATA)
    save_to_json(args.output, DATA)
