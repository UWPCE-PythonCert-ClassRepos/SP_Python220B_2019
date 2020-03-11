"""
Module to extend the .csv files in ./data with more entries for testing purposes.
"""

import csv
import re
import random
import string


def extend(cust, prod, rent, n):
    """
    Extend customers, products, and rental CSV files by a factor of ``N``.
    :param cust: str
    :param prod: str
    :param rent: str
    :param n:
    :return: tuple
    """

    cust_f, cust_keys = _extend(cust, n)
    prod_f, prod_keys = _extend(prod, n)
    rent_f, _ = _extend(rent, n, keys=(list(cust_keys), list(prod_keys)))

    return cust_f, prod_f, rent_f


def _extend(filename, n, keys=()):
    """
    For internal use only. Extend a file.

    :param file: str
    :param n: int
    :param keys: tuple
    :return: str, set
    """

    with open(filename, 'r') as file:
        header = file.readline()
        reader = csv.reader(file)
        lines = [_ for _ in reader]

    fname = f"{filename}_{n}.csv"
    with open(fname, 'w') as file:
        file.write(header)
        for line in lines:
            file.write(','.join(line) + '\n')
        # file.writelines([','.join(x) for x in lines])
        # file.write('\n')

        if not keys:
            these_keys = set([line[0].strip() for line in lines])
        else:
            these_keys = set()
            n = n // 5

        for i in range(n):
            for line in lines:
                mod_words = line[:]

                if keys:  # Use provided users and products
                    uid = random.choice(keys[0])
                    pid = random.choice(keys[1])

                    counter = 0
                    while (uid, pid) in these_keys:
                        uid = random.choice(keys[0])
                        pid = random.choice(keys[1])
                        if counter > 100:
                            break

                    if (uid, pid) in these_keys:
                        continue

                    file.write(f"{uid}, {pid}, {random.randint(1, int(mod_words[-1].strip()) * 2)}\n")
                else:
                    mod_key = ''.join([random.choice(string.ascii_letters) for _ in range(len(mod_words[0]))])
                    while mod_key.strip() in these_keys:
                        mod_key = ''.join([random.choice(string.ascii_letters) for _ in range(len(mod_words[0]))])
                    these_keys.add(mod_key)
                    mod_words[0] = mod_key

                    for j, word in enumerate(line[1:], 1):
                        # If a phone number, randomize digits
                        if re.match(r"\d{3}-\d{3}-\d{4}", word.strip()):
                            num = f"{random.randint(0, 9999999999):09d}"
                            mod_words[j] = num[:3] + '-' + num[3:6] + '-' + num[-4:]
                        # If a number, randomize
                        elif re.fullmatch(r"\d*", word.strip()):
                            num = random.randint(1, int(word.strip()) * 2)
                            mod_words[j] = str(num)
                        else:  # Replace 1/2 of characters with random digits
                            mod_locs = [random.randint(0, len(word) - 1) for _ in range(len(word) // 2)]
                            lst = list(word)
                            for loc in mod_locs:
                                lst[loc] = random.choice(string.ascii_letters)
                            mod_words[j] = ''.join(lst)

                    file.write(','.join(mod_words) + '\n')
            # file.writelines([]) for line in lines])

    return fname, these_keys
