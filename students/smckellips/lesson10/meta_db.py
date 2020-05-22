'''
External code to simulate working with legacy classes.
We import the legacy code without modification.
'''
from functools import wraps
from time import time

from database_cls import HPNorton, MongoDBConnection


def timing_decorator(func):
    '''Decorator function for timing.'''
    @wraps(func)
    def return_function(*args, **kwargs):
        time_start = time()
        result = None
        result = func(*args, **kwargs)
        time_end = time()
        HPNorton.LOGGER.info('function: %s args: [%s, %s] took: %2.4f sec',
                    func.__name__, args, kwargs, time_end-time_start)
        if result and '_data' in func.__name__:
            HPNorton.LOGGER.info('function return: %s', result)
        elif isinstance(result, list):
            HPNorton.LOGGER.info('function returns %s records', len(result))

        return result
    return return_function


if __name__ == "__main__":
    for name in vars(HPNorton):
        if not name.startswith('__'):
            base = getattr(HPNorton, name)
            if hasattr(base, '__call__'):
                setattr(HPNorton, name, timing_decorator(base))

    mongo = MongoDBConnection()
    with mongo:
        mongo.connection.drop_database(HPNorton.DB_NAME)

    count, errors = HPNorton.import_data(
        'data', 'products.csv', 'customers.csv', 'rentals.csv')

