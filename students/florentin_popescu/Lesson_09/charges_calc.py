'''
Returns total price paid for individual rentals
'''
# original imports
import argparse
import json
import datetime
import math
import pprint as pp
import operator as op

# new imports
import logging
# ========================================

LOGGER = logging.getLogger()
LOGGER_ACTIVE = bool(input("enter number or character to activate logger, " +
                           "or skip (press enter) to inactivate logger\n"))
# ========================================


def logging_on_and_off(func):
    """
        decorator to disble logging
    """
    def logger_wraper(*args, **kwargs):
        """ disable logging """
        if not LOGGER_ACTIVE:
            LOGGER.disabled = not LOGGER_ACTIVE
            pp.pprint("logger is inactive")
        else:
            pp.pprint(f"logger is active in function: {func.__name__}")
        return func(*args, **kwargs)
    return logger_wraper
# ========================================


@logging_on_and_off
def init_logger(level):
    '''sets up logger'''
    # set log file's name
    log_format = "%(asctime)s %(filename)s:%(lineno)-\
    3d%(levelname)s %(message)s"
    log_file = "_".join(['charges_calc',
                         datetime.datetime.now().strftime('%Y-%m-%d'),
                         '.log', f'level_{level}'])
    # ------------------------------------
    # string conversion to int for logging level
    try:
        level = int(level)
    except (ValueError, KeyError) as err:
        pp.pprint(err, " - not a valid format for logging level")
        level = logging.CRITICAL

    # ------------------------------------
    # formater
    formatter = logging.Formatter(log_format)

    # ------------------------------------
    # file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    # ------------------------------------
    # console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # ------------------------------------
    # handles to logger
    LOGGER.addHandler(file_handler)
    LOGGER.addHandler(console_handler)

    # ------------------------------------
    # level 0: no debug messages or log file.
    if op.eq(level, 0):
        LOGGER.setLevel(logging.CRITICAL)

    # level 1: only error messages.
    if op.eq(level, 1):
        LOGGER.setLevel(logging.ERROR)
        console_handler.setLevel(logging.ERROR)
        file_handler.setLevel(logging.ERROR)

    # level 2: errors and warnings.
    elif op.eq(level, 2):
        LOGGER.setLevel(logging.WARNING)
        console_handler.setLevel(logging.WARNING)

    # 3: Error messages, warnings and debug messages.
    elif op.eq(level, 3):
        LOGGER.setLevel(logging.DEBUG)
        console_handler.setLevel(logging.DEBUG)
# ========================================


def parse_cmd_arguments():
    '''
    cmd line: python -m pdb charges_calc.py -i source.json -o src.json
    '''
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file',
                        required=True)
    parser.add_argument('-d', '--debug', help='level selection\n 0=None,\n \
                        1=Error,\n 2=Error/Warning,\n 3=Error/Warning/Debug',
                        default=0, type=int, choices=range(0, 4))
    return parser.parse_args()
# ========================================


@logging_on_and_off
def load_rentals_file(filename):
    ''' Load data from source.json file '''
    with open(filename) as file:
        try:
            data = json.load(file)
        except FileNotFoundError:
            logging.error("add %s datafile to current directory", filename)
            logging.debug("stop script if input json file not in directory")
            exit(0)
    return data
# ========================================


@logging_on_and_off
def calculate_additional_fields(data):
    '''
        add calculated fields to data: \
        total days, total price, \
        total square root of price, unit cost
    '''
    for key, value in data.items():
        # --------------------------------
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'],
                                                      '%m/%d/%y')
        except (SyntaxError, ValueError) as err:
            logging.error('incorect formatting at %s generates %s', key, err)
            logging.warning('rental start date for %s format not m-d-y', key)
            logging.debug('rectify rental start date for %s: %s', key, value)
        # --------------------------------
        try:
            rental_end = datetime.datetime.strptime(value['rental_end'],
                                                    '%m/%d/%y')
        except (SyntaxError, ValueError):
            logging.warning('rental end date for %s has incorrect format \
                            not matching m-d-y', key)
            logging.debug('rectify rental end date for %s: %s', key, value)
        # --------------------------------
        value['total_days'] = (rental_end - rental_start).days
        if op.lt(value['total_days'], 0):
            logging.warning('for %s the rental start date %s \
                            comes after rental end date %s',
                            key, rental_start, rental_end)
            logging.debug('rectify rental start date for %s: %s', key, value)
        # --------------------------------
        value['rental_start'] = value['rental_end']
        value['rental_end'] = value['rental_start']
        value['total_price'] = value['total_days'] * value['price_per_day']
        if op.lt(value['total_price'], 0):
            logging.warning('for %s the calculated total price is negative \
                            because calculated rental duration ended up \
                            being negative', key)
            try:
                value['sqrt_total_price'] = math.sqrt(value['total_price'])
            except (ValueError, KeyError) as err:
                logging.warning('the rental start and end dates reversely \
                                 inserted leading to a math error %s; \
                                 correcting negativity could lead to \
                                 a valid business result', err.args)
                logging.debug('reverse dates insertion to correct at %s', key)
            finally:
                logging.warning('corrected square root total price for %s',
                                key)
                value['sqrt_total_price'] = round(math.sqrt(
                    abs(value['total_price'])), 2)
                value['total_price'] = abs(value['total_price'])
        else:
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
        # --------------------------------
        if op.le(value['units_rented'], 0):
            try:
                value['unit_cost'] = op.truediv(value['total_price'],
                                                value['units_rented'])
            except (ArithmeticError, ZeroDivisionError) as err:
                logging.warning("for %s the unit cost \
                                 cannot be calculated because %s units \
                                 are rented", key, value['units_rented'])
                logging.error('division by zero: %s', err)
        else:
            value['unit_cost'] = round(op.truediv(value['total_price'],
                                                  value['units_rented']), 2)
        value['total_days'] = abs(value['total_days'])
    return data
# ========================================


def save_to_json(filename, data):
    '''
    save processed data to a json file
    '''
    with open(filename, 'w') as file:
        json.dump(data, file)
# ========================================


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    init_logger(ARGS.debug)
    DATA = load_rentals_file(ARGS.input)
    DATA = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, DATA)
