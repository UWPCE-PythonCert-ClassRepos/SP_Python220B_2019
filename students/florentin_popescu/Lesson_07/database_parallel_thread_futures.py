# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 08:59:40 2019
Modified on Mon Aug 26 10:11:41 2019
@author: Florentin Popescu
"""

# imports
import csv
import logging
import time as tm
# -----------------------------

# imports for paralel processing
import threading
import concurrent.futures as cof
# -----------------------------

import psutil
from pymongo import MongoClient
from memory_profiler import memory_usage
# ==================================

# set basic looging level as INFO
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.info("database_parallel_thread_futures.py")
LOGGER.info("loger active")
# ==================================

MEM_USAGE = memory_usage(proc=-1, interval=.1, timeout=None)
# ===============================


class Timer():
    """
        times execcution
    """
    def __init__(self):
        """ init """
        self.start = tm.perf_counter()

    def __repr__(self):
        """ repper """
        return f"timer started at: {self.start}"

    def get_time_hh_mm_ss_mss(self):
        """ display passed time """
        end = tm.perf_counter()
        milisec = ((end - self.start) % 1) * 1000
        mnt, sec = divmod(end - self.start, 60)
        hrs, mnt = divmod(mnt, 60)
        time_str = "h:m:s:ms>> %02d:%02d:%02d:%3d" % (hrs, mnt, sec, milisec)
        return time_str
# ==================================


class MongoDBConnection():
    """ establish MongoDB connection """
    def __init__(self, host='127.0.0.1', port=27017):
        """ use public ip-address and port """
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        """ enter """
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ exit """
        self.connection.close()
# ==================================


def worker_insert_records(dbs, data):
    """ worker for parallel processing """
    dbs.insert_many(data)
# ==================================


def csv_to_mongo_thread(path, db_name):
    """ import records from file to mongodb via thread"""
    try:
        timer, lock = Timer(), threading.Lock()
        # -----------------------------------------

        mongo = MongoDBConnection()
        with mongo:
            database = mongo.connection.FlorentinDB
            dbs = database[db_name]

            prior_count = dbs.estimated_document_count()

            with open(path, "r") as csvfile:
                csv_dct = csv.DictReader(csvfile, delimiter=",")
                csv_lst = list(csv_dct)
                insert_count = len(csv_lst)

                lock.acquire()
                thread = threading.Thread(target=worker_insert_records,
                                          args=(dbs, csv_lst))
                thread.start()
                lock.release()
                thread.join()

            after_count = dbs.estimated_document_count()
        # -----------------------------------------
        return (insert_count, prior_count, after_count,
                timer.get_time_hh_mm_ss_mss())

    except (FileNotFoundError, UnboundLocalError) as err:
        LOGGER.info("path-indicated file not found")
        LOGGER.info(err)
# ==================================


def csv_to_mongo_futures(path, db_name):
    """ import records one-by-one from file to mongodb via futures """
    try:
        timer = Timer()
        # -----------------------------------------

        mongo = MongoDBConnection()
        with mongo:
            database = mongo.connection.FlorentinDB
            dbs = database[db_name]

            prior_count = dbs.estimated_document_count()

            with open(path, "r") as csvfile:
                csv_dct = csv.DictReader(csvfile, delimiter=",")
                csv_lst = list(csv_dct)
                insert_count = len(csv_lst)

                worker_insert_records(dbs, csv_lst)

                # ---------one-by-one--------------
                # insert_count = 0
                # for record in csv_dct:
                #    row = dict(map(list, zip(list(record.keys()),
                #                             list(record.values()))))
                #    dbs.insert_one(row)
                #    insert_count += 1
                # ---------------------------------

            after_count = dbs.estimated_document_count()
        # -----------------------------------------
        return (insert_count, prior_count, after_count,
                timer.get_time_hh_mm_ss_mss())

    except (FileNotFoundError, UnboundLocalError) as err:
        LOGGER.info("path-indicated file not found")
        LOGGER.info(err)
# ==================================


def main_parallel_thread(repo, colection):
    """ main function parallel_thread """
    timer = Timer()
    # -----------------------
    tpl0 = csv_to_mongo_thread(repo[0], colection[0])
    LOGGER.info("<Thread> inserted file:%s", repo[0])
    tpl1 = csv_to_mongo_thread(repo[1], colection[1])
    LOGGER.info("<Thread> inserted file:%s", repo[1])
    # -----------------------
    LOGGER.info("<T> script cpu usage: %s%%", psutil.cpu_percent())
    LOGGER.info("<T> script memory usage:%s", MEM_USAGE)
    LOGGER.info("<T> script total runtime: %s", timer.get_time_hh_mm_ss_mss())
    # -----------------------

    drop_data()

    return tuple(item for item in tpl0), tuple(item for item in tpl1)
# ==================================


def main_parallel_futures(repo, colection):
    """ main function """
    timer = Timer()
    # -----------------------
    with cof.ThreadPoolExecutor(max_workers=2) as ex:
        ft0 = ex.submit(lambda: csv_to_mongo_futures(repo[0], colection[0]))
        LOGGER.info("<Futures> inserted file:%s", repo[0])
        ft1 = ex.submit(lambda: csv_to_mongo_futures(repo[1], colection[1]))
        LOGGER.info("<Futures> inserted file:%s", repo[1])
    # -----------------------
    LOGGER.info("<F> script cpu usage: %s%%", psutil.cpu_percent())
    LOGGER.info("<F> script memory usage:%s", MEM_USAGE)
    LOGGER.info("<F> script total runtime: %s", timer.get_time_hh_mm_ss_mss())
    # -----------------------

    drop_data()

    return ft0.result(), ft1.result()
# ==================================


def drop_data():
    """
        drop data from MongoDB
    """
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.FlorentinDB

    dbs = ["product", "customer", "rental"]
    for name in dbs:
        database[name].drop()

    return "data has been dropped from Mongo database"
# ==================================


def show_available_products():
    """
        list available products
    """
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.FlorentinDB

    products = database["product"].find({"quantity_available": {"$ne": "0"}})
    products_dict = {prod["product_id"]:
                     {"description": prod["description"],
                      "product_type": prod["product_type"],
                      "quantity_available": int(prod["quantity_available"])}
                     for prod in products}
    return products_dict
# ==================================


def show_rentals(product_id):
    """
        list customers that rented products
    """
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.FlorentinDB

    rentals = database["rental"].find({"product_id": product_id})\
        .sort("customer_id")
    rental_list = [rental["customer_id"] for rental in rentals]
    customers = database["customer"].find({"customer_id":
                                           {"$in": rental_list}})
    cust_dict = {cust["customer_id"]:
                 {"name": f"{cust['first_name']} {cust['last_name']}",
                  "address": cust["address"],
                  "phone": cust["phone"],
                  "email": cust["email"]}
                 for cust in customers}
    return cust_dict
# ==================================


def print_products():
    """
        print products
    """
    products = show_available_products()
    for prod in products:
        print(prod, products[prod])
# ==================================


# if __name__ == "__main__":
#    PATH = "csvdata/customers.csv", "csvdata/products.csv"
#    COLECTION = "customer", "product"
#
#    RESULTS_THREAD = main_parallel_thread(PATH, COLECTION)
#    LOGGER.info(RESULTS_THREAD)
#
#    RESULTS_FUTURES = main_parallel_futures(PATH, COLECTION)
#    LOGGER.info(RESULTS_FUTURES)

# Exemple run
# INFO:__main__:database_parallel_thread_futures.py
# INFO:__main__:loger active
# INFO:__main__:<Thread> inserted file:csvdata/customers.csv
# INFO:__main__:<Thread> inserted file:csvdata/products.csv
# INFO:__main__:<T> script cpu usage: 34.7%
# INFO:__main__:<T> script memory usage:[114.65234375]
# INFO:__main__:<T> script total runtime: h:m:s:ms>> 00:00:00:145
# INFO:__main__:((1000, 0, 1000, 'h:m:s:ms>> 00:00:00: 76'),
#                (1000, 0, 1000, 'h:m:s:ms>> 00:00:00: 60'))
# INFO:__main__:<Futures> inserted file:csvdata/customers.csv
# INFO:__main__:<Futures> inserted file:csvdata/products.csv
# INFO:__main__:<F> script cpu usage: 35.6%
# INFO:__main__:<F> script memory usage:[114.65234375]
# INFO:__main__:<F> script total runtime: h:m:s:ms>> 00:00:00:127
# INFO:__main__:((1000, 0, 1000, 'h:m:s:ms>> 00:00:00: 84'),
#                (1000, 0, 1000, 'h:m:s:ms>> 00:00:00:118'))
# ==================================
