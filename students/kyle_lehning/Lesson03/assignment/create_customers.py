#!/usr/bin/env python3
"""
Used to create database of customers, only needed once
"""
import customer_schema


def create_tables():
    """Helper function to create tables in database"""
    with customer_schema.DB:
        customer_schema.DB.create_tables([customer_schema.Customer])
    customer_schema.DB.close()


if __name__ == '__main__':
    create_tables()
