'''
Returns total price paid for individual rentals
'''
import argparse
import json
import datetime
import math
import logging


def init_logger(level):
    """sets up logger"""
    # Convert string to int for log level
    level = int(level)

    # Format log
    log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s \
                    %(message)s"
    log_file = 'charges_calc_' + datetime.datetime.now().strftime('%Y-%m-%d')+'.log'

    # Attach formater
    formatter = logging.Formatter(log_format)

    # Add file handler and only log to file
    # when level is WARNING or above
    file_handler = logging.FileHandler(log_file)
#    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(formatter)

    # Add console handler
    console_handler = logging.StreamHandler()
#    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    # Add handles to logger
    logger = logging.getLogger()
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Setup log level according to user selection
    # 0: No debug messages or log file.
    if level == 0:
        logger.setLevel(logging.CRITICAL)

    # 1: Only error messages.
    if level == 1:
        logger.setLevel(logging.ERROR)
        console_handler.setLevel(logging.ERROR)
        file_handler.setLevel(logging.ERROR)

    # 2: Error messages and warnings.
    elif level == 2:
        logger.setLevel(logging.WARNING)
        console_handler.setLevel(logging.WARNING)

    # 3: Error messages, warnings and debug messages.
    elif level == 3:
        logger.setLevel(logging.DEBUG)
        console_handler.setLevel(logging.DEBUG)


def parse_cmd_arguments():
    '''
    Parse command line arguments
    '''
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file',
                        required=True)
    parser.add_argument('-d', '--debug', help='debug level', required=True)

    return parser.parse_args()


def load_rentals_file(filename):
    '''
    Load input file
    '''
    with open(filename) as input_file:
        try:
            data = json.load(input_file)
        except ValueError as ex:
            logging.error(ex)
    return data


def calculate_additional_fields(data):
    '''
    Calculate additional fields based on source.json file
    '''
    data_new = data.copy()
    for key in data:
        try:
            rental_start = datetime.datetime.strptime(data[key]['rental_start'],
                                                      '%m/%d/%y')
            rental_end = datetime.datetime.strptime(data[key]['rental_end'],
                                                    '%m/%d/%y')
            total_days = (rental_end - rental_start).days
            if total_days <= 0:
                raise ValueError('End before start')
#                logging.error('not a valid rental length for rental %s', key)
#                del data_new[key]
            data[key]['total_days'] = total_days
            data[key]['total_price'] = data[key]['total_days'] * data[key]['price_per_day']
            data[key]['sqrt_total_price'] = math.sqrt(data[key]['total_price'])
            data[key]['unit_cost'] = data[key]['total_price'] / data[key]['units_rented']

        except ValueError as ex:
            if "time data '' does not match format" in str(ex):
                logging.error('no rental_end for rental %s', key)
                del data_new[key]
            elif "math domain error" in str(ex):
                logging.error('total_price is negative for rental %s: %s', key,
                              data[key]['total_price'])
                del data_new[key]
            elif 'does not match format' in str(ex):
                logging.warning(ex)
                del data_new[key]
            elif 'End before start' in str(ex):
                logging.error('not a valid rental length for rental %s', key)
                del data_new[key]

    return data_new


def save_to_json(filename, data):
    '''
    Save results to JSON file
    '''
    with open(filename, 'w') as out_file:
        json.dump(data, out_file)


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    init_logger(ARGS.debug)
#    logging.debug(ARGS)    is this line necessary?
    DATA = load_rentals_file(ARGS.input)
    RESULT = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, RESULT)
