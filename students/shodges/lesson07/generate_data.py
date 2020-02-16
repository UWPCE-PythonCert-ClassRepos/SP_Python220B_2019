"""
Functionality to generate additional test data.
"""

import csv
import random

def generate_data(filename, target_count, data_type):
    """
    Generate additional random data in filename.  target_count provides a declarative end-state
    for the count of records in the CSV.  data_type should be either: customers, products, or
    rentals.
    """
    with open(filename, 'r') as csvfile:
        # Evaluate whether the data file has a newline at the end of the file
        # Also get the current length so we know how many new lines to add
        dataset_asis = csvfile.readlines()
        current_count = len(dataset_asis) - 1 # subtract 1 for the header
        add_newline = not bool(dataset_asis[-1][-1] == '\n')

    with open(filename, 'a') as csvfile:
        if add_newline is True:
            # If there's no newline at the end, add one
            csvfile.write('\n')

        writer = csv.writer(csvfile, delimiter=',', quotechar='"')

        if data_type == 'customers':
            first_names = ['Alan', 'Beverly', 'Christopher', 'David', 'Elizabeth', 'Fred',
                           'Ginny', 'Harold', 'Ines', 'Jessica', 'Katie', 'Liam', 'Michael',
                           'Natalie', 'Philippa', 'Quincy', 'Sean', 'Tywin', 'William']
            last_names = ['Anderson', 'Borman', 'Cunningham', 'Dillinger', 'Ellington',
                          'Fitzgerald', 'Gutenberg', 'Hindenberg', 'Isaacson', 'King',
                          'Livingston', 'Michaelson', 'Nelson', 'Sutherland', 'Thompson',
                          'Wilson']
            street_names = ['Aardvark Ln', 'Birch St', 'Columbus Cir', 'Dragon Ave', 'Euclid Wy',
                            'First St', 'Gold Rd', 'Hacienda Ter', 'Island Dr', 'Jones Rd',
                            'King Pkwy', 'London Ave', 'Main St', 'North Pkwy', 'Oldtown Rd',
                            'Port St', 'Queen Ave', 'Royale Wy', 'South St', 'Thomas St',
                            'Union St', 'Valkyrie Wy', 'West St', 'Xanadu St', 'Yesler Wy',
                            'Zzyzx Rd']
            email_domain = ['aul.com', 'bong.com', 'cmm.com', 'dmail.com', 'exfeedia.com',
                            'facefolder.com', 'goggle.com', 'homemail.com', 'indiewentwent.com',
                            'jimmyjanes.com', 'koldaid.com', 'levos.com', 'munster.com',
                            'napple.com', 'oreoz.com', 'pinternet.com', 'quorum.com']

            rows = [['cust_' + str(i),
                     fn:=random.choice(first_names) + " " +
                     ln:=random.choice(last_names),
                     str(random.randint(1,99999)) + ' ' + random.choice(street_names),
                     random.randint(1000000000,9999999999),
                     fn.lower() + "." + ln.lower() + "@" + random.choice(email_domain)]
                    for i in range(current_count + 1, target_count + 1)]
            # Add lines in the same format
            writer.writerows(rows)

if __name__ == "__main__":
    generate_data('data/exercise.csv', 1000000)
