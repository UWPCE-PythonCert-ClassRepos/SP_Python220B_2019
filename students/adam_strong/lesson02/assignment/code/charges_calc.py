#!/usr/bin/env python
'''
Returns total price paid for individual rentals:
   argparse options:

        required: -i INPUT FILE -o OUTPUT FILE
        optional: -d # (Debug levels:
                        0 - No error logging (DEFAULT)
                        1 - Only error messages (causing it to crash)
                        2 - Only warnings (skipped records, how many errors)
                        3 - All warnings (including script flow indicators)
'''
import argparse
import json
import datetime
import math
import sys
import logging

logger = logging.getLogger()
LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
log_file = 'logs/charges_calc' + datetime.datetime.now().strftime('%Y-%m-%d')+'.log'
formatter = logging.Formatter(LOG_FORMAT)
logger.setLevel(logging.DEBUG)


# MAIN CODE___________________________________________________________________

def parse_cmd_arguments():
    '''Interpret the command line arguments, -i INPUT, -o OUTPUT, -d DEBUG'''
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-debug', '-d', type=int, default=0, required=False,
                        choices=[0, 1, 2, 3],
                        help='Debug Level: 0=No debug messages or log file, \
                        1=Only error messages, 2=Error messages and warnings,\
                        3=Error messages, warnings and debug messages')
    try:
        return parser.parse_args()
    except TypeError:
        sys.exit()

def set_logger(debug):
    '''Sets the logging level input from command line'''
    if debug > 0:
        if debug == 1:
            set_handlers(logging.ERROR)
        elif debug == 2:
            set_handlers(logging.WARNING)
        elif debug == 3:
            set_handlers(logging.DEBUG)
    else:
        logging.disable(logging.CRITICAL)


def set_handlers(log_level):
    '''Sets all the handlers based on level selected in set_logger(debug)'''
    file_handler = logging.FileHandler(log_file)
    if log_level == logging.DEBUG:
        file_handler.setLevel(logging.WARNING)
    else:
        file_handler.setLevel(log_level)

    file_handler.setFormatter(formatter)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def load_rentals_file(filename):
    '''Opens up the json file'''
    with open(filename) as file:
        logging.debug('In load_rentals_file, filename is %s', filename)
        try:
            source_data = json.load(file)
        except FileNotFoundError:
            logging.error('Exiting in load_rentals_file() exception error')
            sys.exit()
    logging.debug('Data has been successfully loaded')
    return source_data

def calculate_additional_fields(process_data):
    '''Main processer of the data'''
    for value in process_data.values():
        try:
            errcount = 0 # Using a counting system to ensure all errors are captured
            logging.debug('Inputted record: %s', str(value)) # What is the value to be processed

            #Checking that rental start has a real value
            if value['rental_start'] == '':
                errcount += 1
                logging.warning('No start date')
            else:
                rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
                logging.debug('Real start date value')

            #Checking that rental end has a value
            if value['rental_end'] == '':
                errcount += 1
                logging.warning('No end date')
            else:
                rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
                logging.debug('Real end date value')

            #If the dates are real, check that end date follows the start date
            if errcount == 0:
                value['total_days'] = (rental_end - rental_start).days
                #Checking that there is at least 1 day of rental
                if value['total_days'] <= 0:
                    errcount += 1
                    logging.warning('Total days is 0 or less, skipping calculations')
                    value['total_days'] = 'ERROR'
                else:
                    logging.debug('Value from total days calculation %s', str(value['total_days']))

            #Proceeding if no errors
            if errcount == 0:
                value['total_price'] = value['total_days'] * value['price_per_day']
                # Math domain error will occur if there is a negative value
                value['sqrt_total_price'] = math.sqrt(value['total_price'])
                value['unit_cost'] = value['total_price'] / value['units_rented']
                logging.debug('SUCCESS calculating: %s', str(value))
            else:
                logging.warning('Skip: %s, %sError', str(value['product_code']), str(errcount))

        except ValueError:
            logging.error('Exiting in calculate_additional_fields() exception error')
            sys.exit()

    return process_data

def save_to_json(filename, write_data):
    '''Write the modified json file to out.json'''
    logging.debug('Writing to file')
    with open(filename, 'w') as file:
        json.dump(write_data, file)


if __name__ == "__main__":
    args = parse_cmd_arguments()
    set_logger(args.debug)
    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)
