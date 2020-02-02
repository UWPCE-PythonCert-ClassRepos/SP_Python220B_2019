"""
Profiles CSV import performance of linear.py and parallel.py. Perform profiling with
both 1,000 entry and 1,000,000 entry files.
"""

import timeit
from time import perf_counter
import cProfile
import pstats

import linear
import parallel

from linear import DB_NAME


def delete_db_entries():
    """Delete entries of database so profiling is equal."""

    with linear.MongoManager() as mm:
        mm.db.product.delete_many({})
        mm.db.customers.delete_many({})
        mm.db.rentals.delete_many({})

        for name in ('products', 'customers', 'rentals'):
            mm.db.drop_collection(name)

    print("Database wiped", flush=True)


if __name__ == "__main__":

    labels = ("Thousand entries", "Fifty thousand entries")
    customers = ("customers.csv", "customers.csv_million.csv")
    products = ("products.csv", "products.csv_million.csv")

    N = 10

    for i in range(2):

        label = labels[i]
        cust = customers[i]
        prod = products[i]

        # Profile linear function
        delete_db_entries()
        cProfile.runctx(f"linear.import_data('data', '{cust}', '{prod}', 'rentals.csv')",
                        globals(), locals(), filename='profile_linear')
        p = pstats.Stats('profile_linear')
        print(f"{label} Linear profile:")
        p.strip_dirs().sort_stats(pstats.SortKey.TIME).print_stats(15)

        # Profile parallel function
        delete_db_entries()
        cProfile.runctx(f"parallel.import_data('data', '{cust}', '{prod}', 'rentals.csv')",
                        globals(), locals(), filename='profile_parallel')
        p = pstats.Stats('profile_parallel')
        print(f"{label} Parallel profile")
        p.strip_dirs().sort_stats(pstats.SortKey.TIME).print_stats(15)

        lin = timeit.timeit(f"linear.import_data('data', '{cust}', '{prod}', 'rentals.csv')",
                            setup="delete_db_entries()", number=N, globals=globals())

        par = timeit.timeit(f"parallel.import_data('data', '{cust}', '{prod}', 'rentals.csv')",
                            setup="delete_db_entries()", number=N, globals=globals())

        print(f"{label} Linear: ", lin / N)
        print(f"{label} Parallel: ", par / N)


    # # Profile parallel function
    # start = perf_counter()
    # res = parallel.import_data('data', 'customers.csv', 'products.csv', 'rentals.csv')
    # t = perf_counter() - start
    # # cProfile.runctx("parallel.import_data('data', 'customers.csv', 'products.csv', 'rentals.csv')",
    # #                 globals(), locals(), filename='profile_parallel')
    # # p = pstats.Stats('profile_parallel')
    # # p.strip_dirs().sort_stats(pstats.SortKey.TIME).print_stats()
    #
    # print("Parallel code took: ", t, " seconds")
    #
