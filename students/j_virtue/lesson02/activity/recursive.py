# Jason Virtue -- Lesson 2 Assignment 1 
# Python Advanced UW Course
# 02/06/2020

#Reason for recursive loop is no exit logic
#If n does not equal 2 it keeps looping thru program
#return function my_fun(n/2) will keep getting smaller and go to infinity
#N will only equal 2 if it is a power of 2
#Otherwise the my_fun(n/2) will keep dividing forever
#Fix is to add exit logic if n does not equal 2

#Below is my debugging log:

import sys
 
def my_fun(n):
    if n == 2:
        return True
    if n < 1:
        return print("N is not a Power of 2")
    return my_fun(n/2)

if __name__ == '__main__':
    n = int(sys.argv[1])
    print(my_fun(n))
