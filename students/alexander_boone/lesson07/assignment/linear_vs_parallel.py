'''Compares runtimes for linear vs parallel data imports'''

from linear import import_data_linear
from parallel import import_data_parallel

DIRECTORY = 'testfiles'
PROD_FILE = 'prod_file_new.csv'
CUST_FILE = 'cust_file_new.csv'
RENTAL_FILE = 'rental_file_new.csv'

def runtime_import_data_linear():
    '''
    Print the runtime of the HP Norton Database
    import_data_linear function.
    '''

    counts_linear = import_data_linear(DIRECTORY, PROD_FILE, CUST_FILE, RENTAL_FILE)
    linear_runtime = str(counts_linear[0][3])
    print('Linear runtime (s): ' + linear_runtime)


def runtime_import_data_parallel():
    '''
    Print the runtime of the HP Norton Database
    import_data_parallel function.
    '''

    counts_parallel = import_data_parallel(DIRECTORY, PROD_FILE, CUST_FILE, RENTAL_FILE)
    parallel_runtime = str(counts_parallel[0][3])
    print('parallel runtime (s): ' + parallel_runtime)


# Run test functions
if __name__ == '__main__':
    runtime_import_data_linear()
    runtime_import_data_parallel()
