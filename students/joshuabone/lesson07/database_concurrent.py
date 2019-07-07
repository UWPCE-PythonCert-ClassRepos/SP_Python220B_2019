"""Use a concurrent approach to importing rental info into MongoDB."""
import concurrent.futures
import logging
import database_linear as dbl

logging.basicConfig(level=logging.INFO)

# EXAMPLE RUN:
# INFO:root:Imported 10000 products, 10000 customers, and 10000 rentals.
# (split time: 7.373854 secs, total time: 7.373854 secs).
if __name__ == "__main__":
    MONGO = dbl.MongoDBConnection()

    with MONGO:
        dbl.DATABASE = MONGO.connection.rentals

    STOPWATCH = dbl.Stopwatch()
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        PROD_FUTURE = executor.submit(lambda:
                                      dbl.import_from_csv('data/products.csv',
                                                          dbl.import_product))
        CUST_FUTURE = executor.submit(lambda:
                                      dbl.import_from_csv('data/customers.csv',
                                                          dbl.import_customer))
        RENT_FUTURE = executor.submit(lambda:
                                      dbl.import_from_csv('data/rentals.csv',
                                                          dbl.import_rental))
    STOPWATCH.mark_and_log(f"Imported {PROD_FUTURE.result()} products, "
                           f"{CUST_FUTURE.result()} customers, and "
                           f"{RENT_FUTURE.result()} rentals.")
    dbl.drop_data()
