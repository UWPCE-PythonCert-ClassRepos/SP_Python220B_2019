""""
must use 127.0.0.1 on windows
pip install pymongo

"""
from pymongo import MongoClient
#import logging

class MongoDBConnection():
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

def insert_collection_one(connection, collection, dataset):
    collection = connection[collection]
    collection.insert_one(dataset)
    return collection


def insert_collection_many(connection, collection, dataset):
    collection = connection[collection]
    collection.insert_many(dataset)
    return collection

def lookup_query(collector_collection, cd_collection):
    # related data
    for name in collector_collection.find():
        print(f'List for {name["name"]}')
        query = {"name": name["name"]}
        for a_cd in cd_collection.find(query):
            print(f'{name["name"]} has collected {a_cd}')

def print_mdb_collection(collection_name):
    for doc in collection_name.find():
        print(doc)

def drop_collection(collector_collection, cd_collection):
    # start afresh next time?
    yorn = input("Drop data?")
    if yorn.upper() == 'Y':
        cd_collection.drop()
        collector_collection.drop()

def main():
    mongo = MongoDBConnection()

    with mongo:
        # mongodb database; it all starts here
        media_db = mongo.connection.media

        # collection in database
        cd_collection = insert_collection_many(media_db, 'cd', cd_ip)
        cd_collection = insert_collection_one(media_db, 'cd', cd_ip_1)
        collector_collection = insert_collection_many(media_db, 'collector', collector_ip)

    print_mdb_collection(cd_collection)

    print_mdb_collection(collector_collection)

    lookup_query(collector_collection, cd_collection)

    drop_collection(collector_collection, cd_collection)


if __name__ == "__main__":
    cd_ip_1 = {"artist": "The Who", "Title": "By Numbers"}
    cd_ip = [
        {"artist": "Deep Purple", "Title": "Made In Japan", "name": "Andy"},
        {"artist": "Led Zeppelin", "Title": "House of the Holy", "name": "Andy"},
        {"artist": "Pink Floyd", "Title": "DSOM", "name": "Andy"},
        {"artist": "Albert Hammond", "Title": "Free Electric Band", "name": "Sam"},
        {"artist": "Nilsson", "Title": "Without You", "name": "Sam"}
    ]
    collector_ip = [
        {"name": "Andy", "preference": "Rock"},
        {"name": "Sam", "preference": "Pop"}
    ]
    main()
