"""
PyPy video
"""
import math
import time

reps = 1000000000

init = time.process_time()

for i in range(reps):
    value = math.sqrt(i * math.fabs(math.sin(i - math.cos(1))))

print("No function: %s" % (time.process_time() - init)) 

def calcMath(i):
    return math.sqrt(i * math.fabs(math.sin(i - math.cos(1))))

for i in range(reps):
    value = calcMath(i)

print("Function: %s" % (time.process_time() - init))

