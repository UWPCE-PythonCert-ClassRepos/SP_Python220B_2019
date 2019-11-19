"""
    Compare the poorly and better performing codes.

"""

import logging
import pstats

# Setup logging
FILE_LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"

# Console logging setup
CONSOLE_LOG_FORMAT = "%(filename)s:%(lineno)-4d %(message)s"
CONSOLE_FORMATTER = logging.Formatter(CONSOLE_LOG_FORMAT)
CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setLevel(logging.DEBUG)
CONSOLE_HANDLER.setFormatter(CONSOLE_FORMATTER)

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(CONSOLE_HANDLER)


def main(output_file):
    """Import and compare both files"""
    with open(output_file, 'w+') as fl:
        lin_perf_stats = pstats.Stats('linear.log', stream=fl)
        para_async_perf_stats = pstats.Stats('parallel_async.log', stream=fl)
        para_threading_perf_stats = pstats.Stats('parallel_threading.log', stream=fl)

        lin_perf_stats.sort_stats('cumtime')
        para_async_perf_stats.sort_stats('cumtime')
        para_threading_perf_stats.sort_stats('cumtime')

        fl.write('--------------------------------------------\n')
        fl.write('LINEAR PERFORMANCE STATS\n')
        fl.write(f"Time: {lin_perf_stats.total_tt}\n")
        fl.write(f"Function Calls: {lin_perf_stats.total_calls}\n")
        fl.write(f"Top 30 cumulative times\n")
        lin_perf_stats.print_stats(30)

        fl.write('--------------------------------------------\n')
        fl.write('PARALLEL Async PERFORMANCE STATS\n')
        fl.write(f"Time: {para_async_perf_stats.total_tt}\n")
        fl.write(f"Function Calls: {para_async_perf_stats.total_calls}\n")
        fl.write(f"Top 30 cumulative times\n")
        para_async_perf_stats.print_stats(30)

        fl.write('--------------------------------------------\n')
        fl.write('PARALLEL Threading PERFORMANCE STATS\n')
        fl.write(f"Time: {para_threading_perf_stats.total_tt}\n")
        fl.write(f"Function Calls: {para_threading_perf_stats.total_calls}\n")
        fl.write(f"Top 30 cumulative times\n")
        para_threading_perf_stats.print_stats(30)


if __name__ == "__main__":
    """run main"""
    main('findings.txt')
