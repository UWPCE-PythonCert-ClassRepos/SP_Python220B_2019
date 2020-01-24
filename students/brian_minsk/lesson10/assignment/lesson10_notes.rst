#######################################
lesson10 Assignment Notes - Brian Minsk
#######################################

********************
What I Did
********************

Design
======

The challenge for me on this assignment was figuring out how my metaprogram would access the
total number of records a function processed, a value that, as the code was already written, was
not returned by any function. I thought about changing my original code and putting the functions
in a class, having each function set a class attribute that represents the number of records
processed and having the metaprogram access that value but it wasn't so easy figuring out how my
metaprogram would be able to refer to the object instatiated by that class (still thinking about
it and I might try to implement on my own time). I decided to leave my existing code pretty much
the way it had already been written, write a decorator that would wrap the relevant existing
functions, and modifying those functions to return a dictionary, with one of the dictionary items
representing the number of records processed, with the key 'num_docs_total'. While I did have to
modify the existing code a tiny bit my metaprogramming would not be specific to any function while
imposing the requirement that the function return a dictionary as described. The decorator wraps
the function passed to it with a timer, gets the number of records processed value returned from
the function passed to it, as well as the name of the function, and writes it a file named
"timings.txt".

Unit tests from lesson05 were adapted for the new return value formats.

Testing Design
==============

I wrote a script to duplicate my existing csv records data and write it to a new files. For testing
I used existing data, as is, files with the data duplicated 100 times, and files with the data
duplicated 10,000 times. The decorator metaprogram outputted the results to a file named
"timings.txt" as required by the assignment.

In __name__ == '__main__' the functions wrapped by the decorator (import_data,
show_available_products, and show_rentals) are called on the 3 sets of data files - the original
data, the data duplicated 100 times, and the data duplicated 10,000 times.

*******
Results
*******

The first set of runs the existing database that was already popluated was used. For the second set
of runs the database was emptied. Pasted text from timings.txt (format: function, time in seconds,
number of documents processed):

    |    import_data, 0.125, 18
    |    show_available_products, 0.71875, 50539
    |    show_rentals, 0.015625, 224
    |    import_data, 12.796875, 1800
    |    show_available_products, 0.984375, 51039
    |    show_rentals, 0.0, 424
    |    import_data, 1435.390625, 180000
    |    show_available_products, 2.171875, 101039
    |    show_rentals, 0.234375, 20424
    |    import_data, 0.171875, 18
    |    show_available_products, 0.015625, 5
    |    show_rentals, 0.015625, 4
    |    import_data, 13.140625, 1800
    |    show_available_products, 0.0, 505
    |    show_rentals, 0.0, 204
    |    import_data, 1472.109375, 180000
    |    show_available_products, 1.359375, 50505
    |    show_rentals, 0.421875, 20204

Isolating to each function:

.. csv-table:: import_data output
   :widths: 13, 10, 10, 10
   :header: "Function", "Time (secs)", "# of Documents", "Average Time (secs)"
   :file: results/import_data.csv

|

.. csv-table:: show_available_products output
   :widths: 13, 10, 10, 10
   :header: "Function", "Time (secs)", "# of Documents", "Average Time (secs)"
   :file: results/show_available_products.csv

|

.. csv-table:: show_rentals output
   :widths: 13, 10, 10, 10
   :header: "Function", "Time (secs)", "# of Documents", "Average Time (secs)"
   :file: results/show_rentals.csv

|

Note that the average time per document for import_data is fairly consistent and does not seem to
vary with the number of documents processed. Also note that the average time to process per
document in show_available_products is close to 0 for 505 records - since the data is repeated and,
thus, the same queries are repeated done, perhaps the queries are memoized for a relatively small
number of queries (?). The show_rentals function, which also involves many repeated queries, shows a similar
pattern in its timing output. When show_rentals only processed 4 records the average time was
relatively high - perhaps it takes some extra time to complete the first query and that extra time
contributes a lot to the average and is contribution is minimized when it is just one query of
many (?).