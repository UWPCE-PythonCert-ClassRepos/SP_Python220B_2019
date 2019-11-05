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
        poor_perf_stats = pstats.Stats('poor_perf.log', stream=fl)
        good_perf_stats = pstats.Stats('good_perf.log', stream=fl)

        poor_perf_stats.sort_stats('cumtime')

        fl.write('--------------------------------------------\n')
        fl.write('POOR PERFORMANCE STATS\n')
        fl.write(f"Time: {poor_perf_stats.total_tt}\n")
        fl.write(f"Function Calls: {poor_perf_stats.total_calls}\n")
        fl.write(f"Top cumulative times\n")
        poor_perf_stats.print_stats(20)

        fl.write('--------------------------------------------\n')
        fl.write('GOOD PERFORMANCE STATS\n')
        fl.write(f"Time: {good_perf_stats.total_tt}\n")
        fl.write(f"Function Calls: {good_perf_stats.total_calls}\n")
        fl.write(f"Top 20 cumulative times\n")
        good_perf_stats.print_stats(20)


if __name__ == "__main__":
    """run main"""
    main('output_file.txt')
