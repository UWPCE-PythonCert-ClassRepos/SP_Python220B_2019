'''
Returns total price paid for individual rentals
'''
import argparse
import json
import datetime
import math
import logging
import sys
# pylint:disable=C0103

def set_logging_settings(level):
    '''set it'''
    if level == '0':
        logging.disable()
        return None

    # define the format and tell the logging module about your format
    log_format = '%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s'
    formatter = logging.Formatter(log_format)

    # name the file the logging gets saved to
    log_file = datetime.datetime.now().strftime('%Y-%m-%d')+'.log'

    # tell the logging module WHERE to save and  HOW to save in its file
    FH = logging.FileHandler(log_file)
    FH.setFormatter(formatter)

    # tell the logging module WHERE to save and  HOW to save in console
    CH = logging.StreamHandler()
    CH.setFormatter(formatter)

    if level == '1':
        FH.setLevel(logging.ERROR)
        CH.setLevel(logging.ERROR)

        LOGGER = logging.getLogger()
        LOGGER.setLevel(logging.DEBUG)
        LOGGER.addHandler(FH)
        LOGGER.addHandler(CH)

    if level == '2':
        FH.setLevel(logging.WARNING)
        CH.setLevel(logging.WARNING)

        LOGGER = logging.getLogger()
        LOGGER.setLevel(logging.DEBUG)
        LOGGER.addHandler(FH)
        LOGGER.addHandler(CH)

    if level == '3':
        FH.setLevel(logging.WARNING)
        CH.setLevel(logging.DEBUG)

        LOGGER = logging.getLogger()
        LOGGER.setLevel(logging.DEBUG)
        LOGGER.addHandler(FH)
        LOGGER.addHandler(CH)

    logging.debug('logging level set at %s', level)
    return None


def parse_cmd_arguments():
    '''parse it'''
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
# you name the output file in the user interface
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--dbg_command', help='debug level', required=False
                        , default=0)
    return parser.parse_args()


def load_rentals_file(filename):
    '''load it'''
    with open(filename) as file:
        try:
            data = json.load(file)
            logging.debug("Loaded %s.", filename)
        except FileNotFoundError:
            logging.error("Double check name of %s.json", filename)
            sys.exit(0)
    logging.debug("You have %s rows of data", len(data))
    return data


def calculate_additional_fields(data):
    '''calculate it'''
    bug_count = 0
    for key, value in data.items():
        try:
            if not value['rental_end']:
                logging.warning("rental_end is missing for %s", key)
                bug_count = bug_count+1
            # make dates into dates data type for calc
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            value['total_days'] = (rental_end - rental_start).days
        except KeyError:
            logging.error("KeyError in total_days for %s", key)
        except ValueError:
            logging.error("ValueError in total_days for %s", key)
            value['total_days'] = 0
            bug_count = bug_count+1
        if not value['rental_start']:
            logging.warning("rental_start is missing for %s", key)
            bug_count = bug_count+1
            continue
        if value['units_rented'] < 1:
            logging.warning("units_rented is less than 1 for %s", key)
            bug_count = bug_count+1
            continue
        if rental_start > rental_end:
            logging.error('rental_end is before rental_start for %s', key)
            bug_count = bug_count+1
            continue
        value['total_price'] = value['total_days'] * value['price_per_day']
        value['sqrt_total_price'] = math.sqrt(value['total_price'])
        value['unit_cost'] = value['total_price'] / value['units_rented']

    logging.debug('there were %s bugs out of %s lines' % (bug_count, len(data)))
    return data


def save_to_json(filename, data):
    '''for saving to the json output file, wont work unless
    calculate_additional_fields works'''
    with open(filename, 'w') as file:
        json.dump(data, file)
    logging.debug("wrote output file to %s", filename)


if __name__ == "__main__":
    args = parse_cmd_arguments()
    set_logging_settings(args.dbg_command)

    # logging.debug("Input file provided: %s.", args.input)
    # logging.debug("Output file provided: %s.", args.output)
    # logging.debug("Debug level is %s.", args.dbg_command)
    DATA = load_rentals_file(args.input)
    DATA = calculate_additional_fields(DATA)
    save_to_json(args.output, DATA)
