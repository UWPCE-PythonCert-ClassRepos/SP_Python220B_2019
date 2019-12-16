"""
Returns total price paid for individual rentals.

Modified to log potential errors. There are 3 levels of log statements:
- Debug : General comments about program.
- Warning : Missing source data that alters program flow.
- Error : Erroneous source data that causes program crashes.

Program usage:
> python charges_calc.py -i input -o output [-d/-debug level]

The -d flag can be used to give a debug level from 0 to 3:
- 0 : no messages
- 1 : Only error messages
- 2 : Errors and warnings
- 3 : Errors, warnings, and debug statements

Errors are issued when invalid data values are encountered.
Warnings are issued when required data is missing.
Debug statements are issued if the computation or data retreival is
successful.

If any condition that causes an error or warning is encountered,
the computation is abandoned and the program skips to the
next item.
"""

import argparse
import json
import datetime
import math
import logging
import sys

# Set up logging
LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
FORMATTER = logging.Formatter(LOG_FORMAT)

LOG_FILE = datetime.datetime.now().strftime("%Y-%m-%d") + '.log'
FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setFormatter(FORMATTER)

STREAM_HANDLER = logging.StreamHandler()
STREAM_HANDLER.setFormatter(FORMATTER)

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(STREAM_HANDLER)

VALID_OPTS = (0, 1, 2, 3)
INVALID_KEY = "{}: No {} data present"
INVALID_FORMAT = "{}: {} is in incorrect format"


def parse_cmd_arguments():
    """
    Parse command line arguments.

    :returns: parsed args
    """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)

    # Add optional argument for logging level
    parser.add_argument('-d', '-debug', help='logging level, 0 - 3', required=False,
                        default=0, type=int)

    return parser.parse_args()


def load_rentals_file(filename):
    """
    Load input JSON file.

    :param filename: str, name of file to load
    :return: dict, loaded data
    """
    with open(filename) as file:
        try:
            # Attempt to load the file
            msg = f"Loading {filename}"
            logging.debug(msg)
            data = json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            # Log an error message if unable to open file
            msg = f"Unable to load input file ({filename})"
            logging.error(msg)
            sys.exit(0)
    return data


def _compute_times(key, value):
    """
    Compute start and end times.

    :param key: str, key of data
    :param value: str, value of data
    :returns: bool, True if successful
    :returns: float, total rented days
    """
    # Attempt to get start rental date
    try:
        rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
    except KeyError:
        msg = INVALID_KEY.format(key, 'rental_start')
        logging.warning(msg)
        return False
    except ValueError:
        msg = INVALID_FORMAT.format(key, value['rental_start'])
        logging.warning(msg)
        return False
    else:
        msg = f"  - Start date = {rental_start}"
        logging.debug(msg)

    # Attempt to get end rental date
    try:
        rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
    except KeyError:
        msg = INVALID_KEY.format(key, "rental_end")
        logging.warning(msg)
        return False
    except ValueError:
        msg = INVALID_FORMAT.format(key, value['rental_end'])
        logging.warning(msg)
        return False
    else:
        msg = f"  - End date = {rental_end}"
        logging.debug(msg)

    # Compute time of rental
    total_days = (rental_end - rental_start).days
    if total_days < 0:
        msg = f"{key}: End date is before start date"
        logging.error(msg)
        return False

    value['total_days'] = total_days
    msg = f"  - total_days = {total_days}"
    logging.debug(msg)

    return True


def calculate_additional_fields(data):
    """
    Calculate additional fields and modify the input dictionary.

    :param data: dict, loaded data
    :return: dict, input dict with new fields added
    """
    for key, value in data.items():
        # Store which key is being accessed
        msg = f"Current key: {key}"
        logging.debug(msg)

        success = _compute_times(key, value)
        if not success:
            continue

        # Compute total price of rental
        try:
            ppd = value['price_per_day']
        except KeyError:
            msg = f"{key}: No price_per_day"
            logging.warning(msg)
            continue
        else:
            msg = f"  - price_per_day = {ppd}"
            logging.debug(msg)

        try:
            value['total_price'] = value['total_days'] * ppd
        except ValueError:
            msg = f"{key}: Invalid price_per_day"
            logging.error(msg)
            continue
        else:
            msg = f"  - total_price ={value['total_price']}"
            logging.debug(msg)

        # Compute square-root of total price
        try:
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
        except ValueError:
            msg = f"{key}: Invalid total_price, unable to take square root"
            logging.error(msg)
        else:
            msg = f"  - sqrt_total_price = {value['sqrt_total_price']}"
            logging.debug(msg)

        # Compute unit cost of rental
        try:
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except KeyError:
            msg = f"{key}: No units_rented"
            logging.warning(msg)
        except ValueError:
            msg = f"{key}: Invalid units_rented"
            logging.error(msg)
        else:
            msg = f"  - units_rented = {value['units_rented']}"
            logging.debug(msg)

    return data


def save_to_json(filename, data):
    """
    Save data to a JSON file.

    :param filename: str, name of file to save to
    :param data: dict, data to save
    """
    msg = f"Dumping JSON data to {filename}"
    logging.debug(msg)
    with open(filename, 'w') as file:
        json.dump(data, file)


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()

    # Set logging level based on -d input
    if ARGS.d not in VALID_OPTS:
        raise ValueError("Invalid debug flag")

    D = ARGS.d
    if D == 0:
        FILE_HANDLER.setLevel(100)
        STREAM_HANDLER.setLevel(100)
    else:
        FILE_HANDLER.setLevel(logging.ERROR)
        STREAM_HANDLER.setLevel(logging.ERROR)
        if D >= 2:
            FILE_HANDLER.setLevel(logging.WARNING)
            STREAM_HANDLER.setLevel(logging.WARNING)
        if D == 3:
            STREAM_HANDLER.setLevel(logging.DEBUG)

    # Log commands
    MSG = f"Input file: {ARGS.input}"
    logging.debug(MSG)
    MSG = f"Output file: {ARGS.output}"
    logging.debug(MSG)
    MSG = f"Debug level: {D}"
    logging.debug(MSG)

    DATA = load_rentals_file(ARGS.input)
    DATA = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, DATA)
