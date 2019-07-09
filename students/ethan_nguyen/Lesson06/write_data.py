import csv
import uuid
import time
from random import randint
from datetime import datetime

def write_file():
    
    filename = "data/exercise_file.csv"

    with open(filename, mode='w', newline='') as exercise_file:
        employee_writer = csv.writer(exercise_file, delimiter=',', quotechar='"')

        for i in range(1, 1000000, 1):
            d = randint(100000, int(time.time()))
            try:
                employee_writer.writerow([str(uuid.uuid4()), randint(0, 99), randint(0, 99), randint(0, 99),
                                    randint(0,99), datetime.fromtimestamp(d).strftime('%m/%d/%Y'),
                                    "ao" if randint(0,99) > 50 else ""])
            except Exception as ex:
                print(ex)
                pass

if __name__ == "__main__":
    write_file()
