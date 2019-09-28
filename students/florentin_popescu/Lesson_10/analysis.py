# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 09:11:49 2019
@author: Florentin Popescu
"""
# imports
import os.path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from sklearn.linear_model import LinearRegression

# pd.set_option("display.max_rows", 1000)
# pd.set_option("display.max_columns", 1000)
# ================================

try:
    if os.path.exists('timing.txt'):
        LST = []
        with open('timing.txt') as file:
            LINES = file.readlines()
            for line in LINES:
                LST.append(line.split())
            DFR = pd.DataFrame(LST,
                               columns=["f", "n",
                                        "method", "t",
                                        "load_time(ms)", "time_unit",
                                        "r", "prc", "products_loaded",
                                        "p", "customers_loaded", "cst",
                                        "rentals_loaded", "rnt"])
        DFR = DFR.drop(["f", "n", "t", "time_unit", "r",
                        "prc", "p", "cst", "rnt"], axis=1)
        # ----------------------------

        DFR["temp"] = np.where(DFR.products_loaded != "0", "import_products",
                               np.where(DFR.customers_loaded != "0",
                                        "import_customers",
                                        np.where(DFR.rentals_loaded != "0",
                                                 "import_rentals",
                                                 DFR.method)))
        DFR["method"] = np.where(((DFR["products_loaded"] != "0") &
                                  (DFR["customers_loaded"] != "0") &
                                  (DFR["rentals_loaded"] != "0")),
                                 DFR["method"], DFR["temp"])
        DFR = DFR.drop(["temp"], axis=1)
        # ----------------------------

        DFR["load_time(ms)"] = pd.to_numeric(DFR["load_time(ms)"],
                                             errors="coerce")
        DFR["products_loaded"] = pd.to_numeric(DFR["products_loaded"],
                                               errors="coerce")
        DFR["customers_loaded"] = pd.to_numeric(DFR["customers_loaded"],
                                                errors="coerce")
        DFR["rentals_loaded"] = pd.to_numeric(DFR["rentals_loaded"],
                                              errors="coerce")
        # ----------------------------

        DFR = DFR.sort_values(by=["method", "load_time(ms)"],
                              ascending=[True, True])

        DFR_PROD = DFR[["method", "products_loaded",
                        "load_time(ms)"
                        ]].loc[DFR["method"] == "import_products"]
        DFR_PROD = DFR_PROD.sort_values("products_loaded")

        DFR_CUST = DFR[["method", "customers_loaded",
                        "load_time(ms)"
                        ]].loc[DFR["method"] ==
                               "import_customers"]
        DFR_CUST = DFR_CUST.sort_values("customers_loaded")

        DFR_RENT = DFR[["method", "rentals_loaded",
                        "load_time(ms)"
                        ]].loc[DFR["method"] ==
                               "import_rentals"]
        DFR_RENT = DFR_RENT.sort_values("rentals_loaded")

        DFR_DROP_DTA = DFR[["method", "products_loaded",
                            "load_time(ms)"]].loc[DFR["method"] ==
                                                  "drop_data,"]
        DFR_DROP_DTA = DFR_DROP_DTA.sort_values("products_loaded")
        DFR_DROP_DTA = DFR_DROP_DTA.rename(columns={"products_loaded":
                                                    "products_deleted",
                                                    "load_time(ms)":
                                                    "delete_time(ms)"})

        # correlation
        CORR, _ = pearsonr(DFR_DROP_DTA.iloc[:, 1],
                           DFR_DROP_DTA.iloc[:, 2])

        # linear regression
        LRL = LinearRegression()
        AOX = DFR_DROP_DTA.iloc[:, 1].values.reshape(-1, 1)
        AOY = DFR_DROP_DTA.iloc[:, 2].values.reshape(-1, 1)
        LRL_DROP_DTA = LRL.fit(AOX, AOY)
        LRL_DROP_DTA_PRED = LRL.predict(AOX)

except FileNotFoundError:
    print("file does not exist")
# =================================

FIG = plt.figure(figsize=(13, 11))

AX1 = FIG.add_subplot(231)
HANDLES, LABELS = AX1.get_legend_handles_labels()
AX1.set_xlabel("loaded products")
AX1.set_ylabel("load time (ms)")
AX1.set_title("loading time for products", fontsize=13,
              fontweight='bold', va='top')
AX1.text(-0.2, 1.05, "Author: Florentin Popescu", transform=AX1.transAxes)

AX2 = FIG.add_subplot(232, sharey=AX1)
AX2.set_xlabel("loaded customers")
AX2.set_title("loading time for customers", fontsize=13,
              fontweight='bold', va='top')

AX3 = FIG.add_subplot(233, sharey=AX1)
AX3.set_xlabel("loaded rentals")
AX3.set_title("loading time for rentals", fontsize=13,
              fontweight='bold', va='top')

AX4 = FIG.add_subplot(212)
AX4.set_xlabel("number of products")
AX4.set_ylabel("delete_time (ms)")
AX4.set_title(f"drop time vs #products (correlation: {round(CORR, 3)})",
              fontsize=13, fontweight='bold', va='top')

AX1.plot(DFR_PROD["products_loaded"], DFR_PROD["load_time(ms)"],
         "k-", color="brown", marker="o")
AX2.plot(DFR_CUST["customers_loaded"], DFR_CUST["load_time(ms)"],
         "k--", color="blue", marker="o")
AX3.plot(DFR_RENT["rentals_loaded"], DFR_RENT["load_time(ms)"],
         "k-.", color="green", marker="o")
AX4.plot(DFR_DROP_DTA["products_deleted"], DFR_DROP_DTA["delete_time(ms)"],
         "k-.", color="black", marker="o")
AX4.plot(AOX, LRL_DROP_DTA_PRED, "k-", color="red")

plt.savefig("loading_time_performance.png", dpi=300)
