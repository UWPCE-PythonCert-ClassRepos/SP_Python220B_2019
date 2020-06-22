import logging
import sys
import functools
from datetime import datetime

def set_logger():
    logger = logging.getLogger('decorator-log')
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)

class LogDecorator(object):

    def __init__(self, debug_mode=None):
        set_logger()
        self.logger = logging.getLogger('decorator-log')
        if debug_mode:
            self.logger = logging.getLogger('decorator-log')
            self.logger.setLevel(level=logging.DEBUG)

            # create file handler which logs even debug messages
            self.log_file = logging.FileHandler(f'{datetime.now().strftime("%Y-%m-%d")}.log')

            # create console handler with a higher log level
            self.log_stdout = logging.StreamHandler(sys.stdout)

            # create formatter and add it to the handlers
            formatter = logging.Formatter('%(asctime)s %(filename)s:%(lineno)-3d \
             %(levelname)s %(message)s')
            self.log_stdout.setFormatter(formatter)
            self.log_file.setFormatter(formatter)

            self.log_file.setLevel(logging.WARNING)

            self.logger.addHandler(self.log_stdout)
            self.logger.addHandler(self.log_file)
        else:
            self.logger = None
            logging.disable(logging.CRITICAL)


    def __call__(self, fn):
        @functools.wraps(fn)
        def decorated(*args, **kwargs):
            try:

                self.logger.debug("{0} - {1} - {2}".format(fn.__name__, args, kwargs))
                result = fn(*args, **kwargs)
                self.logger.debug(result)
                return result
            except Exception as ex:
                self.logger.debug("Exception {0}".format(ex))
                raise ex
            return result
        return decorated
