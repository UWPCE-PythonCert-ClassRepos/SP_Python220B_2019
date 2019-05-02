"""Program that runs in parallel"""
import csv
import time
import queue as Queue
from threading import Thread
import pymongo
#pylint: disable=C0103,W0702,W0613,W0612,C0200

class db_thread(Thread):
    """db_thread class - so program runs in parallel"""

    def __init__(self, q, collection_name, csv_file):
        """db_thread object initializer"""
        self.queue = q
        self.collection_name = collection_name
        self.csv_file = csv_file
        super().__init__()

    def run(self):
        """Creates database, counts items in database and errors"""
        start = time.time()
        db_collection = db[self.collection_name]
        start_count = db_collection.count_documents({})
        db_list = csv_convert(self.csv_file)
        db_errors = 0
        for item in db_list:
            try:
                db_collection.insert_one(item)
            except:
                db_errors += 1
        out_list = (self.collection_name,
                    db_collection.count_documents({}) - start_count,
                    start_count, db_collection.count_documents({}),
                    time.time() - start)
        self.queue.put(out_list)
        self.queue.task_done()
        #return None

def import_data(directory_name, product_file, customer_file, rentals_file):
    """
    This function takes a directory name three csv files as input,
    one with product data, one with customer data and the third one with
    rentals data and creates and populates a new MongoDB database
    with these data.

    # Each module will return a list of tuples, one tuple for customer and
    # one for products. Each tuple will contain 4 values:
    # 1. the number of records processed (int)
    # 2. the record count in the database prior to running (int)
    # 3. the record count after running (int), and the time taken to run
    # the module (float).
    """
    db_queue = Queue.Queue()

    product_thread = db_thread(db_queue, 'products', product_file)
    customer_thread = db_thread(db_queue, 'customers', customer_file)
    rental_thread = db_thread(db_queue, 'rental', rentals_file)

    threads = []
    threads.append(product_thread)
    threads.append(customer_thread)
    threads.append(rental_thread)
    for thread in threads:
        thread.start()

    db_queue.join()

    output = []
    for item in range(len(threads)):
        output.append(db_queue.get())

    return output

def csv_convert(f):
    """Converts csv file rows into a dict for use in database"""
    dict_list = []
    with open(f, newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        row1 = next(csv_reader)
        for row in csv_reader:
            dict_row = {}
            for n in range(len(row1)):
                dict_row[row1[n]] = row[n]
            dict_list.append(dict_row)
        return dict_list

if __name__ == "__main__":
    starting = time.time()
    client = pymongo.MongoClient()
    with client:
        db = client['mydatabase']
        print(import_data('', 'products.csv', 'customers.csv',
                          'rentals.csv'))
        ending = time.time()
        print('Run time: {}'.format(ending - starting))
