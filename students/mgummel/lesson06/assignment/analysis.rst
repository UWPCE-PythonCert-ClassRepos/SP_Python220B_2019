Just after quick skim, I noticed three things right away:
1.	The local variable on line 50 is unused
2.	The for loop has a ton of conditions to check every time it runs
3.	Seems as if there’s unnecessary for loops
Then I ran Cprofile on the poor proof for a benchmark test
Cprofile first test:
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    4.471    4.471    4.566    4.566 good_perf.py:9(analyze)
  1000012    0.064    0.000    0.064    0.000 {method 'append' of 'list' objects}
        1    0.048    0.048    4.613    4.613 good_perf.py:59(main)
    19182    0.018    0.000    0.018    0.000 {built-in method _codecs.utf_8_decode}
    19182    0.012    0.000    0.030    0.000 codecs.py:319(decode)
        3    0.003    0.001    0.003    0.001 {built-in method _imp.create_dynamic}
        2    0.002    0.001    0.002    0.001 {method 'read' of '_io.FileIO' objects}
        2    0.001    0.000    0.001    0.000 {built-in method marshal.loads}
       29    0.000    0.000    0.000    0.000 {built-in method posix.stat}
        5    0.000    0.000    0.000    0.000 {built-in method posix.getcwd}
       13    0.000    0.000    0.000    0.000 {built-in method builtins.__build_class__}
        2    0.000    0.000    0.000    0.000 {built-in method io.open}
       22    0.000    0.000    0.001    0.000 <frozen importlib._bootstrap_external>:1356(find_spec)
        2    0.000    0.000    0.002    0.001 <frozen importlib._bootstrap_external>:914(get_data)
       12    0.000    0.000    0.000    0.000 datetime.py:473(__new__)
      100    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:56(_path_join)
        1    0.000    0.000    0.003    0.003 datetime.py:5(<module>)
        2    0.000    0.000    0.000    0.000 {built-in method builtins.print}
      100    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:58(<listcomp>)
        5    0.000    0.000    0.001    0.000 <frozen importlib._bootstrap_external>:1240(_get_spec)
      111    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:222(_verbose_message)
        5    0.000    0.000    0.001    0.000 <frozen importlib._bootstrap>:882(_find_spec)
      104    0.000    0.000    0.000    0.000 {method 'join' of 'str' objects}
       12    0.000    0.000    0.000    0.000 {built-in method builtins.round}
        5    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:157(_get_module_lock)
      227    0.000    0.000    0.000    0.000 {built-in method builtins.isinstance}

After seeing this it looks like there’s a ton of calls to append objects. It’s doing about a
million calls with the time per call .064, so that will add up quick. Then I notice there’s
a lot of encoding and decoding going on, which I think is due to the file being opened twice.

Plan of action:
	Remove unnecessary variables
	Reduce to 1 for loop
	Reduce number of conditional checks

After making these changes, I ran the cprofile on my code again. And see the results:
(assignment) ➜  assignment git:(master) ✗ python -m cProfile -s tottime good_perf.py
{'2013': 99955, '2014': 100080, '2015': 99872, '2016': 100517, '2017': 199743, '2018': 0}
'ao' was found 500973 times
         21003 function calls (20986 primitive calls) in 1.814 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    1.795    1.795    1.810    1.810 good_perf.py:9(analyze)
     9591    0.009    0.000    0.009    0.000 {built-in method _codecs.utf_8_decode}
     9591    0.006    0.000    0.014    0.000 codecs.py:319(decode)
        3    0.001    0.000    0.001    0.000 {built-in method _imp.create_dynamic}
        2    0.001    0.000    0.001    0.000 {built-in method marshal.loads}
       29    0.000    0.000    0.000    0.000 {built-in method posix.stat}
        5    0.000    0.000    0.000    0.000 {built-in method posix.getcwd}
       13    0.000    0.000    0.000    0.000 {built-in method builtins.__build_class__}

Half as many decoding calls(due to opening the file once) and no append calls.
The total time was reduced from 4.471 -> 1.8. Also,  the old code had 1040191 function calls
and good performing code was reduced to 21004 function calls.
This is about a pretty extraordinary increase in performance.
No crazy amount of calls (except for the decoding, which, there’s not much we can do about),
total time is down. So overall the code seems to be much more efficient.
