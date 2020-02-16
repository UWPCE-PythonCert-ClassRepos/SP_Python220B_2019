'''
Returns total price paid for individual rentals
'''
import argparse
import json
import datetime
import math
import logging
import sys

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = datetime.datetime.now().strftime("%Y-%m-%d")+'.log'
FORMATTER = logging.Formatter(LOG_FORMAT)

FH = logging.FileHandler(LOG_FILE)
CH = logging.StreamHandler()
FH.setFormatter(FORMATTER)
CH.setFormatter(FORMATTER)

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(FH)
LOGGER.addHandler(CH)


def parse_cmd_arguments():
    '''Parse Command Line Arguments.'''
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='debug level', type=int,
                        default=0, choices=range(4), required=False)
    return parser.parse_args()


def load_rentals_file(filename):
    '''load data from file.'''
    with open(filename) as file:
        try:
            logging.debug("Loading %s.", filename)
            data = json.load(file)
            logging.debug("Loaded %s.", filename)
        except FileNotFoundError:
            logging.error("Failed to load input json file %s.", filename)
            sys.exit(0)
    logging.debug("Loaded %s entries.", len(data))
    return data


def calculate_additional_fields(data):
    '''Make additional field calculations.'''
    for value in data.values():
        try:
            #if logging level > a given level for grouped logging evaluations.
            #would reduce calls to if statements to one.
            if not value['rental_start']:
                #Missing source DATA, resulting in an error.
                logging.error("Start date is missing for %s.", value['product_code'])
                continue
            if not value['rental_end']:
                #Log warning if end date is missing
                logging.warning("End date is missing for %s.", value['product_code'])
                logging.debug("%s", value)
                #skip calculations if end date is missing.
                continue
            if value['units_rented'] < 1:
                logging.warning("Units rented of %s is less than one.", value['product_code'])
                continue
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            if rental_start > rental_end:
                #incorrect result, therefore an error.
                logging.error("Rental end is before rental start for %s.", value['product_code'])
                #avoid except clause for this condition.
                continue
            value['total_days'] = (rental_end - rental_start).days

            #DATAset is unclear, but logically price_per_day should for one unit.
            #But price_per_day could be for units_rented.
            #Code suggests this given the unit_cost calculation.
            value['total_price'] = value['total_days'] * value['price_per_day']

            #Pointless line that highlights the negative days error.
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except: # pylint: disable=W0702
            logging.error("Hit unknown error in calculate_additional_fields.")
            logging.error("%s", value)
            continue
            # exit(0)

    return DATA


def save_to_json(filename, data):
    '''Save output file function.'''
    try:
        logging.debug("Writing output file to %s.", filename)
        with open(filename, 'w') as file:
            json.dump(data, file)
        logging.debug("Wrote output file to %s.", filename)
    except IOError as io_error:
        logging.error("Failed to write output file to %s.", filename)
        logging.error("%s", dir(io_error))


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    LEVEL = ARGS.debug
    if LEVEL == 0:
        #Disable logging
        LOGGER.disabled = True
    elif LEVEL == 1:
        FH.setLevel(logging.ERROR)
        CH.setLevel(logging.ERROR)
    elif LEVEL == 2:
        FH.setLevel(logging.WARNING)
        CH.setLevel(logging.WARNING)
    elif LEVEL == 3:
        FH.setLevel(logging.WARNING)
        CH.setLevel(logging.DEBUG)

    logging.debug("Input file provided: %s.", ARGS.input)
    logging.debug("Output file provided: %s.", ARGS.output)
    logging.debug("Debug level is %s.", ARGS.debug)

    logging.error("Generate an error.")

    DATA = load_rentals_file(ARGS.input)
    DATA = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, DATA)
