'''
Returns total price paid for individual rentals 

charges_calc.py
joli umetsu
py220
'''
import argparse
import json
import datetime
import math
import logging


# define dictionary of debug levels
DEBUG_LEVEL = {'0': logging.CRITICAL, '1': logging.ERROR, '2': logging.WARNING, '3': logging.DEBUG}

def setup_logging(level):
    """ set console and file logging levels based on user passed in arguments """

    # given format for log messages
    log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
    formatter = logging.Formatter(log_format)

    # given filename format for log files
    log_file = datetime.datetime.now().strftime("%Y-%m-%d")+'.log'

    # set up log message handler sent to file with level input
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(formatter)

    # set up console log message; level of message set to debug (always shown on screen)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(DEBUG_LEVEL[level])
    console_handler.setFormatter(formatter)

    # set up root handler and add file and console handlers
    logger = logging.getLogger()
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

def parse_cmd_arguments():
    """ parse user inputs """

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='debug level', required=False, default='0')

    return parser.parse_args()


def load_rentals_file(filename):
    """ load the input file with rental data """
    logging.debug("Loading input file {}...".format(filename))

    try:
        with open(filename) as file:
            try:
                data = json.load(file)
            except ValueError:
                logging.error("Could not locate input file (value error)")
                exit(0)
    except FileNotFoundError:
        logging.error("Could not locate input file (file did not exist)")
        exit(0)

    return data

def calculate_additional_fields(data):
    """ calculate rental data """
    logging.debug("Calculating additional rental data...")

    for key, value in data.items():
        logging.debug("*** Processing data for rental {}...***".format(key))

        # get rental start date
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            logging.debug(f"[Rental start date: {rental_start}...]")
        except ValueError:
            logging.error("Invalid date format for rental start")

        # get rental end date
        try:
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            logging.debug(f"[Rental end date: {rental_end}...]")
        except ValueError:
            logging.error("Invalid date format for rental end")

        if rental_start > rental_end:
            logging.warning("Start date cannot occur after end date")

        # calculate total rental days
        value['total_days'] = (rental_end - rental_start).days
        logging.debug("Total rental days: {}".format(value['total_days']))

        # calculate total rental price
        value['total_price'] = value['total_days'] * value['price_per_day']
        logging.debug("Total rental price: {}".format(value['total_price']))

        # calculate square root of the total rental price
        try:
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            logging.debug("Sqrt rental price: {}".format(value['sqrt_total_price']))
        except ValueError:
            logging.error(f"Could not compute square root price for {key} (value error)")
        except KeyError:
            logging.error(f"Could not compute square root of {key} (key error)")

        # calculate unit rental cost
        try:
            value['unit_cost'] = value['total_price'] / value['units_rented']
            logging.debug("Unit cost: {}".format(value['unit_cost']))
        except ZeroDivisionError:
            logging.error(f"Could not compute unit cost of {key} (divide by 0 error)")

    return data            

def save_to_json(filename, data):
    """ save the output file """
    logging.debug("Saving output file {}...".format(filename))

    with open(filename, 'w') as file:
        json.dump(data, file)

if __name__ == "__main__":
    args = parse_cmd_arguments()
    logger = setup_logging(args.debug)
    logging.debug("Arguments %s passed in...", args)
    logger.setLevel(DEBUG_LEVEL[args.debug])
    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)
