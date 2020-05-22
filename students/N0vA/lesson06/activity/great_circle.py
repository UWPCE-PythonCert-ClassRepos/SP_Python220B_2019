"""
Great Circle Module
"""

import math

def great_circle(long_1, lat_1, long_2, lat_2):

    radius = 3956 # miles
    x = math.pi / 180.0
    a = (90.0 - lat_1) * (x)
    b = (90.0 - lat_2) * (x)

    theta = (long_2 - long_1) * (x)
    c = math.acos((math.cos(a) * math.cos(b)) + (math.sin(a) * math.sin(b) * math.cos(theta)))

    return radius * c

    
