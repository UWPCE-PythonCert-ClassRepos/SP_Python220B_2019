'''
Returns total price paid for individual rentals
'''
import argparse
import json
import datetime
import math
import logging


LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
FORMATTER = logging.Formatter(LOG_FORMAT)

LOG_FILE = datetime.datetime.now().strftime('%Y-%m-%d') + '.log'
FILE_HANDLER = logging.FileHandler(LOG_FILE)
#file_handler.setLevel(logging.WARNING)
FILE_HANDLER.setFormatter(FORMATTER)

CONSOLE_HANDLER = logging.StreamHandler()
#console_handler.setLevel(logging.DEBUG)
CONSOLE_HANDLER.setFormatter(FORMATTER)

LOGGER = logging.getLogger()
#logger.setLevel(logging.DEBUG)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLE_HANDLER)


def parse_cmd_arguments():
    """Pass in JSON file, name the output file, select level of debug in command line"""

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help="enter desired debug level",
                        required=False, default=0)


    return parser.parse_args()

def load_rentals_file(filename):
    """Open JSON file, log error if not found"""

    try:
        with open(filename) as file:
            logging.debug('JSON file: {}'.format(filename))
            data = json.load(file)
    except FileNotFoundError:
        #log an error if file is not found
        logging.error("File not found")
        exit(0)
    return data

def calculate_additional_fields(data):
    """Checking values in JSON, calculating total days,
       total price, sqrt total price, & unit cost"""

    for value in data.values():
        try:
            logging.info("Called with value: {}".format(value))

            #logs a warning if no rental end date is available
            if value['rental_start'] == '':
                logging.warning("Missing rental start date")
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            #logs the rental start date
            logging.debug('Rental start: {}'.format(value['rental_start']))

            #logs a warning if no rental end date is available
            if value['rental_end'] == '':
                logging.warning("Missing rental end date")
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            #logs the rental end date
            logging.debug('Rental ends: {}'.format(value['rental_end']))

            value['total_days'] = (rental_end - rental_start).days
            #logs total days
            logging.debug('Total days: {:d}'.format(value['total_days']))

            value['total_price'] = value['total_days'] * value['price_per_day']
            #logs the total price
            logging.debug('Total price: ${:,.2f}'.format(value['total_price']))

            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            #logs square root of total price
            logging.debug('Square root of total price: {:06.2f}'.format(value['sqrt_total_price']))

            value['unit_cost'] = value['total_price'] / value['units_rented']
            logging.debug('Unit cost: ${:,.2f}'.format(value['unit_cost']))
        except ValueError:
            #logs an error if total days are negative, resulting in attempting to find square
            #root of a negative number
            logging.error("Total days must not be negative; end date is before start date")

    return data

def save_to_json(filename, data):
    """Save new Values to JSON file"""

    with open(filename, 'w') as file:
        json.dump(data, file)

if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    if ARGS.debug == '0':
        LOGGER.disabled = True
    elif ARGS.debug == '1':
        FILE_HANDLER.setLevel(logging.ERROR)
        CONSOLE_HANDLER.setLevel(logging.ERROR)
        LOGGER.setLevel(logging.ERROR)
    elif ARGS.debug == '2':
        FILE_HANDLER.setLevel(logging.WARNING)
        CONSOLE_HANDLER.setLevel(logging.WARNING)
        LOGGER.setLevel(logging.WARNING)
    elif ARGS.debug == '3':
        #From assignment: Debug: General comments, indicating where in the script flow we are.
        #Should be shown on screen only (i.e., never saved to logfile).
        FILE_HANDLER.setLevel(logging.WARNING)
        CONSOLE_HANDLER.setLevel(logging.DEBUG)
        LOGGER.setLevel(logging.DEBUG)
    else:
        logging.debug("User entered {}".format(ARGS.debug))
        logging.error("User must select 0, 1, 2, or 3")
        raise ValueError


    DATA_1 = load_rentals_file(ARGS.input)
    DATA_1 = calculate_additional_fields(DATA_1)
    save_to_json(ARGS.output, DATA_1)
    