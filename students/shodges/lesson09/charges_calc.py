'''
Returns total price paid for individual rentals
'''
import argparse
import json
import datetime
import math
import logging
import sys

def init_logging(func):
    '''
    Decorator for logging functions.
    '''
    def setup_logging(log_level, *args):
        '''
        Setup standard logging.  Requires log_level variable to be set at this mapping:

        0 = no logging
        1 = ERROR and above (CRITICAL is not implemented)
        2 = WARNING and above
        3 = DEBUG and above
        '''
        log_level_mapping = {'0': 99, '1': logging.ERROR, '2': logging.WARNING, '3': logging.DEBUG}

        # We want to setup the logger regardless of log_level -- if it's disabled, set it to level >50
        logger = logging.getLogger()
        logger.setLevel(log_level_mapping[log_level])

        if log_level != '0': # Let's not bother to setup the rest if we're disabling logging
            log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
            log_file = datetime.datetime.now().strftime("%Y-%m-%d") + '.log'


            formatter = logging.Formatter(log_format)
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.WARNING)
            file_handler.setFormatter(formatter)

            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            console_handler.setFormatter(formatter)

            logger.addHandler(file_handler)
            logger.addHandler(console_handler)


def parse_cmd_arguments():
    '''
    Define script arguments.
    '''
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='debug level: 0 (default) = off, 1 = ERROR, ' +
                        '2 = ERROR + WARNING, 3 = ERROR + WARNING + DEBUG', default='0',
                        choices=('0', '1', '2', '3'))

    return parser.parse_args()


def load_rentals_file(filename):
    '''
    Load data (specified in filename variable) as json.
    '''
    try:
        with open(filename) as file:
            data = json.load(file)
            logging.debug('Successfully opened data file %s', filename)
    except FileNotFoundError:
        logging.error('File %s does not exist -- exiting.', filename)
        sys.exit()
    return data

def calculate_additional_fields(data):
    '''
    Iterate through data and add additional calculated fields.
    '''
    for value in data.values():
        logging.debug('Calculate additional fields with data: %s', value)
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
        except ValueError:
            # This isn't likely to happen (and it's not present in the source data like this)
            # Adding a contingency for it anyway.
            logging.warning('Caught ValueError when converting %s to datetime',
                            value['rental_start'])

        try:
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
        except ValueError:
            # rental_end may not be specified (i.e. if rental is ongoing), raising an exception
            # We'll want to flow change this so that we are filtering out rentals in-progress
            # (i.e., rental_end = '')
            logging.warning('Caught ValueError when converting %s to datetime',
                            value['rental_end'])

        value['total_days'] = (rental_end - rental_start).days

        if value['total_days'] < 0:
            # total_days is negative.
            # This occurs when rental_end occurs before rental_start (data may be flipped)
            # We have two options here: we can add some input validation on the front-end
            # to ensure that rental_end occurs after rental_start (preferred) or we can massage
            # the data set such that the later date is assumed to be rental_end.  This /seems/
            # fine but there may be unintended consequences of doing so so the preferred is safer.
            logging.error('Calculated invalid value for total_days (%s - %s = %s)',
                          value['rental_start'], value['rental_end'], value['total_days'])
        else:
            logging.debug('Calculated value for total_days (%s - %s = %s)',
                          value['rental_start'], value['rental_end'], value['total_days'])

        value['total_price'] = value['total_days'] * value['price_per_day']

        if value['total_price'] < 0:
            # total_days being negative leads to a negative total_price
            logging.error('Calculated invalid value for total_price (%s * %s = %s)',
                          value['total_days'], value['price_per_day'], value['total_price'])
        else:
            logging.debug('Calculated value for total_price (%s * %s = %s)',
                          value['total_days'], value['price_per_day'], value['total_price'])

        try:
            # negative total_price causes a ValueError when trying to get the square root
            # (evidently Python doesn't like imaginary numbers :) )
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
        except ValueError:
            logging.error('Caught ValueError when calculating sqrt_total_price for %s',
                          value['total_price'])
        else:
            logging.debug('Calculated value for sqrt_total_price (sqrt(%s) = %s)',
                          value['total_price'], value['sqrt_total_price'])

        try:
            # We'll get a divide-by-zero error if units_rented = 0 (which shouldn't happen).
            # We'll want to add some input validation on the front-end to make sure we don't end
            # up with this value in the data set.
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except ZeroDivisionError:
            logging.error('Caught ZeroDivisionError when calculating unit_cost (%s / %s)',
                          value['total_price'], value['units_rented'])
        else:
            logging.debug('Calculated value for unit_cost (%s / %s = %s)',
                          value['total_price'], value['units_rented'], value['unit_cost'])

    return data

def save_to_json(filename, data):
    '''
    Save processed data to filename as json.
    '''
    with open(filename, 'w') as file:
        json.dump(data, file)
        logging.debug('Wrote data to %s', filename)

if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    setup_logging(ARGS.debug)
    DATA = load_rentals_file(ARGS.input)
    DATA = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, DATA)
