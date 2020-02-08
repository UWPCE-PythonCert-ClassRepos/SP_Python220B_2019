""" lesson09 assignment part 1 code
Changed lesson02 assignment code to use a decorator to set the logging level. Use the command line
switch "-d" to with "0" (disable logging), "1" (logging.ERROR), "2" (logging.WARNING), or "3"
(logging.DEBUG). Use as follows (examples):

$ python charges_calc.py -i source.json -o output.json -d 0
$ python charges_calc.py -i source.json -o output.json -d 1
$ python charges_calc.py -i source.json -o output.json -d 2
$ python charges_calc.py -i source.json -o output.json -d 3

Returns total price paid for individual rentals. (BSM: Actually does more - adds some fields to the
rentals data.)

BSM - Found a problem where some records in the input data have a rental start date that is after
the end date, so a value calculated for the total number of rental days is sometimes negative.
The calculated total rental price uses the total number of rental days in its calculation: when the
total number of rental days is negative the total rental price is also calculated to be negative.
The square root of the total rental price is then calculated. When the total rental price is
negative then sqrt gives an exception, which is only handled by exiting the script.

I found another problem where a couple values in the data are "" which causes exceptions as well.

I added logging, which among other things, logs the data values and calculated values. I also added
code to handle the exceptions described above so the script continues execution without exiting.
Logging level can be set with a "-d" switch and the following logging level values:
    0: No debug messages or log file.
    1: Only error messages.
    2: Error messages and warnings.
    3: Error messages, warnings and debug messages.
"""
import argparse
import json
import datetime
import math

import logging


class Set_Logger_Level(object):
    """ Decorator to disable logging or to set the logging level to logging.ERROR, logging.WARNING,
    logging.DEBUG.
    Note: It was difficult to figure out how to send argument values to a decorator at runtime. I
    found this and adapted it:
    https://stackoverflow.com/questions/11855418/passing-parameters-to-decorator-at-runtime
    """
    def __init__(self, func=None, log_level=0):
        self.func = func
        self.log_level = log_level

    def __call__(self, *args, **kwargs):
        if self.func == None:
            self.func = args[0]
        else:
            if self.log_level == 0 or self.log_level == '0':
                logging.disable()
            else:
                levels = {'1': logging.ERROR, '2': logging.WARNING, '3': logging.DEBUG,
                        }
                logger = logging.getLogger()
                logger.setLevel(levels[self.log_level])

        return self.func(*args, **kwargs)


@Set_Logger_Level
def setup_logger():
    """ Set up logging to a file.
    Note: Logging level is now set with a decorator class, using a command line variable.
    """
    log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
    formatter = logging.Formatter(log_format)

    log_file = datetime.datetime.now().strftime("%Y-%m-%d")+'.log'
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.addHandler(file_handler)


def parse_cmd_arguments():
    """ Parse arguments from the command line.
    """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='set logging level', required=False)

    return parser.parse_args()


def load_rentals_file(filename):
    """ Load the file whose filename was previously indicated on the command line as a json file.
    """
    logging.debug("Loading rentals json file. Function name: load_rentals_file")
    with open(filename) as file:
        try:
            data = json.load(file)
        # Pylint is saying not to use a bare except. Since I am not touching this code I am
        # supressing the error.
        # pylint: disable-msg=W0702
        except:
            exit(0)
    return data


def calculate_additional_fields(data):
    """ Calculate various new fields from the input data and add them to the input data.

    Keyword arguments:
    data - input json data
    """
    logging.debug("Starting computing derived data. Function name: calculate_additional_fields")
    for key, value in data.items():
        logging.debug("*****Computing derived data for rental code %s.*****", key)

        rental_start = process_rental_start(key, value)
        rental_end = process_rental_end(key, value)

        # Sometimes rental_start or rental_end will be bad data and, if so, they are set to None.
        # If one or both is None type '>' will raise a TypeError exception.
        try:
            if rental_start > rental_end:
                logging.warning("%s: rental_end is before rental_start.", key)
        except TypeError as err:
            logging.error("%s: Rental date has bad data: %s", key, err)

        process_total_days(key, value, rental_start, rental_end)
        validate_price_per_day(key, value)
        process_total_price(key, value)
        process_sqrt_total_price(key, value)
        validate_units_rented(key, value)
        process_unit_cost(key, value)

    return data


def process_rental_start(key, value):
    """ Validate rental_start, convert it to datetime format, and return it.
    """
    rental_start = None
    if (not value['rental_start']) or (value['rental_start'] == ""):
        logging.warning("%s: no rental_start value.", key)
    try:
        rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
    except ValueError as err:
        logging.error("%s: rental_start: %s", key, err)
    logging.debug("%s: rental_start = %s", key, rental_start)

    return rental_start


def process_rental_end(key, value):
    """ Validate rental_end, convert it to datetime format, and return it.
    """
    rental_end = None
    # found a case where value['rental_end'] == ""
    if (not value['rental_end']) or (value['rental_end'] == ""):
        logging.warning("%s: no rental_end value.", key)
    try:
        rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
    except ValueError as err:
        logging.error("%s: rental_end: %s", key, err)
    logging.debug("%s: rental_end = %s", key, value['rental_end'])

    return rental_end


def process_total_days(key, value, rental_start, rental_end):
    """ Calculate total_days and add it to the data.
    """
    total_days = None
    # if rental_end is a prior date to rental_start then value['total_days'] is negative
    try:
        total_days = (rental_end - rental_start).days
    except TypeError as err:
        logging.error("%s: computing total_days: %s", key, err)
    if total_days and (total_days >= 0):
        value['total_days'] = total_days
        logging.debug("%s: total_days = %s", key, value['total_days'])
    if total_days and (total_days < 0):
        logging.warning("%s: computing total_days: value is negative", key)


def validate_price_per_day(key, value):
    """ Validate price_per_day (currently only used for logging).
    """
    if (not value['price_per_day']) or (value['price_per_day'] == ""):
        logging.warning("%s: no price_per_day value.", key)


def process_total_price(key, value):
    """ Calculate total_price and add it to the data.
    """
    # if value['total_days'] is negative then value['total_price'] is negative
    try:
        value['total_price'] = value['total_days'] * value['price_per_day']
    except TypeError as err:
        logging.error("%s: computing total_price: %s", key, err)
    except KeyError as err:
        logging.error("%s: computing total_price: %s", key, err)
    else:
        if value['total_price'] < 0:
            logging.warning("%s: computing total_price: value is negative", key)
        logging.debug("%s: total_price = %s", key, value['total_price'])


def process_sqrt_total_price(key, value):
    """ Calculate sqrt_total_price and add it to the data.
    """
    # if value['total_price'] is negative then the sqrt gives an exception
    try:
        value['sqrt_total_price'] = math.sqrt(value['total_price'])
    except ValueError:
        logging.error("%s: computing sqrt_total_price: cannot sqrt negative value", key)
    except KeyError as err:
        logging.error("%s: computing sqrt_total_price: %s", key, err)
    else:
        logging.debug("%s: sqrt_total_price = %s", key, value['sqrt_total_price'])


def validate_units_rented(key, value):
    """ Validate units_rented (currently only used for logging).
    """
    if (not value['units_rented']) or (value['units_rented'] == ""):
        logging.warning("%s: no units_rented value.", key)


def process_unit_cost(key, value):
    """ Calculate unit_cost and add it to the data.
    """
    try:
        value['unit_cost'] = value['total_price'] / value['units_rented']
    except ZeroDivisionError:
        logging.error("%s: computing unit_cost: zero division error", key)
    except TypeError as err:
        logging.error("%s: computing unit_cost: %s", key, err)
    except KeyError as err:
        logging.error("%s: computing unit_cost: %s", key, err)
    else:
        logging.debug("%s: unit_cost = %s", key, value['unit_cost'])


def save_to_json(filename, data):
    """ Save the data with new fields to a file whose name was previously specified on the command
    line.

    Keyword arguments:
    filename - name of the file the data will be saved to.
    data - json data to be saved to the file.
    """
    logging.debug("Saving augmented data to json file. Function name: save_to_json")
    with open(filename, 'w') as file:
        json.dump(data, file)


def main():
    """ Parse the command line arguments. Setup a logger. Load a json file with rentals data.
    Calculate new fields from the rentals data and add them to the data. Save the data to a json
    file.
    """
    args = parse_cmd_arguments()
    setup_logger.log_level = args.debug
    setup_logger()   # setup the logging level from a command line parameter
    rental_data = load_rentals_file(args.input)
    rental_data = calculate_additional_fields(rental_data)
    save_to_json(args.output, rental_data)


if __name__ == "__main__":
    main()
    logging.debug("Normal exit")
