from data_processing.data_constants import *
import datetime as dt
import numpy as np
import ruptures as rpt


def getDays(year, quarter):
        if(year % 4 ==0):
            return [_, 91, 91, 92, 92][quarter]
        else:
            return [_, 90, 91, 92, 92][quarter]

