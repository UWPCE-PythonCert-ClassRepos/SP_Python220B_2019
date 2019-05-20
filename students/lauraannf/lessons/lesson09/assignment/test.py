# -*- coding: utf-8 -*-
"""
Created on Mon May 20 14:32:15 2019

@author: Laura.Fiorentino
"""

def add(a, b):
    print("Function 'add' called with args: {}, {}".format(a, b) )
    result = a + b
    print("\tResult --> {}".format(result))
    return result


def logged_func(func):
    def logged(*args, **kwargs):
        print("Function {} called".format(func.__name__))
        if args:
            print("\twith args: {}".format(args))
        if kwargs:
            print("\twith kwargs: {}".format(kwargs))
        result = func(*args, **kwargs)
        print("\t Result --> {}".format(result))
        return result
    return logged