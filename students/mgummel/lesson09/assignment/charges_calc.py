'''
Returns total price paid for individual rentals
'''
import argparse
import json
import datetime
import math
import sys
import functools
import logging


class LogDecorator(object):

    def __init__(self, debug_mode=None):
        self.logger = logging.getLogger('decorator-log')
        self.logger.setLevel(level=logging.DEBUG)
        if debug_mode:
            # create file handler which logs even debug messages
            self.log_file = logging.FileHandler(f'{datetime.datetime.now().strftime("%Y-%m-%d")}.log')

            # create console handler with a higher log level
            self.log_stdout = logging.StreamHandler(sys.stdout)

            # create formatter and add it to the handlers
            formatter = logging.Formatter('%(asctime)s %(filename)s:%(lineno)-3d \
             %(levelname)s %(message)s')
            self.log_stdout.setFormatter(formatter)
            self.log_file.setFormatter(formatter)

            self.log_file.setLevel(logging.DEBUG)

            self.logger.addHandler(self.log_stdout)
            self.logger.addHandler(self.log_file)

        else:
            logging.disable(logging.CRITICAL)


    def __call__(self, fn):
        @functools.wraps(fn)
        def decorated(*args):
            try:
                self.logger.debug("{0} - {1}".format(fn.__name__, args))
                result = fn(*args)
                self.logger.debug(result)
                return result
            except FileNotFoundError as fe:
                self.logger.error(f"Exception {fe}")
            except ValueError as ve:
                self.logger.error(f"Exception {ve}")
            except Exception as ex:
                self.logger.error(f"Exception {ex}")
            return
        return decorated

def parse_cmd_arguments():
    """
    Parses all arguments provided to the script at runtime.
    :return:
    """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='output JSON file', required=True)
    parser.add_argument('-d', '--debug', help='adds logging to program', action='store_const', default=False, const=True, required=False)

    arguments = parser.parse_args()

    if arguments.debug:
        global logger
        logger = LogDecorator("debug")
    else:
        logger = LogDecorator()

    return arguments


if __name__ == "__main__":
    args = parse_cmd_arguments()

    @logger
    def load_rentals_file(filename):
        """
        Loads the input file to be parsed by the rest of the program. Exits
        if the file is not found.
        :param filename:
        :return:
        """
        try:
            with open(filename) as file:
                data = json.load(file)
        except FileNotFoundError as ex:
            raise ex
        return data


    def calculate_additional_fields(data):
        """
        Parses through data and calculates all fields needed to for rental
        data metrics.
        :param input_data: dictionary of rental transactions
        :return:
        """

        for value in data.values():
            try:
                rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
                rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
                value['total_days'] = (rental_end - rental_start).days
                value['total_price'] = value['total_days'] * value['price_per_day']
                value['sqrt_total_price'] = math.sqrt(value['total_price'])
                value['unit_cost'] = value['total_price'] / value['units_rented']
            # Sometimes a negative value is calculated for "total_price". When this occurs
            # the following expressions will throw an error.
            except ValueError as e:
                raise(e)


            # LOGGER.debug(f'Updated rental item entry: {value}')
        return data


    def save_to_json(filename, updated_data):
        """
        Takes all calculated data and writes to a file specified from the
        command line argument when running the script

        :param filename: file to write
        :param updated_data: data to write to filename
        """
        with open(filename, 'w') as file:
            json.dump(updated_data, file)


    input_data = load_rentals_file(args.input)
    calculated = calculate_additional_fields(input_data)
    save_to_json(args.output, calculated)
