
Notes updates for performance:

. initial (poor_perf) was approx 7.48sec execution time for 1M rows
. improved (good_perf) was approx 2.96sec execution time for 1M rows
. measured with timeit lib
. updated analyze function
. compressed iteration handling to single for loop
. compressed fileio to single reader
. removed lrow list creation


