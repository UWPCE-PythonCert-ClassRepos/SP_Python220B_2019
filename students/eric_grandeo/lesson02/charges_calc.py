'''
Returns total price paid for individual rentals 
'''
import argparse
import json
import datetime
import math
import logging

logging.basicConfig(level=logging.DEBUG)

def parse_cmd_arguments():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)

    return parser.parse_args()


def load_rentals_file(filename):    
    try:
        with open(filename) as file:
            logging.debug('JSON file: {}'.format(filename))
            data = json.load(file)
    except FileNotFoundError:
        logging.error("File not found")
        exit(0)
    return data

def calculate_additional_fields(data):
    for value in data.values():
        try:
            logging.info("Called with value: {}".format(value))
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            logging.debug('Rental start: {}'.format(value['rental_start']))
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            logging.debug('Rental ends: {}'.format(value['rental_end']))
            value['total_days'] = (rental_end - rental_start).days
            logging.debug('Total days: {:d}'.format(value['total_days']))
            if value['total_days'] < 0:
                logging.warning("Total days must not be negative")
            #program exits if total days is negative; end date is before start date
            value['total_price'] = value['total_days'] * value['price_per_day']
            logging.debug('Total price: ${:,.2f}'.format(value['total_price']))
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            logging.debug('Square root of total price: {:06.2f}'.format(value['sqrt_total_price']))
            value['unit_cost'] = value['total_price'] / value['units_rented']
            logging.debug('Unit cost: ${:,.2f}'.format(value['unit_cost']))
        except ValueError:
            #exit(0)
            logging.error("Total days must not be negative")

    return data

def save_to_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file)

if __name__ == "__main__":
    args = parse_cmd_arguments()
    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)
