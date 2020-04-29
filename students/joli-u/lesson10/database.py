"""
database.py
Assignment 10
Joli Umetsu
PY220
"""
import time
import csv
from pymongo import MongoClient
from pymongo.errors import BulkWriteError, DuplicateKeyError


def write_data(*args, **kwargs):
    ip = {0: 'products', 1: 'customers', 2: 'rentals'}

    with open('timings.txt', 'a') as f:
        # get_data or import_data methods
        if len(args) > 2:
            # import_data method
            if "tuple" in str(type(args[3])):
                f.write("\nName: {}".format(args[0]))
                f.write("\nTime: {:.10f} seconds".format(args[1][-1]))
                f.write(f"\nProc: {sum(args[3])} records")
                for i, n in enumerate(args[3]):
                    f.write(f"\n\t ({n} {ip[i]})")
                f.write("\n")
            # get_data method
            else:
                f.write(f"\nName: {args[0]} ({args[2][-1][6:]})")
                f.write("\nTime: {:.10f} seconds\n".format(args[1][-1]))
                if "rental" in args[2][-1][6:]:
                    t_tot = sum(args[1][-3:])
                    f.write("\t/ {:.10f} seconds [Total: get_data]\n".format(t_tot))
        # other methods
        elif len(args) > 1:
            f.write("\nName: {}".format(args[0]))
            f.write("\nTime: {:.10f} seconds\n".format(args[1]))

        else:
            f.write("\n-----------------------------------------------")



def timer(func, *args, **kwargs):
    """
    Times runtime of function
    Returns: Function, modified with timing data
    """
    t_import = []
    def timed_func(*args, **kwargs):
        time_i = time.time()
        mod_func = func(*args, **kwargs)
        time_d = time.time() - time_i

        if "data" in func.__name__:
            t_import.append(time_d)
            write_data(func.__name__, t_import, args, mod_func[0])
        else:
            write_data(func.__name__, time_d)
        
        return mod_func

    return timed_func



class MongoDB():
    """
    Context manager to connect/access MongoDB
    """
    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.connection = None
        self.database = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        self.database = self.connection.media
        return self.database

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()



class Timed(type):
    """
    Metaclass
    """
    def __new__(cls, name, bases, dct):
        for mthd, val in dct.items():
            if not mthd.startswith('__'):
                # replace methods with modified (timed) version
                dct[mthd] = timer(val)
        
        return super().__new__(cls, name, bases, dct)



class HPNortonApp(metaclass=Timed):
    """
    HP Norton application functionality
    """
    def get_data(self, file):
        """
        Gets data from csv file
        Returns: List, consisting of Dicts with data in each row
        """
        data = []
        with open(file, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for i, row in enumerate(reader):
                if i == 0:
                    header = row
                else:
                    data.append(dict(zip(header, row)))
        return data


    def import_data(self, product_file, customer_file, rental_file):
        """
        Creates and populates 3 collections in MongoDB database
        Inputs: path to data for: products, customers, rentals (in that order)
        Returns: Tuple, with number of entries added;
                 Tuple, with number of errors occurred
        """
        with MongoDB() as database:
            collections = ({"database": "products", "file": product_file, "records": 0, "errors": 0},
                           {"database": "customers", "file": customer_file, "records": 0, "errors": 0},
                           {"database": "rentals", "file": rental_file, "records": 0, "errors": 0})
            for collection in collections:
                try:
                    data = self.get_data(collection["file"])
                    try:
                        database[collection["database"]].insert_many(data)
                        collection["records"] = (database[collection["database"]]).count_documents({})
                    except BulkWriteError:
                        collection["errors"] += 1
                    except DuplicateKeyError:
                        collection["errors"] += 1
                except FileNotFoundError:
                    collection["errors"] += 1

            return (collections[0]["records"], collections[1]["records"], collections[2]["records"]), \
                   (collections[0]["errors"], collections[1]["errors"], collections[2]["errors"])


    def show_available_products(self):
        """
        Queries product database for available items
        Returns: Dict, with available product data
        """
        prods = {}
        with MongoDB() as database:
            for prod in database["products"].find({"qty_avail": {"$gt": "0"}}):
                prods[prod["prod_id"]] = {"desc": prod["description"], "prod_type": \
                                            prod["prod_type"], "qty_avail": \
                                            prod["qty_avail"]}
            return prods


    def show_rentals(self, product_id):
        """
        Queries rental database for customer by product ID
        Returns: Dict, user info for those who have rented product
        """
        renters = {}
        with MongoDB() as database:
            id_list = [item["user_id"] for item in database["rentals"].find({"prod_id": product_id})]
            for user_id in id_list:
                user = database["customers"].find_one({"user_id": user_id})
                renters[user_id] = {"name": user["name"], "address": user["address"], "phone": \
                                    user["phone"], "email": user["email"]}
            return renters


    def clear_collections(self):
        """
        Clears all collections in database
        """
        with MongoDB() as database:
            database["products"].drop()
            database["customers"].drop()
            database["rentals"].drop()



if __name__ == "__main__":

    r_n = (10, 100, 500, 1000, 2500, 5000)
    fdr = 'files/'
    ext = '.csv'

    for n in r_n:
        write_data(n)
        i = HPNortonApp()
        i.clear_collections()
        prod_f = fdr + 'products' + str(n) + ext
        cust_f = fdr + 'customers' + str(n) + ext
        rent_f = fdr + 'rentals' + str(n) + ext
        i.import_data(prod_f, cust_f, rent_f)
        i.show_available_products()
        i.show_rentals('prod0007')