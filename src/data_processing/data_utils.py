import numpy as np

from data_processing.data_constants import *


def getDays(year, quarter):
    if (year % 4 == 0):
        return [0, 91, 91, 92, 92][quarter]
    else:
        return [0, 90, 91, 92, 92][quarter]


def getDate(year, month, day):
    if (year % 4 == 0):
        return year + (np.cumsum(LEAPS)[month - 1] + day - 1) / 366.
    else:
        return year + (np.cumsum(MONTHS)[month - 1] + day - 1) / 365.
