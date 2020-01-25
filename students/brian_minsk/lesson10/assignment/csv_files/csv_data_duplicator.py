import csv
import os

def read_data(csv_file_name):
    """ Read each each row into a dict and return a list of all the dicts.
    """
    with open(csv_file_name, newline='', encoding='utf-8-sig') as csv_file:
        reader = csv.DictReader(csv_file)        
        return [row for row in reader]


def get_fields(csv_file_name):
    with open(csv_file_name, newline='', encoding='utf-8-sig') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            return reader.fieldnames


def create_new_file_name(csv_file_name, num_dups):
    root_ext = os.path.splitext(csv_file_name)
    return root_ext[0] + str(num_dups) + root_ext[1]


def write_new_file(data, csv_file_name, field_names, num_dups):
    with open(file=csv_file_name, mode='w', newline='', encoding='utf-8-sig') as csv_file:
        writer = csv.DictWriter(csv_file, field_names)
        writer.writeheader()
        for _ in range(num_dups):
            writer.writerows(data)


if __name__ == "__main__":
    file_names = ['customers.csv', 'product.csv', 'rentals.csv']
    num_dups = 10000

    for file_name in file_names:
        data = read_data(file_name)
        field_names = get_fields(file_name)
        new_file_name = create_new_file_name(file_name, num_dups)
        write_new_file(data, new_file_name, field_names, num_dups)

