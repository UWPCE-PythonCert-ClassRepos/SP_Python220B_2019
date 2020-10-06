""" Documentation for do_profile

This script runs cProfile on a specified file and
saves the results to profile_{filename}_MM/DD/YYYY_HH:MM:SS.txt"""

import os
import sys
import datetime
import subprocess

USAGE = """
run the script with file(s) to cProfile as command line args
>>>python do_profile.py file1.py file2.py
"""

if not len(sys.argv) > 1:
    print(USAGE)
    raise ValueError("No files to profile!")

files = sys.argv[1:]

for f in files:
    if not os.path.exists(f):
        raise FileNotFoundError(f"Not found {f} in {os.getcwd()}")

    profile_file = f"profile-{f.replace('.','_')}-{datetime.datetime.now().strftime('%m%d%Y_%H%M%S')}"
    cmd = f"python -m cProfile {f} > {profile_file}"
    print(cmd)
    print(os.getcwd())
    subprocess.call(cmd, shell = True)

