#!/usr/bin/env python3
"""
Used to create database of customers, only needed once
"""
from customer_schema import *


def create_tables():
    """Helper function to create tables in database"""
    with db:
        db.create_tables([Customer])
    db.close()


if __name__ == '__main__':
    create_tables()
