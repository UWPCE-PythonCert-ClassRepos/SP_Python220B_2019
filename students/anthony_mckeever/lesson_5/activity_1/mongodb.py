# Advanced Programming In Python - Lesson 5 Activity 1: Intro to MongoDB
# RedMine Issue - SchoolOps-15
# Code Poet: Anthony McKeever
# Start Date: 11/20/2019
# End Date: 11/20/2019

""""
must use 127.0.0.1 on windows
pip install pymongo
"""

import json
from pymongo import MongoClient


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


def print_mdb_collection(collection_name):
    """
    Print documents in a collection.

    :collection_name:   The collection to read from.
    """
    for doc in collection_name.find():
        print(doc)


def read_json_file(file_name):
    """
    Return json data from file

    :file_name:     The name of the json file.
    """
    with open(file_name, "r") as json_file:
        json_content = json.load(json_file)
        return json_content


def write_and_print_content(media_db, collection, file_name):
    """
    Write content to the collection and then print the collection's documents

    :media_db:      The Mongo DB collection for the Media Database
    :collection:    The name of the collection to write and print.
    :file_name:     The name of the json file.
    """
    media_collection = media_db[collection]

    json_content = read_json_file(file_name)
    media_collection.insert_many(json_content)

    print_mdb_collection(media_collection)

    return media_collection


def relate_data(collector_collection, cd_collection):
    """
    Demonstrate how to relate data documents to each other by printing a
    collectors' collection.

    :collector_collection:     The Collector collection.
    :cd_collection:            The CD List collection.
    """
    for name in collector_collection.find():
        print(f'List for {name["name"]}')
        query = {"name": name["name"]}
        for a_cd in cd_collection.find(query):
            print(f'{name["name"]} has collected {a_cd}')


def prompt_drop(collector_collection, cd_collection):
    """
    Prompt whether or not to drop the collections and start fresh.  If the user
    answers yes, both the collector_collection and cd_collection will be
    dropped.

    :collector_collection:     The Collector collection.
    :cd_collection:            The CD List collection.
    """
    yorn = input("Drop data?")
    if yorn.upper() == 'Y':
        cd_collection.drop()
        collector_collection.drop()


def main():
    """
    The Main Application method.
    """
    mongo = MongoDBConnection()

    with mongo:
        # mongodb database; it all starts here
        media_db = mongo.connection.media

        cd_collection = write_and_print_content(media_db, "cd", "cd_list.json")
        collector_collection = write_and_print_content(media_db,
                                                       "collector",
                                                       "collectors.json")

        relate_data(collector_collection, cd_collection)

        prompt_drop(collector_collection, cd_collection)


if __name__ == "__main__":
    main()
