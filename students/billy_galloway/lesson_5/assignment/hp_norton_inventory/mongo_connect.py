'''
Mongo DB connection
'''
from pymongo import MongoClient

class MongoDBConnection():
    ''' mongodb connection '''

    def __init__(self, host='127.0.0.1', port=27017):
        ''' initialize host and port '''
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        ''' start connection '''
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        ''' close connection when finished '''
        self.connection.close()
