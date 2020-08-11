#!/usr/env/bin python
"""
How is a syntax error handled or thrown in pdb?

"""

def broken():
    print("broken syntax follows")
    x

if __name__ == "__main__":
    broken()