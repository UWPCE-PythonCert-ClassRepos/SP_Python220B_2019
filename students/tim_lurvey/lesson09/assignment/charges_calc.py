"""
Returns total price paid for individual rentals
"""
import argparse
import json
import datetime
import math
import logging

#pylint: disable=logging-fstring-interpolation, logging-format-interpolation, broad-except

ARGS = None
logger = logging.getLogger()

def logging_decorator(func):
    """
    Determine the logging level from the command line and set terminal and file logging.
    Default is no log file or debug terminal printing
    """
    def inner(*args, **kwargs):

        log_level = {'0': {'term': logging.NOTSET,
                           'file': logging.NOTSET},
                     '1': {'term': logging.ERROR,
                           'file': logging.ERROR},
                     '2': {'term': logging.WARNING,
                           'file': logging.WARNING},
                     '3': {'term': logging.DEBUG,
                           'file': logging.WARNING},
                     }

        if ARGS.debug not in log_level:
            raise SystemExit(
                f"The logging value '{ARGS.debug}' is invalid.  "
                f"Please use -h for valid options.\nExiting....")

        format_str = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"

        log_terminal = logging.StreamHandler()
        log_terminal.setFormatter(fmt=logging.Formatter(format_str))
        log_terminal.setLevel(level=log_level.get(ARGS.debug).get('term'))

        log_file = logging.FileHandler(
            filename=datetime.datetime.now().strftime("%Y-%m-%d") + ".log")
        log_file.setFormatter(fmt=logging.Formatter(format_str))
        log_file.setLevel(level=log_level.get(ARGS.debug).get('file'))

        logger.setLevel(logging.DEBUG)
        logger.addHandler(log_terminal)
        logger.addHandler(log_file)

        return func(*args, **kwargs)
    return inner


def parse_cmd_arguments():
    """
    Parse arguments from command line and return values
    """
    debug_help_cmd = "Debugging level" \
                     "\n0: No debug messages or log file." \
                     "\n1: Only error messages." \
                     "\n2: Error messages and warnings." \
                     "\n3: Error messages, warnings and debug messages."

    parser = argparse.ArgumentParser(description='Process some integers.',
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-i', '--input',
                        help='input JSON file',
                        required=True)

    parser.add_argument('-o', '--output',
                        help='ouput JSON file',
                        required=True)

    parser.add_argument('-d', '--debug',
                        help=debug_help_cmd,
                        required=False,
                        default='0')

    return parser.parse_args()

@logging_decorator
def load_rentals_file(filename):
    """
    Open the specified data file

    Log all actions in debug mode.

    :type filename: str
    :return dict
    """
    try:
        with open(filename) as file:
            try:
                read_data = json.load(file)
                logging.debug("File opened: {f}".format(f=filename))
                return read_data
            except Exception as ex:
                logging.error("Cannot open file: {f}".format(f=filename))
                raise ex
    except FileNotFoundError as ex:
        logging.error("File not found: {f}".format(f=filename))
        raise ex

@logging_decorator
def check_dates(key, val):
    """
    Try to read and convert start and end dates, returning a boolean of success.
    Log any error that occurs in reading and converting the read data into a datetime object
    :param key: str
    :param val: dict
    :return bool
    """
    for start_end in ['rental_start', 'rental_end']:
        try:
            datetime.datetime.strptime(val[start_end], '%m/%d/%y')
        except ValueError as err:
            logging.error(f"[{key}] Value {start_end} cannot be converted to a date.  Skipping...")
            logging.error(err)
            return False
    return True


def calc_total_days(val):
    """
    Return the total number of days
    :type val: dict
    :return int
    """
    try:
        start = datetime.datetime.strptime(val['rental_start'], '%m/%d/%y')
        end = datetime.datetime.strptime(val['rental_end'], '%m/%d/%y')
        total_days = (end - start).days
    except ValueError as err:
        logging.error(err)
        total_days = 0
    return total_days


def calc_total_price(val):
    """
    Calculate the price total
    :type val: dict
    :return float
    """
    return float(val['total_days'] * val.get('price_per_day', 0.))


def calc_total_sqrt(val):
    """
    Calculate the square root of the price
    :type val: dict
    :return float
    """
    try:
        return math.sqrt(val.get('total_price'))
    except ValueError as err:
        logging.error(err)
        return 0.


def calc_unit_cost(val):
    """
    Returns the unit cost (total / units)
    :type val: dict
    :return float
    """
    if val.get('units_rented'):     # pylint: disable=no-else-return
        return val.get('total_price') / val.get('units_rented')
    else:
        return 0.


@logging_decorator
def calculate_additional_fields(data):
    """
    Calculate and set new values needed for each entry in the data set.  Each calculation is
    isolate into their own function for clarity.

    Verbose debugging information can be obtained and written.  Use -h for details.
    - For each read of a variable, print the read value to the terminal in debug mode.
    - Any value calculation errors that can be overwritten as a 0, will be 0 upon errors.
      A WARNING will be written to a log file if run in debug mode.
    - Values that are critical and cannot be missing will report errors and the entry
      will be skipped.
      An ERROR will be written to a log file if run in debug mode.

    :type data: dict
    :return dict
    """

    calculations = {'total_days': calc_total_days,
                    'total_price': calc_total_price,
                    'total_sqrt': calc_total_sqrt,
                    'unit_cost': calc_unit_cost,
                    }

    for key, value in data.items():
        # test for key reading
        for sub_key in ['product_code',
                        'rental_start',
                        'rental_end',
                        'price_per_day',
                        'units_rented']:
            try:
                read = value[sub_key]
                logging.debug(f"[{key}] Value '{sub_key}' read as {read}")
            except Exception as err:
                logging.error(f"[{key}] No value '{sub_key}'")
                logging.error(err)

        # determine if dates are readable and convertible, skip entry if not
        if not check_dates(key=key, val=value):
            continue

        # setup new variables and add them to data
        for new_val in sorted(calculations.keys()):
            calc = calculations.get(new_val)(val=value)
            if not calc:
                logging.warning(f"[{key}] Unabled to calculate {new_val}. Using {calc}")
            value.update({new_val: calc})
            logging.debug(f"[{key}] Value {new_val} set as {calc}")

    return data


def save_to_json(filename, data):
    """
    Save the modified data dictionary to a file
    :param filename: str
    :param data: dict
    :return: None
    """
    with open(filename, 'w') as file:
        file.write(json.dumps(data, indent=2))


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    raw_data = load_rentals_file(ARGS.input)
    mod_data = calculate_additional_fields(raw_data)
    save_to_json(ARGS.output, mod_data)
