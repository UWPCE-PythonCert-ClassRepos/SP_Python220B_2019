'''
Returns total price paid for individual rentals
'''
import argparse
import json
import datetime
import math
import logging
import sys


LOGGER = logging.getLogger('rental_logger')


def parse_cmd_arguments():
    """
    Parses all arguments provided to the script at runtime.
    :return:
    """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='output JSON file', required=True)
    parser.add_argument('-d', '--debug', help='debug level 0-3', required=False)

    return parser.parse_args()


def set_logging_level(level):
    """
    Sets debug level for the program based on the argument passed at runtime.
    :param level:
    :return:
    """

    level_dict = {
        1: logging.ERROR,
        2: logging.WARNING,
        3: logging.DEBUG
    }

    try:
        # set debug level for which the logger will capture
        debug_level = level_dict[int(level)]
        LOGGER.setLevel(debug_level)

        # create file handler which logs even debug messages
        log_file = logging.FileHandler(datetime.datetime.now().strftime("%Y-%m-%d") + '.log')

        # create console handler with a higher log level
        log_stdout = logging.StreamHandler(sys.stdout)

        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s %(filename)s:%(lineno)-3d \
         %(levelname)s %(message)s')
        log_stdout.setFormatter(formatter)
        log_file.setFormatter(formatter)

        if debug_level == logging.DEBUG:
            log_file.setLevel(logging.WARNING)

        LOGGER.addHandler(log_stdout)
        LOGGER.addHandler(log_file)

    except KeyError:
        logging.disable(logging.CRITICAL)



def load_rentals_file(filename):
    """
    Loads the input file to be parsed by the rest of the program. Exits
    if the file is not found.
    :param filename:
    :return:
    """
    LOGGER.debug('function call \"load_rentals_file()\" starts here')
    LOGGER.debug(f'filename to be loaded: {filename}')
    try:
        with open(filename) as file:
            data = json.load(file)
    except FileNotFoundError:
        LOGGER.error(f"Specified file {filename} was not found. Please specify another input file.")
        sys.exit()
    return data


def calculate_additional_fields(data):
    """
    Parses through data and calculates all fields needed to for rental
    data metrics.
    :param input_data: dictionary of rental transactions
    :return:
    """
    LOGGER.debug('function call \"calculate_additional_fields()\" starts here')

    for value in data.values():
        try:
            LOGGER.debug(f"Full product entry: {value}")
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            LOGGER.debug(f"rental_start: {rental_start}")

            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            LOGGER.debug(f"rental_end: {rental_end}")

            value['total_days'] = (rental_end - rental_start).days
            LOGGER.debug(f"total_days: {value['total_days']}")

            value['total_price'] = value['total_days'] * value['price_per_day']
            LOGGER.debug(f"total_price calculated value: {value['total_price']}")

            # Sometimes a negative value is calculated for "total_price". When this occurs
            # the following expressions will throw an error.
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            LOGGER.debug(f"total_price calculated value: {value['sqrt_total_price']}")

            value['unit_cost'] = value['total_price'] / value['units_rented']
            LOGGER.debug(f"unit_cost calculated value: {value['unit_cost']}")

        # ValueError's will be thrown if the error value is negative or the rental_end
        # value doesn't exist. This is captured in the ValueError value present below
        except ValueError:
            if value['rental_end']:
                LOGGER.error(f"Trying to calculate negative square root \
                with total price of {value['total_price']}")
            else:
                LOGGER.warning('Missing rental_end value. Cannot calculate further values.')

        else:
            LOGGER.debug("All fields updated successfully.")

        LOGGER.debug(f'Updated rental item entry: {value}')
    return data


def save_to_json(filename, updated_data):
    """
    Takes all calculated data and writes to a file specified from the
    command line argument when running the script

    :param filename: file to write
    :param updated_data: data to write to filename
    """

    LOGGER.debug('function call \"save_to_json()\" starts here')
    LOGGER.debug(f'filename to be created: {filename}')
    with open(filename, 'w') as file:
        json.dump(updated_data, file)


if __name__ == "__main__":
    args = parse_cmd_arguments()

    if args.debug:
        set_logging_level(args.debug)
    else:
        logging.disable(logging.CRITICAL)

    input_data = load_rentals_file(args.input)
    calculated = calculate_additional_fields(input_data)
    save_to_json(args.output, calculated)
