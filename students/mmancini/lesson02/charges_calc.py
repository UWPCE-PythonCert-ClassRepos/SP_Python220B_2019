'''
Returns total price paid for individual rentals
'''
import argparse
import json
import datetime
import math
import traceback
import logging
import sys


def init_logger(level):
    ''' init logger '''
    log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
    log_file = datetime.datetime.now().strftime("%Y-%m-%d") + ".log"

    level_opts = {0: logging.CRITICAL, 1: logging.ERROR,
                  2: logging.WARNING, 3: logging.DEBUG}

    try:
        log_level = level_opts.get(int(level))
    except KeyError:
        print('Debug level not valid.')
        log_level = logging.CRITICAL

    # Create a formatter using the format string.
    formatter = logging.Formatter(log_format)

    # Create a log message handler that sends output to a time-stamped log file.
    file_handler = logging.FileHandler(log_file)
    # Sets the level of log messages to be displayed in the file.
    file_handler.setLevel(logging.WARNING)
    # Sets the formatter for this handler to the formatter created above.
    file_handler.setFormatter(formatter)

    # Create a console log message handler.
    console_handler = logging.StreamHandler()
    # Set the level of messages to be displayed in the console window.
    console_handler.setLevel(log_level)
    # Set the formatter for the handler to the formatter created above.
    console_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(log_level)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def parse_cmd_arguments():
    ''' parse up the command line runtime args '''
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='specify debugger level [0-3]',
                        required=False, default='0')

    return parser.parse_args()


def load_rentals_file(filename):
    ''' read rentals source data file '''

    with open(filename) as file:
        try:
            data = json.load(file)
        except FileNotFoundError:
            sys.exit(0)
    return data

def calculate_additional_fields(data):
    ''' calculate values from input data, on bad data report and continue '''
    for key, value in data.items():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            value['total_days'] = (rental_end - rental_start).days
            value['total_price'] = value['total_days'] * value['price_per_day']
        except Exception as ex:
            # ***MMM fix this
            print('1111111111111111111111111 exception encountered: -' + str(ex) + "-")
            print(traceback.format_exc())
            print(f"Error in input data for key={key}, value={str(value)}")

        try:
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except Exception as ex:
            # ***MMM fix this
            print('222222222222222222222222 exception encountered: -' + str(ex) + "-")
            print(traceback.format_exc())
            print(f"Error in input data for key={key}, value={str(value)}")

    return data

def save_to_json(filename, in_data):
    ''' save rental data file '''
    with open(filename, 'w') as file:
        json.dump(in_data, file)

if __name__ == "__main__":

    ARGS = parse_cmd_arguments()
    init_logger(ARGS.debug)

    # ***MMM test
    logging.debug("test the logger")
    logging.critical("test the logger")
    logging.error("test the logger")
    logging.warning("test the logger")
    # sys.exit()



    DATA = load_rentals_file(ARGS.input)
    DATA = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, DATA)
