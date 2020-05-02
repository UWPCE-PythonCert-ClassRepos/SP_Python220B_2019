"""
Great Circle Runner
"""

from great_circle import great_circle

long_1, lat_1, long_2, lat_2 = 72.345, 34.235, -61.823, -29.835

if __name__ == "__main__":

    for i in range(1000000):
        great_circle(long_1, lat_1, long_2, lat_2)