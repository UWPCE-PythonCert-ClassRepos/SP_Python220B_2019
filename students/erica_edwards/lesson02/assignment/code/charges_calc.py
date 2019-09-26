'''
Returns total price paid for individual rentals 

Logging:

PDB (Command Line):
The basic information found in parse_cmd_arguments is needed to use PDB. The defaults for --input 
and --output have been set to the current file names. If the file names are different this information 
must be entered. --debug has 4 options for logging messages. 0 = No Messages, 1 = Error Messages, 
2 = Error and Warning messages, and 3 = Error, warning, and debug. Default is 3.

Console logging:
All error, warnings, and debug messages are printed to the console. Debug messages are used for flow
of the script and to log information. Warnings are used to call attention to changes in the data or 
flow. For example if the date entered into the program for rental_start and rental_end are the same a warning is 
issued to notify the programmer of the change in rental days from zero to one. Errors are used to call attention
to issues that will cause major issues with the script in either completing the script or in the information
saved to output.json.

File logging:
All errors and warnings are saved to the file while the script is running. 

Note: The source file is not scrubbed before it is run through the script. Data that is found to have errors
while processing is removed from output.json

'''
import argparse
import json
import datetime
import math
import logging
import os


def parse_cmd_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', default="source.json", required=False,)
    parser.add_argument('-o', '--output', help='ouput JSON file', default="output.json", required=False)
    parser.add_argument('-d', '--debug', type=int, default=3,
                        help='Debug Level 0-3', required=False)
    return parser.parse_args()

def init_logger(level):
    """Setting up logging"""
    logger = logging.getLogger()

    # Format log
    log_file = datetime.datetime.now().strftime("%Y-%m-%d")+'.log'
    log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"

    #Set-up format
    formatter = logging.Formatter(log_format)

    #Create filehandler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(formatter)

    #Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    # Set log level
    if args.debug == 0:
        logger.disabled = True
    elif args.debug == 1:
        logger.setLevel(logging.ERROR)
    elif args.debug == 2:
        logger.setLevel(logging.WARNING)
    elif args.debug == 3:
        logger.setLevel(logging.DEBUG)
    else:
        raise ValueError("logging level incorrect.")

    #Adding filehandler and console handler to the log
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def load_rentals_file(filename):
    """Load source json file"""

    # Checking what the current directory is.
    logging.debug(f"cwd is {os.getcwd()}")
    #Checking file name path.
    logging.debug(f"filename is {filename}")
    # Discovered that I needed to start the try before the open().
    try:
        with open(filename) as file:
            # Flow check 
            logging.debug(f"Before loading json file")
            data = json.load(file)
            # Confirming file was loaded
            logging.debug(f"After loading json file")
    except Exception as e:
            # Checking for exception that caused the file to not be loaded
            logging.error(f"Exception while loading json file: {e} ")
            exit(0)
    return data

def calculate_additional_fields(data):
    """Calculating additional fields based on information provided in source.json"""

    # Check that data was loaded into the output.json file.
    logging.debug(f"In calculate_additional_fields len(data): {len(data)}")
    # Create list to track keys associated with bad data.
    bad_data_keys = []
    for key, value in data.items():
        try:
            # Log the rental id.
            logging.debug(f"Rental Id: {key}")

            # Checking flow of script
            logging.debug(f"Before rental_start")
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')

            # Checking flow of script
            logging.debug(f"Before rental_end")
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')

            # Checking flow of script
            logging.debug(f"Before total_days")
            value['total_days'] = (rental_end - rental_start).days
            
            # Add bad key to list 
            if value['total_days'] < 0:
                logging.error(f"Total_days is less than 0: {value['total_days']}")
                logging.error(f"Rejecting this record {key}.")
                bad_data_keys.append(key)
                continue
            # Change total_days value to 1 for billing 
            elif value['total_days'] < 1:
                # Logging value of total days is 0
                logging.warning(f"Total_days is {value['total_days']}. Billing for one day.")
                value["total_days"] = 1  
                # Warning that a value was changed.
                logging.warning(f"Changed value['total_days'] to 1")

            # Checking flow of script
            logging.debug(f"Before total_price")
            value['total_price'] = value['total_days'] * value['price_per_day']

            #Check the value of total_price to make sure number is not negative           
            logging.debug(f"Before sqrt_total_price: value['total_price']: {value['total_price']}")
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
           
            # Checking flow of script
            logging.debug(f"Before unit_cost")
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except Exception as e:
            # Log reason for exception
            logging.error(f"Exception while calculating additional fields: {e} ")
            # Data is bad so add rental)id(key) to list
            logging.error(f"Rejecting this record {key}.")
            bad_data_keys.append(key)
            continue
    # Count of records deleted from file
    logging.warning(f"Deleting {len(bad_data_keys)} keys containing bad data")
    for key in bad_data_keys: 
        del data[key] 

    return data

def save_to_json(filename, data):
    """Save data to output.json file"""
    with open(filename, 'w') as file:
        json.dump(data, file)

if __name__ == "__main__":
    args = parse_cmd_arguments()
    init_logger(3)
    # logging.info("*"*60)
    # logging.info("* Program Start" + (" "*44) + "*" )
    # logging.info("*"*60)
    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)
