""""
download mongodb
create the following directories for your project
data
data/db
data/logpython

must use 127.0.0.1 on windows
pip install pymongo

"""
from pymongo import MongoClient


class MongoDBConnection(object):
    """MongoDB Connection"""
    def __init__(self, host='127.0.0.1', port=27017):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def print_mdb_collection(collection_name):
    for doc in collection_name.find():
        print(doc)

def add_to_collection(collection, data):
    # Call insertion method based on type of data passed
    if type(data).__name__ == 'dict': # Single record
        collection.insert_one(data)
    elif type(data).__name__ == 'list': # Multiple records
        collection.insert_many(data)
    else:
        raise ValueError('Data type {} not supported, only list or dict.'.format(type(data).__name__))

def main():
    mongo = MongoDBConnection()

    with mongo:
        # mongodb database; it all starts here
        db = mongo.connection.media

        # collection in database
        cd = db["cd"]

        # notice how easy these are to create and that they are "schemaless"
        # that is, the Python module defines the data structure in a dict,
        # rather than the database which just stores what it is told

        cd_ip = {"artist": "The Who", "Title": "By Numbers"}
        add_to_collection(cd, cd_ip)

        cd_ip = [
            {"artist": "Deep Purple", "Title": "Made In Japan", "name": "Andy"},
            {"artist": "Led Zeppelin", "Title": "House of the Holy", "name": "Andy"},
            {"artist": "Pink Floyd", "Title": "DSOM", "name": "Andy"},
            {"artist": "Albert Hammond", "Title": "Free Electric Band", "name": "Sam"},
            {"artist": "Nilsson", "Title": "Without You", "name": "Sam"}
        ]
        add_to_collection(cd, cd_ip)

        print_mdb_collection(cd)

        # another collection
        collector = db["collector"]

        collector_ip = [
            {"name": "Andy", "preference": "Rock"},
            {"name": "Sam", "preference": "Pop"}
        ]
        add_to_collection(collector, collector_ip)

        print_mdb_collection(collector)

        # related data
        for name in collector.find():
            print(f'List for {name["name"]}')
            query = {"name": name["name"]}
            for a_cd in cd.find(query):
                print(f'{name["name"]} has collected {a_cd}')


        # start afresh next time?
        yorn = input("Drop data?")
        if yorn.upper() == 'Y':
            cd.drop()
            collector.drop()


if __name__== "__main__":
    main()
