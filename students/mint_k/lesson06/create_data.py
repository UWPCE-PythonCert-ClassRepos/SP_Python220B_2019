"""Lesson 06 assignment"""
import csv
import uuid
from random import randint, randrange, choice
from datetime import timedelta, datetime


def my_4random_int(num1, num2):
    """generate 4 random integers"""
    myrand1 = randint(num1, num2)
    myrand2 = randint(num1, num2)
    myrand3 = randint(num1, num2)
    myrand4 = randint(num1, num2)
    return myrand1, myrand2, myrand3, myrand4

def random_date():
    """
    This function will return a random datetime between two datetime
    objects.
    """
    start = datetime.strptime('1/1/2010', '%m/%d/%Y')
    end = datetime.strptime('12/30/2019', '%m/%d/%Y')
    delta = end - start
    random_day = randrange(delta.days)
    return (start + timedelta(days=random_day)).strftime('%m/%d/%Y')

def create_one_millon():
    """This function is to expand the data set to 1 million records"""
    filename = "data/exercise.csv"

    with open(filename, 'a', newline='') as csvfile:
        mywriter = csv.writer(csvfile, delimiter=',', quotechar='"')
        mylist = []
        for _ in range(1000000):
            mylist.append([uuid.uuid4(), *my_4random_int(1, 10),
                           random_date(), choice(['', 'ao'])])
        mywriter.writerows(mylist)


def main():
    """this one is main function"""
    create_one_millon()


if __name__ == "__main__":
    main()
