import cProfile
import re
cProfile.run('re.compile("foo|bar")','restat')

#python -m cProfile -o test.txt -s -1 cperf.py