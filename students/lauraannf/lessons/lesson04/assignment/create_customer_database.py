# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 16:17:54 2019

@author: Laura.Fiorentino
"""

from customer_model import *


DATABASE.create_tables([Customer])
DATABASE.close()
