'''
Function Timer
'''
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def timer(original_function):
    ''' Function to track time of other functions '''
    def checker(*args, **kwargs):
        ''' start timer and write out the final time counter '''
        start = time.perf_counter()
        functions_output = original_function(*args, **kwargs)
        end = time.perf_counter()
        total_time = end-start

        logger.info(f'Total time to run {original_function.__name__}  took: {total_time:2f}')

        return functions_output

    return checker