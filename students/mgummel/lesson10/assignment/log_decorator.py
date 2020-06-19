import logging
from timeit import default_timer as dt
import functools
from datetime import datetime

class LogDecorator(object):

    def __init__(self):
        self.logger = logging.getLogger('decorator-log')
        self.logger.setLevel(level=logging.DEBUG)
        # create file handler which logs even debug messages
        self.log_file = logging.FileHandler(f'timings.txt')
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s %(filename)s:%(lineno)-3d \
         %(levelname)s %(message)s')
        self.log_file.setFormatter(formatter)
        self.log_file.setLevel(logging.DEBUG)
        self.logger.addHandler(self.log_file)


    def __call__(self, fn):
        @functools.wraps(fn)
        def decorated(*args, **kwargs):
            try:
                self.logger.debug(f"{fn.__name__} - {args}")
                start = dt
                print('**********************************')
                print(start)
                print('**********************************')
                result = fn(*args, **kwargs)
                stop = dt
                #self.logger.debug(f"{fn.__name__} - {stop - start}")
                #return result
            except Exception as ex:
                self.logger.debug("Exception {0}".format(ex))
                raise ex
            return result
        return decorated
