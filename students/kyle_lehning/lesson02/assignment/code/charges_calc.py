"""
Returns total price paid for individual rentals 
"""
import argparse
import json
import datetime
import math
import logging


def init_logger(level):
    """Initialize settings for log file"""
    # Name of the log file with time stamp
    log_file = 'charges_calc' + datetime.datetime.now().strftime("%Y-%m-%d") + '.log'
    # log format
    log_format = "%(asctime)s%(filename)s:%(lineno)-3d%(levelname)s%(message)s"
    # Create a formatter using format string
    formatter = logging.Formatter(log_format)

    # Create a log message handler that sends output to the log_file
    file_handler = logging.FileHandler(log_file)
    # Set the formatter for this log message handler to the formatter created above
    file_handler.setFormatter(formatter)

    # Get the root logger
    logger = logging.getLogger()
    # Add file_handler to the root logger's handlers
    logger.addHandler(file_handler)
    if level == 0:
        # No debug messages or log file
        logger.setLevel(logging.CRITICAL)
    elif level == 1:
        # Only error messages
        pass
    elif level == 2:
        # Error messages and warnings
        file_handler.setLevel(logging.WARNING)
    elif level == 3:
        # Error messages, warnings, and debug messages
        file_handler.setLevel(logging.WARNING)


def parse_cmd_arguments():
    """Gather arguments from command line"""
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='output JSON file', required=True)

    return parser.parse_args()


def load_rentals_file(filename):
    """Open passed filename and use json.load to read to data object and return it"""
    with open(filename) as file:
        try:
            data = json.load(file)
        except:
            exit(0)
    return data


def calculate_additional_fields(update_data):
    """
    Receive update_data and go through each value within update_data and update fields
    within the dictionary then return update_data with updated value fields
    """
    for value in update_data.values():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            value['total_days'] = (rental_end - rental_start).days
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except:
            exit(0)

    return update_data


def save_to_json(filename, input_data):
    """Save info from input_data to filename in json format"""
    with open(filename, 'w') as file:
        json.dump(input_data, file)


if __name__ == "__main__":
    args = parse_cmd_arguments()
    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)
