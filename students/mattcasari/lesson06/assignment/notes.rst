============================================
Notes on improving performance for Lesson 06
============================================



Generating 1 Million Records
============================
In order to generate 1 million records with the same format as the provided file

Format:
    GUID, idx, idx+1, idx+2, idx+3, random_date,
Example:
    5df44a54-8cca-4928-bc53-caabb23cf329,1,2,3,4,05/26/2015,

To generate the GUID, use the python UUID package.  The following command 
can be used to generate a UUID.

::

    >> import uuid

    >> uuid.uuid1()

    UUID('34259ef0-528a-11ea-8d84-1065307baeb6')

  

Timing in Windows 10 - PowerShell
=================================

Commands
--------


Using Measure-Command to measure the program "file_name.py"

::

    PS> Measure-Command {start-process py .\file_name.py  -Wait}


Results
-------
Results of poor_perf.py

::

    PS> Measure-Command {start-process py .\poor_perf.py  -Wait}

Returns response

::

    Days              : 0
    Hours             : 0
    Minutes           : 0
    Seconds           : 1
    Milliseconds      : 15
    Ticks             : 10158298
    TotalDays         : 1.17572893518519E-05
    TotalHours        : 0.000282174944444444
    TotalMinutes      : 0.0169304966666667
    TotalSeconds      : 1.0158298
    TotalMilliseconds : 1015.8298


Observations in the poor_perf.py program
========================================

- File was opened twice
    a) can be reduced to single open

- year_count initialized inside csv call
    a) probably not a big deal, but try moving it up.

- remove print functions

- new_ones is unneccessary. 
    a) move new[0][6:] into ``for row in reader`` loop
    b) delete ``new_ones = []```

- if lrow[5] > '00/00/2012': is unneccessary
    a) compare year directly instead of doing > check

- lrow is redundant
    a) replace lrow with row

- Add generator for increment functions
    a) create generator
    b) complete year_count outside of loop

- Try using csv.DictReader instead of csv.reader

- Try using Pandas
    a) Use pandas.csv_reader to load Data
    b) Use pandas functions to work on data to test speed.


Tests and refactoring performed 
===============================

- Create file to test both poor and good _perf.py programs
    a) File created program_comparison.py
    b) Run tests between both programs to check Timing
        
        ``Average of 2 Runs``

        ``Poor Performance Elapsed Time = 4.72653``
        
        ``Good Performance Elapsed Time = 4.73381``
        
        ``Time deterioration of -0.00728 seconds``
        
        ``Factor of 1.0 deterioration``

    **CONCLUSION: No difference(expected)**

- Modify good_perf.py to have single csv open
    a) removed second csv open
    b) moved ``if "ao"" in row[6]`` to ``for row in reader`` loop
    c) reran test
        
        ``Average of 2 Runs``
        
        ``Poor Performance Elapsed Time = 4.73817``
        
        ``Good Performance Elapsed Time = 3.07490``
        
        ``Time improvement of 1.66327 seconds``
        
        ``Factor of 1.5 improvement``

    **CONCLUSION: Removing second csv call speeds up the program by 1.5 times**

- Move year_count initialization outside of csv call
    a) Not sure that this will do much, but..
    b) Moved year_count initialization to just below start time call
    c) reran test
        ``Average of 2 Runs``

        ``Poor Performance Elapsed Time = 4.72203``
        
        ``Good Performance Elapsed Time = 3.09786``
        
        ``Time improvement of 1.62416 seconds``
        
        ``Factor of 1.5 improvement``

    **CONCLUSION: No noticeable difference**

- Removing the ``print`` functions
    a) Data is returned anyway, print from that if needed
    b) removed the ``print`` statements
    c) reran test
        ``Average of 2 Runs``

        ``Poor Performance Elapsed Time = 4.78552``

        ``Good Performance Elapsed Time = 3.06015``

        ``Time improvement of 1.72537 seconds``

        ``Factor of 1.6 improvement``

    **CONCLUSION: More improvement achieved when not having to print**

- Removing new_ones.append and directly update year_count
    a) Delete new_ones list
    b) Replace new_ones.append() with direct update year_count check
    c) rerun test
        ``Average of 2 Runs``
    
        ``Poor Performance Elapsed Time = 5.88415``
        
        ``Good Performance Elapsed Time = 3.39963``
        
        ``Time improvement of 2.48452 seconds``
        
        ``Factor of 1.7 improvement``

    ** CONCLUSION: Performance improvement removing list**

- Remove if lrow[5] > '00/00/2012':
    a) Remove lrow[5] > '00/00/2012' since it is redundant
    b) rerun test
        ``Average of 2 Runs``
        
        ``Poor Performance Elapsed Time = 5.30039``
        
        ``Good Performance Elapsed Time = 3.12264``
        
        ``Time improvement of 2.17776 seconds``
        
        ``Factor of 1.7 improvement``

    **CONCLUSION: Minor improvement, possibly**
- Remove lrow and replace with row, since lrow is redundant
    a) Replace all instances of lrow with row.
    b) Delete lrow = list(row)
    c) rerun test
        ``Average of 2 Runs``

        ``Poor Performance Elapsed Time = 5.27644``
        
        ``Good Performance Elapsed Time = 3.14163``
        
        ``Time improvement of 2.13480 seconds``
        
        ``Factor of 1.7 improvement``
    
    **CONCLUSION: Inconclusive improvement**

- Replace year_count and found increment with generator
    a) Replace year_count["2013"] += 1 with generator 
    b) Replace found += 1 with generator
    c) rerun test

        ``Average of 2 Runs``

        ``Poor Performance Elapsed Time = 5.75993``
        
        ``Good Performance Elapsed Time = 3.23316``
        
        ``Time improvement of 2.52677 seconds``
        
        ``Factor of 1.8 improvement``
    
    **CONCLUSION: Slight improvement in performance**

- Replace csv.read with csv.DictReader 
    a) replace CSV call with csv.DictReader
    b) replace row[5] with row['date']
    c) replace row[6] with row['extra']
    d) add fieldname list to open csv.DictReader
    e) rerun tests

        ``Average of 2 Runs``
        
        ``Poor Performance Elapsed Time = 4.81238``
        
        ``Good Performance Elapsed Time = 5.92293``

        ``Time deterioration of -1.11055 seconds``

        ``Factor of 0.8 deterioration``

    **CONCLUSION: DictReader slowed the program significantly**

    **NOTE: Might be how I am accessing data that is slow**


- Replace csv.DictReader with Pandas.csv_reader
    a) Replaced csv.DictReader with Pandas.csv_reader
    b) used Pandas functions to sum/count years and found
    c) reran tests
        ``Average of 2 Runs``
        
        ``Poor Performance Elapsed Time = 7.02374``
        
        ``Good Performance Elapsed Time = 8.05161``

        ``Time deterioration of -1.02787 seconds``

        ``Factor of 0.9 deterioration``

- Reverted to previous version using csv.reader
    a) copied previous commit code (to preserve notes) rather than Reverted
    b) reran tests
        ``Average of 2 Runs``
        
        ``Poor Performance Elapsed Time = 5.13292``
        
        ``Good Performance Elapsed Time = 2.74515``
        
        ``Time improvement of 2.38777 seconds``
        
        ``Factor of 1.9 improvement``
    **CONCLUSION: Back to good performance**

- Compare against fewer characters
    a) truncate character compare from 4 to 2 char for year count
    b) rerun test
        ``Average of 2 Runs
        
        ``Poor Performance Elapsed Time = 4.76997``
        
        ``Good Performance Elapsed Time = 2.68535``
        
        ``Time improvement of 2.08462 seconds``
        
        ``Factor of 1.8 improvement``
    **CONCLUSION: Decreased performance (or about the same)**