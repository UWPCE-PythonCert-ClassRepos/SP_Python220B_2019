# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 9:08:01 2019
@author: Florentin Popescu
"""
# imports
import pandas as pd
# ============================

DFR = pd.DataFrame(columns=["item_code",
                            "item_description",
                            "item_monthly_price"])
DFR = DFR.append({"item_code": "LR04",
                  "item_description": "Leather Sofa",
                  "item_monthly_price": 25}, ignore_index=True)
DFR = DFR.append({"item_code": "KT78",
                  "item_description": "Kitchen Table",
                  "item_monthly_price": 10}, ignore_index=True)
DFR = DFR.append({"item_code": "BR02",
                  "item_description": "Queen Mattress",
                  "item_monthly_price": 17}, ignore_index=True)
DFR.to_csv("test_items.csv", index=False, header=False)
