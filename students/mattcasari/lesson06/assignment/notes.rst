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

- 


Tests and refactoring performed 
===============================

- Create file to test both poor and good _perf.py programs
    a) File created program_comparison.py
    b) Run tests between both programs to check Timing
        
        ``Poor Performance Elapsed Time = 0.006908754000000128``

        ``Good Performance Elapsed Time = 0.006858526000000031``

- Modify good_perf.py to have single csv open



