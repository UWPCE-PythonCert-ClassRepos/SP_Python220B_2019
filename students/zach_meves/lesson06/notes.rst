Performance Improvement Notes
*****************************

cProfile Results for Initial Code
=================================

Initially, ``good_perf.py`` is a copy of ``poor_perf.py``.

The Python script ``time_good.py``
script runs ``timeit.timeit`` on ``good_perf.main()`` 5 times
to generate average runtime results, then runs ``cProfile``
to profile the code.

At the command line::
    python time_good.py

Results in a runtime of 4.77s. From the profile output, the most time-consuming components are list appending (1 million function calls) and character decoding (~19,000 calls). Reducing the number of list appends by restructing the
data storage method may increase the program speed. Character decoding may
be unavoidable, but the frequency of calling it may be reducible.

It is also interesting that the number of list appends is equal to the 
number of records in the input data, even though the append statement is
within a conditional block. This suggests that the conditional is not
correct and is letting data through that it should not.

Code Changes
============

#. Fix conditional statement
    
    The ``poor_perf.py`` code::

        if lrow[5] > '00/00/2012':      
            new_ones.append((lrow[5], lrow[0]))

    is incorrect, since string comparison in this format will not
    filter dates. From the ``year_count`` structure, it is apparent
    that only dates in 2013 and later are desired. The new code is::

        cutoff = datetime.datetime(year=2012, month=12, day=31)
        
        ...

            if datetime.datetime.strptime(lrow[5], "%m/%d/%Y") > cutoff:
                new_ones.append((lrow[5], lrow[0]))

    This reduces the list append calls to ~666,000, but the ``datetime``
    constructor is much more expensive, resulting in a run time of 11.84s.
    These ``datetime`` calls need to be reduced or the time comparison should
    be done a different way.

#. Reduce ``datetime`` calls

    Based on a ``timeit`` study, simply comparing the string representation of
    the year is significantly faster than creating and comparing ``datetime``
    objects::

        date1 = "01/04/2012"
        date2 = "01/05/2014"

        timeit("date1[-4:] < date2[-4:]", globals=globals())   
        >> 0.16138020000000353

        timeit("datetime.strptime(date1, '%m/%d/%Y') < datetime.strptime(date2, '%m/%d/%Y')", globals=globals())
        >> 14.585801599999996

    The code can therefore be refactored to::

        cutoff = "2012"
        
        ...
        
            if lrow[5][-4:] > cutoff:
                new_ones.append((lrow[5], lrow[0]))

    The runtime is reduced to 3.89s. The list append calls have been reduced,
    and the next most-called function is character decoding.

#. Reduce character decoding

    The file is opened in read mode twice, when only once is necessary. 
    All of the code counting ``'ao'`` instances can be moved to the initial
    CSV iteration::

        cutoff = "2012"
        found = 0  # Do 'ao' checking here
        for row in reader:
            lrow = list(row)
            if lrow[5][-4:] > cutoff:
                new_ones.append((lrow[5], lrow[0]))
            if 'ao' in lrow[6]:
                found += 1 

    The runtime is reduced to an average of 2.30s, and decode function 
    calls are reduced from ~19,000 to ~9,500. The list append calls
    can likely be eliminated altogether.


#. Remove or reduce list ``append`` function calls.

    The logic used for determining the year and presence of ``'ao'``
    can be done during the CSV iteration - there is no need to 
    construct a list to then iterate over::

        cutoff = "2012"
        found = 0

        year_count = {
            "2013": 0,
            "2014": 0,
            "2015": 0,
            "2016": 0,
            "2017": 0,
            "2018": 0
        }

        for row in reader:
            year = row[5][-4:]
            if year > cutoff:
                if year == '2013':
                    year_count["2013"] += 1
                if year == '2014':
                    year_count["2014"] += 1
                if year == '2015':
                    year_count["2015"] += 1
                if year == '2016':
                    year_count["2016"] += 1
                if year == '2017':
                    year_count["2017"] += 1
                if year == '2018':
                    year_count["2017"] += 1

            if 'ao' in row[6]:
                found += 1

    This reduces the average runtime to 1.81s. The only function in the
    profile results that is called more than twice is character decoding.

#. Miscellaneous improvements

    The profile results did not point towards this, but it is 
    apparent in the source code that the sequential ``if``
    statements can be converted to ``if-else`` statements.
    Furthermore, once the code has be re-written as shown above,
    it becomes clear that there is no need to check if the year
    is beyond 2012.

    This results in an average runtime of 1.75s, a slight improvement.

    The ``if-else`` logic can actually be converted to dictionary 
    lookups::

        for row in reader:
            year = row[5][-4:]
            if year in year_count:
                year_count[year] += 1

            if 'ao' in row[6]:
                found += 1

        # Re-create the 'bug' found in poor_perf.py
        year_count['2017'] += year_count['2018']
        year_count['2018'] = 0

    The average runtime is now 1.66s.

#. C-style improvement




