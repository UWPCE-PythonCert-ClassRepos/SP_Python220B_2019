Assignment:

In this lesson’s assignment, we are going to apply techniques to identify the right way to find bottlenecks in modules. We will use an evidence based approach to implement the right improvements.
Here is what you need to do:

    The assignment repository for this lesson contains a file with 10 records and a module that reads that file.

    Your first task is to take the data file, and expand it (following the format for the 10 records) so that it contains one million records. Write some Python code to do this. One of the columns is a guid (a unique identity). See if you can find an easy way to generate these (look online?).

    The module that reads the file is badly written and probably can be made to run more quickly and efficiently!

    You will look at the code and may immediately form a judgment about where performance can be improved. Do not be tempted to make immediate changes!

    Be sure to use an evidence based approach, and show, with data, how you were able to make improvements.

    Rewrite the module to improve performance. Provide evidence to demonstrate the improvement.

    Your new module should be called good_perf.py, it should use identical input and produce identical output to poor_perf.py

Other requirements:

As always, you should ensure your code produces no errors or warnings from pylint.
Submission

You submission should include the good_perf.py file, along with notes on your findings, performance improvements, and notes on your approach. For notes, you can use regular text format (.txt) or try restructured text (.rst) format. It should also include the program you write to generate 1 million records.

Measurement:

*********************
poor_perf.py under cProfile (cProfile.run('main()', sort='time'))

         1032554 function calls in 4.675 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    4.481    4.481    4.579    4.579 <ipython-input-3-aceea14eec14>:12(analyze)
        1    0.095    0.095    4.675    4.675 <ipython-input-3-aceea14eec14>:62(main)
  1000000    0.066    0.000    0.066    0.000 {method 'append' of 'list' objects}
    16256    0.019    0.000    0.019    0.000 {built-in method _codecs.utf_8_decode}
    16256    0.013    0.000    0.032    0.000 codecs.py:319(decode)
        2    0.000    0.000    0.000    0.000 {built-in method io.open}
        2    0.000    0.000    0.000    0.000 {built-in method builtins.print}
        1    0.000    0.000    4.675    4.675 {built-in method builtins.exec}
        2    0.000    0.000    0.000    0.000 {built-in method now}
        2    0.000    0.000    0.000    0.000 {built-in method _csv.reader}
        2    0.000    0.000    0.000    0.000 _bootlocale.py:33(getpreferredencoding)
        2    0.000    0.000    0.000    0.000 {built-in method _locale.nl_langinfo}
        2    0.000    0.000    0.000    0.000 codecs.py:309(__init__)
       21    0.000    0.000    0.000    0.000 future.py:47(__del__)
        1    0.000    0.000    4.675    4.675 <string>:1(<module>)
        2    0.000    0.000    0.000    0.000 codecs.py:260(__init__)
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}


*********************
good_perf.py under cProfile (cProfile('main()', sort='time'))

         16284 function calls in 1.896 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    1.880    1.880    1.896    1.896 <ipython-input-3-b4f152c5af68>:13(analyze)
     8128    0.009    0.000    0.009    0.000 {built-in method _codecs.utf_8_decode}
     8128    0.007    0.000    0.016    0.000 codecs.py:319(decode)
        1    0.000    0.000    0.000    0.000 {built-in method io.open}
        2    0.000    0.000    0.000    0.000 {built-in method builtins.print}
        2    0.000    0.000    0.000    0.000 {built-in method now}
        1    0.000    0.000    1.896    1.896 {built-in method builtins.exec}
        1    0.000    0.000    1.896    1.896 <ipython-input-3-b4f152c5af68>:36(main)
        1    0.000    0.000    0.000    0.000 {built-in method builtins.sorted}
        1    0.000    0.000    0.000    0.000 _bootlocale.py:33(getpreferredencoding)
        1    0.000    0.000    0.000    0.000 {built-in method _csv.reader}
        1    0.000    0.000    0.000    0.000 {built-in method _locale.nl_langinfo}
        1    0.000    0.000    0.000    0.000 codecs.py:309(__init__)
       11    0.000    0.000    0.000    0.000 <ipython-input-3-b4f152c5af68>:30(<lambda>)
        1    0.000    0.000    0.000    0.000 {method 'items' of 'dict' objects}
        1    0.000    0.000    0.000    0.000 codecs.py:260(__init__)
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
        1    0.000    0.000    1.896    1.896 <string>:1(<module>)


*********************
poor_perf.py under memory_profiler (python3 -m memory_profiler poor_perf.py)

Filename: poor_perf.py

Line #    Mem usage    Increment   Line Contents
================================================
    11   51.789 MiB   51.789 MiB   @profile
    12                             def analyze(filename):
    13   51.797 MiB    0.008 MiB       start = datetime.datetime.now()
    14   51.797 MiB    0.000 MiB       with open(filename) as csvfile:
    15   51.797 MiB    0.000 MiB           reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    16   51.797 MiB    0.000 MiB           new_ones = []
    17  270.336 MiB    0.031 MiB           for row in reader:
    18  270.336 MiB    0.004 MiB               lrow = list(row)
    19  270.336 MiB    0.004 MiB               if lrow[5] > '00/00/2012':
    20  270.336 MiB    1.762 MiB                   new_ones.append((lrow[5], lrow[0]))
    21
    22                                     year_count = {
    23  270.336 MiB    0.000 MiB               "2013": 0,
    24  270.336 MiB    0.000 MiB               "2014": 0,
    25  270.336 MiB    0.000 MiB               "2015": 0,
    26  270.336 MiB    0.000 MiB               "2016": 0,
    27  270.336 MiB    0.000 MiB               "2017": 0,
    28  270.336 MiB    0.000 MiB               "2018": 0
    29                                     }
    30
    31  277.707 MiB    0.004 MiB           for new in new_ones:
    32  277.707 MiB    0.000 MiB               if new[0][6:] == '2013':
    33  277.707 MiB    0.000 MiB                   year_count["2013"] += 1
    34  277.707 MiB    0.000 MiB               if new[0][6:] == '2014':
    35  277.707 MiB    0.000 MiB                   year_count["2014"] += 1
    36  277.707 MiB    0.000 MiB               if new[0][6:] == '2015':
    37  277.707 MiB    0.000 MiB                   year_count["2015"] += 1
    38  277.707 MiB    0.000 MiB               if new[0][6:] == '2016':
    39  277.707 MiB    0.000 MiB                   year_count["2016"] += 1
    40  277.707 MiB    0.000 MiB               if new[0][6:] == '2017':
    41  277.707 MiB    0.000 MiB                   year_count["2017"] += 1
    42  277.707 MiB    0.000 MiB               if new[0][6:] == '2018':
    43  277.707 MiB    0.000 MiB                   year_count["2017"] += 1
    44
    45  277.711 MiB    0.004 MiB           print(year_count)
    46
    47  277.711 MiB    0.000 MiB       with open(filename) as csvfile:
    48  277.711 MiB    0.000 MiB           reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    49
    50  277.711 MiB    0.000 MiB           found = 0
    51
    52  277.730 MiB    0.012 MiB           for line in reader:
    53  277.730 MiB    0.000 MiB               lrow = list(line)
    54  277.730 MiB    0.000 MiB               if "ao" in line[6]:
    55  277.730 MiB    0.000 MiB                   found += 1
    56
    57  277.730 MiB    0.000 MiB           print(f"'ao' was found {found} times")
    58  277.730 MiB    0.000 MiB           end = datetime.datetime.now()
    59
    60  277.730 MiB    0.000 MiB       return (start, end, year_count, found)


    **************************
    good_perf.py under memory_profiler (python3 -m memory_profiler good_perf.py)

    Filename: good_perf.py

Line #    Mem usage    Increment   Line Contents
================================================
    11   51.781 MiB   51.781 MiB   @profile
    12                             def analyze(filename):
    13   51.789 MiB    0.008 MiB       start = datetime.datetime.now()
    14   51.789 MiB    0.000 MiB       with open(filename) as csvfile:
    15   51.789 MiB    0.000 MiB           found = 0
    16   51.789 MiB    0.000 MiB           reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    17   51.789 MiB    0.000 MiB           year_count = {}
    18   52.090 MiB    0.035 MiB           for row in reader:
    19   52.090 MiB    0.000 MiB               if row[5] > '00/00/2012':
    20   52.090 MiB    0.000 MiB                   try:
    21   52.090 MiB    0.000 MiB                       year_count[row[5][6:]] += 1
    22   51.891 MiB    0.000 MiB                   except KeyError:
    23   51.891 MiB    0.000 MiB                       year_count[row[5][6:]] = 1
    24
    25   52.090 MiB    0.000 MiB               if "ao" in row[6]:
    26   52.090 MiB    0.000 MiB                   found += 1
    27
    28   52.090 MiB    0.000 MiB           print(dict(OrderedDict(sorted(year_count.items(),
    29   52.094 MiB    0.004 MiB                                  key=lambda t: t[0]))))
    30   52.094 MiB    0.000 MiB           print(f"'ao' was found {found} times")
    31
    32   52.094 MiB    0.000 MiB       end = datetime.datetime.now()
    33   52.094 MiB    0.000 MiB       return (start, end, year_count, found)


Notes:

- Noticed that there were duplicate loops so I was able to move the processing into a single loop.
- Changed the year_count dictionary from one that is statically defined to one that is dynamic
  and can capture all years in the file as long as they are greater than the minimum defined in the code.
- Refactored the use of the csv file reader such that we only had to use it in one block of code
- Removed unecessary use of list(). The collection was already iterable.  This simplified some logic a bit.
- Removed unecessary list new_ones = [] as this collection could be simply bypassed in favor of interacting directly with the years_count dictionary
- Converted years_count unsorted dict to ordereddict and back for better output formatting.


Summary:

- 64x reduction in the number of call as measured by cProfile
- 41% reduction in execution time as measured by cProfile
- 5x reduction in memory consumption as measured by memory_profiler
- nearly 50% reduction in code lines in the file
