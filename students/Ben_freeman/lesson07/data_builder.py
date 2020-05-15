import csv
import pandas as pd
import multiprocessing

def data_adder(file, n):
    with open(f'./Data/data_files_n={n}/{file}.csv', "w+", newline="") as f:
        original_data = pd.read_csv(f"./Data/data_files_n={int(n/10)}/{file}.csv")
        original_data_list = []
        updated_data = []
        i = 0
        for row in original_data.to_dict("records"):
           original_data_list.append(list(row.values()))
        for i in range(0, 10):
            updated_data = updated_data + original_data_list
            i += 1
        writer = csv.writer(f, delimiter=",")
        for row in updated_data:
            writer.writerow(row)

if __name__ == '__main__':
 listy=[40,400,4000,40000,400000]
 listerino =["customers","rentals","products"]
 for number in listy:
     for item in listerino:
         process = multiprocessing.Process(target=data_adder,
                                             args=(item,number))
         process.start()
         process.join()