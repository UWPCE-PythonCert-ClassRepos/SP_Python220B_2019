import cProfile
import good_perf as gp

filename = "data/exercise_million.csv"
cProfile.run('gp.analyze(filename)')
