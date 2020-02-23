from data_processing.data_constants import *
import datetime as dt
import numpy as np
import ruptures as rpt


def strdate(s):
    date = dt.datetime.strptime(s, '%d %B %Y')
    year = date.date().year
    return year + (date.date().timetuple().tm_yday - 1) / (366 if year % 4 == 0 else 365)


def applyProductMap(s):
    return WANTEDPRODUCTS[str(s)]


def dateToFloat(d):
    year = d // 10000
    mo = (d % 10000) // 100 - 1
    day = d % 100 - 1
    if (year % 4 == 0):
        return year + (LEAPS[mo] + day) / 366
    else:
        return year + (MONTHS[mo] + day) / 365


def applyStationMap(s):
    return WANTEDSTATIONS[str(s)]


def smooth_trend(a, n):
    vals = []
    for i in range(len(a)):
        window = a[max(i - n, 0):min(i + n + 1, len(a))]
        vals.append(sum(window) / len(window))
    return np.array(vals)


def get_temp_feature(temp_df):
    if (len(temp_df) < 50):
        return 0
    else:
        temps = temp_df.Temperature.values
        dates = temp_df.Date.values
        smoothed = smooth_trend(temps, 5)
        diffed = np.diff(smoothed, 1)
        algo = rpt.Pelt(model='rbf', min_size=5).fit(diffed)
        result = algo.predict(pen=5)
        if (len(result) != 1):
            return (smoothed[result[-1]] - smoothed[result[-2]]) / (dates[result[-1]] - dates[result[-2]])
        else:
            return 0


def get_price_feature(food_df):
    prices = food_df.Price.values
    dates = food_df.Date.values
    nVals = len(dates)
    if (nVals == 0):
        return 0.
    minD = minP = 1e10
    maxD = maxP = -1e10
    for i in range(nVals):
        (minD, minP) = (dates[i], prices[i]) if prices[i] < minP else (minD, minP)
        (maxD, maxP) = (dates[i], prices[i]) if prices[i] > maxP else (maxD, maxP)
    if (maxD == minD):
        return 0.
    else:
        return (maxP - minP) / (maxD - minD)  # * (max(maxD, minD) - min(dates)) / (max(dates)-min(dates))


def get_fews_feature(food_df):
    prices = food_df.price.values
    dates = food_df.date.values
    nVals = len(dates)
    minD = minP = 1e10
    maxD = maxP = -1e10
    for i in range(nVals):
        (minD, minP) = (dates[i], prices[i]) if prices[i] < minP else (minD, minP)
        (maxD, maxP) = (dates[i], prices[i]) if prices[i] > maxP else (maxD, maxP)
    if (maxD == minD):
        return 0.
    else:
        return (maxP - minP) / (maxD - minD)  # * (max(maxD, minD) - min(dates)) / (max(dates)-min(dates))
