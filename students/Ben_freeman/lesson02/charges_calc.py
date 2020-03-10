'''
Returns total price paid for individual rentals 
'''
import argparse
import json
import datetime
import math
import sys
import logging

logging_dict = {"3": logging.DEBUG,
                "2": logging.WARNING,
                "1": logging.ERROR,
                "0": logging.CRITICAL}


def logging_file_setup():
    log_format = '%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s'
    formatter = logging.Formatter(log_format)

    log_file = datetime.datetime.now().strftime("%Y-%m-%d") + '.log'

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.WARNING)

    logger = logging.getLogger()
    logger.addHandler(file_handler)

    return logger


def logging_console_setup():
    log_format = '%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s'
    formatter = logging.Formatter(log_format)
    console_handler = logging.StreamHandler()

    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    loggers = logging.getLogger()
    loggers.addHandler(console_handler)

    return loggers

def parse_cmd_arguments():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='debug level', required=True)
    return parser.parse_args()


def load_rentals_file(filename):
    with open(filename) as file:
        log_console.debug("Loading data file")
        try:
            data = json.load(file)
        except FileNotFoundError:
            log.error("error loading data")
    return data


def calculate_additional_fields(data):
    log_console.debug("Beginning data calculations")
    for value in data.values():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            value['total_days'] = (rental_end - rental_start).days
            if value['total_days'] < 1:
                log.warning("Start date after end date.")
                continue
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            try:
                value['unit_cost'] = value['total_price'] / value['units_rented']
            except ZeroDivisionError:
                log.warning("Zero united rented")

        except ValueError:
            log.error("Missing data")

    return data


def save_to_json(filename, data):
    with open(filename, 'w') as file:
        log_console.debug("saving data")
        json.dump(data, file)


if __name__ == "__main__":
    args = parse_cmd_arguments()
    log = logging_file_setup()
    log.setLevel(logging_dict[args.debug])
    log_console = logging_console_setup()
    log_console.setLevel(logging_dict[args.debug])
    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)
