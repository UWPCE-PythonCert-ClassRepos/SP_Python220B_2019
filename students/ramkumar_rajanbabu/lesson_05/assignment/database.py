"""Module for database"""

import csv
import logging
from pymongo import MongoClient


class MongoDBConnection():
    """Code from part 5"""
    def __init__(self, host='127.0.0.1', port=27017):
        """"""
        self.host = host
        self.port = port
        self.connection = None
    
    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
    
def main():
    pass

if __name__ == "__main__":
    pass