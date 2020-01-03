#######################################
lesson06 Assignment Notes - Brian Minsk
#######################################

I am testing performance with a 1 million record (line) csv file. Units are always seconds.
timeit.timeit is used for timings.

********************
Baseline performance
********************

I added a loop with timeit timed performance in main() running the original code 10 times for a
baseline. The results in seconds:

1.	36.2779388
2.	30.1422789
3.	40.5167374
4.	34.7673633
5.	33.6967243
6.	38.4667894
7.	36.9502096
8.	42.8882439
9.	43.7322826
10.	59.4858080

* Average = 39.69243762
* Standard deviation: 8.104057992

********************
Seperate functions
********************

For the next test I seperated out the part of the analyze function that counts years from the part
that counts 'ao' and timed them separately to get a sense of what is taking more time. Note that
the data file is processed separately, just like in the original, so it is expected that the total
time should be about the same as the previous test.

*Counting years*
================

1.	12.9736609
2.	11.3037618
3.	10.839839
4.	11.634324
5.	12.3820648
6.	11.9956079
7.	10.5579572
8.	10.0768187
9.	12.6258915
10.	13.125681

* Average = 11.75156068
* Standard deviation = 1.047655538

*Counting "ao"*
===============

1.	7.6821638
2.	6.2593614
3.	5.5217592
4.	5.5565047
5.	5.3656267
6.	6.4352704
7.	5.5602476
8.	5.5452886
9.	5.2621638
10.	5.4809229

* Average = 5.86693091
* Standard deviation = 0.741705964

*Discussion*
============

Note that the total average time is 17.61849159 seconds, *less than half* of the previous average
time. **This was unexpected!** I am not sure why the time was decreased so much since all that was changed is that the
analyze function was split into two parts. The file is still being processed twice, as it was in
the original. Perhaps longer functions have some additional overhead? Seems unlikely ...

**************************************************************************
Seperate functions: time file processing versus counting in counting years
**************************************************************************

Time the file processing separately from counting the years in the new count_years function by
seperating it into two functions.

*File processing*
=================

1.	9.0295803
2.	11.1414942
3.	10.7242838
4.	9.8427781
5.	7.6808674
6.	7.1741831
7.	6.5525722
8.	7.3929855
9.	7.9902582
10.	8.8016382

* Average = 8.6330641
* Standard deviation = 1.550230267

*Counting*
==========

1.	0.001426
2.	0.0002796
3.	0.0002938
4.	0.0004062
5.	0.0002717
6.	0.0002677
7.	0.0003155
8.	0.0002331
9.	0.000255
10.	0.0002224

* Average = 0.0003971
* Standard deviation = 0.000365138

*Discussion*
============
Note that counting is only a very small fraction of the total time. Also note that the total
average time is 8.6334612, much less than the 11.75156068 average time when processing the file and
counting the years were not separated out. Again I am not sure why but this is further evidence
longer functions have more overhead. Hmm ...

*************************
Improving file processing
*************************

File processing seems to take the bulk of the time. The file is processed twice and it is obvious
this could be improved by combining into one pass of the file.

*File processing combined*
==========================

1.	12.2093062
2.	8.4217574
3.	7.7893208
4.	8.8719249
5.	7.3188556
6.	7.828767
7.	9.1239439
8.	9.7969941
9.	7.972463
10.	9.8990728

* Average = 8.92324057
* Standard deviation = 1.444145159

*Everything else*
=================

1.	0.00164
2.	0.0018976
3.	0.0002189
4.	0.000243
5.	0.0002376
6.	0.0002843
7.	0.0002225
8.	0.0002292
9.	0.0003193
10.	0.0002444

* Average = 0.00055368
* Standard deviation = 0.000644019

*Discussion*
============
The new total average time is 8.92379425, which is much less than the original average time
(39.69243762) and when file processing was still in 2 passes but seperated out into 2 functions
(17.61849159).

*********************
Small efficiencies
*********************
Since there is not a large variation of years in the data it should be more efficient to not check
if the year is 2013 or greater and just add all the dates to the data structure. Also, when
counting the years, we don't have to use a bunch of if statements for each year that we want to
count. We can just use the year string as a key into the dictionary. Also, there is not need to
collect column 0 (the UUID) from the csv file since it is never used or referenced elsewhere.


Also there is a place where column 0 - the UUID column - is getting added to a data structure but
it is never used so that is removed.

*Final timings*
================

1.	8.7201528
2.	9.6481354
3.	8.524903
4.	7.8781495
5.	6.8962293
6.	7.3864331
7.	8.0305397
8.	8.1477461
9.	9.4732293
10.	8.3713321

* Average = 8.30768503
* Standard deviation = 0.850128622

*Final discussion*
==================
Performance comparison with original code
-----------------------------------------
The final average time was 8.30768503, about 0.6 seconds faster than the version that makes 1 pass
through the data file. The final average time is about 4.8 times faster than the original code
(the original code's average run time was 39.69243762).

Note that the time deviations within each version are rather large, likely an effect of processor,
memory access, and file access load on my computer.

Discussion of changes made
--------------------------

Seperate functions (evaluation step)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Initially the code was left intact but separated into two functions, one part that read the csv
file and counted years and the other read the csv file and counted "ao". This was seperated out
only to evaluate how much each part contributed to performance. No performance change was expected
but, suprisingly, it resulted in significantly faster performance - decreasing the average time
from ~39.7 seconds to ~17.6 seconds.

Seperate functions: time file processing versus counting in counting years (evaluation step)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The function for counting years was generally left intact but separated into two functions to
separately evaluate the contribution of file processing and counting years to performance. One
function read the file and created the list data structure with 2 columns of data, one being the
date, and the other counted the years.

It was found that counting years was a very small portion of the time spent in this part of the
program.

Again, the intent of this step was only to evaluate the contribution of each part to performance
but, again also, there was an unexpected performance improvement of the 'counting years' part of
the script: from about 11.8 seconds average to 8.6 seconds average. (Note that in this step the
the 'counting ao' part of the program was not evaluated.)

Improving file processing 
^^^^^^^^^^^^^^^^^^^^^^^^^

Based on the results from the year counting part of the script, it was clear that the script spent
much more time in file processing than in any other part of the code. The original script also made
two passes in reading the csv file. Only one pass is necessary and I thought a big improvement
could be made by making one pass through the file instead. Also, since counting 'ao' consisted of
merely incrementing a counter, it seemed most efficient to not seperate that out into a separate
function.

Making one pass through the csv file resulted in a large performance improvement. The new average
time running the whole script was ~8.9 seconds, about 4.4 times faster than the original code.

Opportunities for smaller performance improvements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

I analyzed the code and found some additional places it could be improved WRT performance:
* No need to collect column 0 (the UUID) from the csv data since it is never used.
* Eliminate the conditional "if" that checks if the year is 2013 or greater for each line of the
file. Just add all the dates to the list that is used later to count the dates.
* When counting the years, there is no need to have a bunch of if statements for each year.
Instead, just take the year from the date string and use it as a key in the dictionary used for 
counting years. Later, the unwanted years - the years before 2013 - can be popped off the
dictionary.

These changes improved performance ~0.6 seconds average.

Summary of final changes
^^^^^^^^^^^^^^^^^^^^^^^^
* Created two functions, one increments a counter for 'ao' and adds the dates to a list while reading each line in the csv file, the other counts the years in the list.
* Eliminated collecting column 0 (the UUID) from the csv data.
* Eliminated the "if" statement that checks if the year is 2013 or greater. Instead counted all the years and later popped the unneeded years off the dictionary that keeps track of the year counts.
* Eliminated the "if" statements that check the year when incrementing the year counters in the dictionary. Instead, used the year from the date in the list as a key for the dictionary.






