import cProfile, pstats, io
pr = cProfile.Profile()
pr.enable()
def f(x):
    return x**2
def g(x):
    return x**4
def h(x):
    return x**8
pr.disable()
s = io.StringIO()
sortby = 'cumulative'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print(s.getvalue())