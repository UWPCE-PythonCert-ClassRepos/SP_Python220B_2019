#######################################
lesson07 Assignment Notes - Brian Minsk
#######################################

********************
Code logic
********************

There are 4 modules, 1 with no parallelism implemented and 3 with parallelism:

1. linear.py
2. parallel_db_writes.py
3. parallel_file_processing.py
4. parallel_file_processing_db_writes.py

linear.py
=========

linear.py simplifies the code from lesson05 to only import data from the product & customer csv
files and write the imported data to the Mongo database. There are two passes: one with the product
csv file, another with the customer csv file. During each pass one line of the file in read into a
dictionary, then the resulting document is written into Mongo. This process repeats on the next
line, and so on, until the file is completed and proceeds with the same process on the next file.
The product file import and the customer file import are completely independent processes. Also,
other than iterating through the same file, each line read is independent from all others, as are
database writes.

- product file import data: 
    - process first document
        - read line from csv file
        - write to Mongo
    - process next document
        - read line from csv file
        - write to Mongo
    - ...
- customer file import data: 
    - process first document
        - read line from csv file
        - write to Mongo
    - process next document
        - read line from csv file
        - write to Mongo
    - ...

parallel_db_writes.py
=====================

parallel_db_writes.py uses the same logic but uses threading.Thread to thread the writes to Mongo.
Presumably, the code that processes each document does not have to wait for the database writes to
in order to continue, especially since the database writes' return values are not used.

parallel_file_processing.py
===========================

parallel_file_processing.py uses the same logic as linear. py but uses theading.Thread to thread
the complete processing of each file is threaded so they run in parallel. linear.py returned a
document count and, instead, parallel_file_processing.py places the document count into a
queue.Queue, later retrieved by the calling function. Note that each file is processed
independently of the other and their documents are added to separate collections. Also note that, 
unlike parallel_db_writes.py, database writes are *not* threaded. There is no additional threading
within a thread.

parallel_file_processing_db_writes.py
=====================================

Using threading.Thread,parallel_file_processing_db_writes.py implements a thread for processing of
each file and, within each file, the database writes are threaded.

**********
Evaluation
**********

Timing methodology
==================

Each file import was timed seperately using time.process_time. The whole process was timed 1000
times for each version of the code and the averages are reported below.

Timing results
==============

+----------------------------------------+----------------------+-----------------------+---------------------+
| Version                                | products             | customers             | Total               |
+========================================+======================+=======================+=====================+
| linear.py                              | 0.031375             | 0.020219              | 0.051594            |
+----------------------------------------+----------------------+-----------------------+---------------------+
| parallel_db_writes.py                  | 0.037094 (+1.182x)   | 0.025000 (+1.236x)    | 0.062094 (+1.204x)  |
+----------------------------------------+----------------------+-----------------------+---------------------+
| parallel_file_processing.py            | 0.000672 (-46.698x)  | 0.002656 (-7.612x)    | 0.003328 (-15.502x) |
+----------------------------------------+----------------------+-----------------------+---------------------+
| parallel_file_processing_db_writes.py  | 0.000516 (-60.848x)  | 0.001734 (-11.658x)   | 0.002250 (-22.931x) |
+----------------------------------------+----------------------+-----------------------+---------------------+

Each number without parens is the average number of seconds. Each number in parens is a comparison
with linear.py - 'times' slower or faster - with '+' being slower and '-' being faster.

Discussion
==========

* The version that only has writes to the database threaded is actually a little slower.
* The version that has the whole file processing (file reads and database writes) in a single thread is a lot faster.
* Very suprisingly, the version that has the whole file processing in a thread *and* the database writes in a separate sub-thread is the fastest.

We learned that in CPython CPU-bound threads tend to slow down performance while Resource-bound
threads tend to speed up performance. I would have to investigate MongoDB's architecture to
understand why there is a slow down when only the database writes are threaded. File reading is
very resource-bound and threading probably minimizes the wait until the GIL allows the files to be
read. It is difficult to explain why the more complex threading that also includes threading
the database writes is the fastest. Perhaps including the file processing in a thread slows down
the rate of writing documents a bit, hitting more of a 'sweet spot' with MongoDB's document writing
mechanism, but, again, it is hard to explain without understanding MongoDB's archetecture -
PyMongo's architecture might also be involved as well.

The overall ~23x performance gain is good but it might be worth trying multiprocessing too to see
what happens, especially given the complex behavior observed.

I believe it is very unlikely there would be a contention with any of these threads since they are
very independent on each other, not relying on the results of one as input for another.
