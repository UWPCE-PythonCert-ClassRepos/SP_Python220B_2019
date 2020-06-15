coverage is below 90% target, at 89%. It's not a big deal, but I think it's a good opportunity for practicing exception coverage.
Currently, the IntegrityError trap on line 57 is not covered, 
same as the DoesNotExist trap on line 110.
Either of those (or both) would get your coverage higher than 90% and provide the change of triggering an exception
with your tests (let me know if you need help on that one, note that testing for an exception should not make your code crash).
-Luis



***
Luis, I added a check for coverage, and made the changes you suggested.
see file results_coverage.txt


Thanks
Mike
