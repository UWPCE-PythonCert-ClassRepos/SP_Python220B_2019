# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 20:31:47 2019

@author: Laura.Fiorentino
"""


def main():
    x = 'main'
    one()


def one():
    y = 'one'
    two()


def two():
    z = 'two'
    long_loop()


def long_loop():
    for i in range(int(1e04)):
        i + 1
        if i == 777:
            raise Exception("terrible bug")
    result = 1 + 1
    return result


if __name__ == '__main__':
    print(main())
    print("last statement")
