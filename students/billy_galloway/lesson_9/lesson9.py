'''
Returns total price paid for individual rentals
'''
import argparse
import json
import datetime
import math
import logging
import sys



def logging_level(original_function):
    """
    sets log levels by taking a single argument
    and matching it to key in the dictionary
    """
    logger = logging.getLogger(__name__)
    LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
    formatter = logging.Formatter(LOG_FORMAT)
    log_file = datetime.datetime.now().strftime("%Y-%m-%d")+'.log'
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    levels = {
        0: logging.NOTSET,
        1: logging.ERROR,
        2: logging.WARNING,
        3: logging.DEBUG
    }

    def logger_func(*args, **kwargs):
        nonlocal logger
        logger.info(f"inner function: {cli_args}")
        
        if cli_args.debug:
            try:
                # debug arg found and passing the
                # integer to the logging_level method
                levels = logging_level(cli_args.debug)
                if levels == 10:
                    logger.setLevel(levels)
                    console_handler = logging.StreamHandler(sys.stdout)
                    console_handler.setFormatter(formatter)
                    logger.addHandler(console_handler)
                else:
                    logger.setLevel(levels)
                    logger.addHandler(file_handler)

            except KeyError:
                # If the debug value does not match
                # a key in the log level dict then exit
                # and log the reason for exiting
                logger.setLevel(logging.ERROR)
                logger.addHandler(file_handler)
                logger.error(f"Invalid debug option")
                sys.exit()

            else:
                data = load_rentals_file(args.input)
                data = calculate_additional_fields(data)

        else:
            logger.disabled = True
            data = load_rentals_file(args.input)
            data = calculate_additional_fields(data)
            save_to_json(args.output, data)


        return original_function(*args, **kwargs)
        
    return logger_func

def parse_cmd_arguments():
    """ Setups parser and returns arguments from the command line """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-d', '--debug', type=int, help='logging verbosity', required=False)

    return parser.parse_args()


@logging_level
def test_logging(cli_args):
    print(f"decorated function")
    # logger.info(f"info logs")
    # logger.warning(f"warning logs")
    # logger.debug(f"debug logs")


cli_args = parse_cmd_arguments()
test_logging(cli_args)