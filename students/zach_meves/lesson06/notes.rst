Performance Improvement Notes
*****************************

cProfile Results for ``poor_perf.py``
=====================================

The Python script ``profile_perf.py`` uses the ``pstats``
module to format ``cProfile`` outputs.

At the command line::
    python -m cProfile -o poor_perf.out poor_perf.py
    python profile_perf.py poor_perf.out

Results in::
   1039355 function calls (1039338 primitive calls) in 5.191 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    4.704    4.704    5.078    5.078 poor_perf.py:9(analyze)
    19084    0.285    0.000    0.285    0.000 {built-in method _codecs.charmap_decode}
        1    0.108    0.108    5.186    5.186 poor_perf.py:59(main)
  1000012    0.080    0.000    0.080    0.000 {method 'append' of 'list' objects}
    19084    0.009    0.000    0.294    0.000 cp1252.py:22(decode)
       12    0.001    0.000    0.001    0.000 {built-in method nt.stat}
        2    0.001    0.000    0.001    0.000 {built-in method marshal.loads}
        2    0.000    0.000    0.000    0.000 {built-in method builtins.print}
        3    0.000    0.000    0.000    0.000 {built-in method _imp.create_builtin}
       13    0.000    0.000    0.001    0.000 {built-in method builtins.__build_class__}
        2    0.000    0.000    0.000    0.000 {built-in method io.open}
        2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:914(get_data)
        9    0.000    0.000    0.000    0.000 datetime.py:473(__new__)
        2    0.000    0.000    0.000    0.000 {method 'read' of '_io.FileIO' objects}
        8    0.000    0.000    0.001    0.000 <frozen importlib._bootstrap_external>:1356(find_spec)
        1    0.000    0.000    0.001    0.001 datetime.py:5(<module>)
      5/2    0.000    0.000    0.005    0.003 <frozen importlib._bootstrap>:978(_find_and_load)
       40    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:56(_path_join)
       40    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:58(<listcomp>)

Decoding characters and list appending stand out as the first place to look
for performance improvements, as each of them are called ~19,000 and 1 million
times, respectively. Reducing the number of list appends by restructing the
data storage method may increase the program speed. Character decoding may
be unavoidable, but the frequency of calling it may be reducible.

Code Changes
============

#. Remove or reduce list ``append`` function calls.

     
