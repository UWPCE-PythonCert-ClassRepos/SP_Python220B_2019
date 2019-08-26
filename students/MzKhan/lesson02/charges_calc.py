'''
Returns total price paid for individual rentals
'''
import argparse
import json
import datetime
import math
import logging

#pylint: disable = w0621, c0103

def parse_cmd_arguments():
    """
    Parse command line arguments.
    :parm input: json file -required argument.
    :parm output: json file - required argument.
    :parm debug: debug level - optional argument. default=0
    :return parsed arguments.
    """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='Debug log level', required=False,
                        default=0, type=int, choices=range(0, 4))

    return parser.parse_args()


def create_logger(level=0):
    """
    Create the logger object.
    :parm level: log level optional.
    :return: logger object
    """
    log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
    log_file = datetime.datetime.now().strftime("%Y-%m-%d")+'.log'
    formatter = logging.Formatter(log_format)
    #Create a new logger.
    logger = logging.getLogger()
    if level:
        #Create a file handler and set the message formatter.
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        #Create a console_handler and set the message formatter.
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        #Set the logger level to DEBUG.
        logger.setLevel(logging.DEBUG)
        # Add the handlers to the logger.
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
    else:
        logger.setLevel(logging.CRITICAL)    # Set the logger level to critical.
    # Set the different log levels for file handler and stream handler based on
    # the debug level argument.
    if level == 1:
        file_handler.setLevel(logging.ERROR)
        stream_handler.setLevel(logging.ERROR)
    elif level == 2:
        file_handler.setLevel(logging.WARNING)
        stream_handler.setLevel(logging.WARNING)
    elif level == 3:
        file_handler.setLevel(logging.WARNING)
        stream_handler.setLevel(logging.DEBUG)

    return logger


def load_rentals_file(filename):
    """
    :parm filename: input file in the json format.
    :return: file content.
    """
    logger.debug('Loading the input file')
    try:            # moved the try catch block outside of with open(...)
        with open(filename) as file:
            data = json.load(file)
    except FileNotFoundError:
        err_msg = f"Input file {filename} is not found"
        logging.error(err_msg)
        exit(0)
    return data


def calculate_additional_fields(data):
    """
    Process the input data.
    :parm data: input data from source file.
    :return data: processed data.
    """
    logger.debug('Calculing the additional fields')
    for key, value in data.items():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            value['total_days'] = (rental_end - rental_start).days
            if value['total_days'] < 0:
                raise ValueError(f'rental_start date > rental_end date for the key: {key}')
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except ValueError as val_err:
            logger.warning(val_err)
            continue
        except KeyError as key_err:
            logger.warning(key_err)
            continue
    return data


def save_to_json(filename, data):
    """write the data to a json file"""
    msg = f'Save the data to the file {filename}'
    logger.debug(msg)
    with open(filename, 'w') as file:
        json.dump(data, file)


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    logger = create_logger(ARGS.debug)
    INPUT_DATA = load_rentals_file(ARGS.input)
    OUTPUT_DATA = calculate_additional_fields(INPUT_DATA)
    save_to_json(ARGS.output, OUTPUT_DATA)
