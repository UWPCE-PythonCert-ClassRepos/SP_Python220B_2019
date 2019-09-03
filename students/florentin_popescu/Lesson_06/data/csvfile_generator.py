# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 13:45:05 2019
@author: Florentin Popescu
"""
# imports
import sys
import gc
import time
import uuid
import logging
from datetime import datetime as dt
import numpy as np
import pandas as pd
from memory_profiler import profile, memory_usage, LogFile
# ==================================


# set basic looging level as INFO
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.info("loger active")
# ==================================

MEM_USAGE = memory_usage(proc=-1, interval=.1, timeout=1)
FP = open("csvfile_generator_profile.log", "w+")
# ===============================


@profile(stream=FP, precision=4)
def generate_csv(rec, start_date, days, prob, out_csvfile):
    """
        generate csvfile using vectorized operations and broadcasting
    """
    data = pd.DataFrame(np.arange(0, rec), columns=["N1"])  # 0.12s
    data["N2"] = data["N1"] + 1  # 0.005s
    data["N3"] = data["N2"] + 1  # 0.005s
    data["N4"] = data["N3"] + 1  # 0.005s
    data["id"] = pd.DataFrame([uuid.uuid4() for _ in range(rec)])  # 3.14s
    data["date"] = np.random.choice(pd.to_datetime(pd.Series(
        pd.date_range(start_date, periods=days)
        )).dt.strftime("%d/%m/%Y"), rec, replace=True)  # 0.056s
    data["sos"] = np.random.choice(["ao", ""], rec, p=[prob, 1-prob])  # 0.049s
    data = data[["id", "N1", "N2", "N3", "N4", "date", "sos"]]
    return data.to_csv(out_csvfile, index=False, header=False)
# ===============================


if __name__ == "__main__":
    START = time.perf_counter()
    DMY = "%d/%m/%Y"
    DS = str(dt.strptime("31/12/2018", DMY) - dt.strptime("1/1/2013", DMY))[:4]
    generate_csv(1000000, "1/1/2013", int(DS), 0.3, "exercise.csv")
    LOGGER.info("memory usage current Python interpreter = %s", MEM_USAGE)
    LOGGER.info("run time perf counter: %s", time.perf_counter() - START)
    sys.stdout = LogFile("memory_profile_log", reportIncrementFlag=False)
    gc.collect()
