from data_processing.data_constants import *
from data_processing.data_utils import *
import pandas as pd
from config import DATA_DIR


def get_famine_data(REGION, STARTTIME):
    print("Loading famine data")
    # Transform food data:
    food_df = pd.read_csv(DATA_DIR + 'food.csv', usecols=[0, 1, 3, 4])
    food_df = food_df[
        food_df.Region.eq(REGION) & food_df.Date.ge(STARTTIME - 1) & food_df.Item.isin(WANTEDPRODUCTS)]
    food_df['ItemID'] = food_df['Item'].apply(applyProductMap)
    trimmed_food_df = food_df[['Date', 'ItemID', 'Price']]

    # Extract FEWSNET food data
    ffood_df = pd.read_csv(DATA_DIR + 'fews_food.csv')
    ffood_df = ffood_df[
        ffood_df.date.ge(STARTTIME - 1) & ffood_df.item.isin(WANTEDFEWSFOOD) & ffood_df.region.eq(REGION)]

    # Extract conflict data
    conflict_df = pd.read_csv(DATA_DIR + "conflict.csv")
    conflict_df = conflict_df[['event_date', 'admin1', 'fatalities']].rename(columns={'admin1': 'region'})
    conflict_df['date'] = conflict_df.event_date.apply(strdate)
    trimmed_conflict_df = conflict_df[conflict_df.date.ge(STARTTIME - 1) & conflict_df.region.eq(REGION)][
        ['date', 'region', 'fatalities']]
    # trimmed_conflict_df =conflict_df

    # Extract IPC data
    ipc_df = pd.read_csv(DATA_DIR + 'ipc-5y.csv')
    trimmed_ipc_df = ipc_df[ipc_df.time.ge(STARTTIME) & ipc_df.region.eq(REGION)]

    # Extract weather data
    weather_df = pd.read_csv(DATA_DIR + 'climate-complete-noaa.csv', usecols=[0, 3, 4])
    weather_df = weather_df[weather_df['Station Name'].isin(WANTEDSTATIONS)]
    weather_df['Date'] = weather_df['Date'].apply(dateToFloat)
    weather_df = weather_df[weather_df.Date.ge(STARTTIME - 1)]
    weather_df['Station Name'] = weather_df['Station Name'].apply(applyStationMap)
    trimmed_weather_df = weather_df.rename(columns={'Station Name': 'Station', 'Mean Temperature': 'Temperature'})

    dates = sorted(list(set(trimmed_ipc_df.time.values)))

    datasets = dict()
    for date in dates:
        dataset = dict()
        features = []
        dataset['ipc'] = trimmed_ipc_df.loc[trimmed_ipc_df.time.eq(date), ['p2perc', 'p3perc', 'p4perc']].to_dict(
            'records')

        food_data = dict()
        for i in range(len(WANTEDPRODUCTS)):
            food_data[i] = trimmed_food_df[
                trimmed_food_df.Date.gt(date - 1) & trimmed_food_df.Date.le(date) & trimmed_food_df.ItemID.eq(i)][
                ['Date', 'ItemID', 'Price']]
            features.append(get_price_feature(food_data[i]))

        fews_data = dict()
        for food in WANTEDFEWSFOOD:
            food_data[food] = ffood_df[ffood_df.date.ge(date - 1) & ffood_df.date.lt(date) & ffood_df.item.eq(food)]
            features.append(get_fews_feature(food_data[food]))

        dataset['food'] = food_data

        conflict_data = trimmed_conflict_df[
            trimmed_conflict_df.date.ge(date - 1) & trimmed_conflict_df.date.lt(date)]
        features.append(np.sum(conflict_data.fatalities.values))

        dataset['conflict'] = conflict_data

        weather_data = dict()
        for i in range(len(WANTEDSTATIONS)):
            weather_data[i] = trimmed_weather_df[trimmed_weather_df.Date.gt(date - 1) & trimmed_weather_df.Date.le(
                date) & trimmed_weather_df.Station.eq(i)][['Date', 'Temperature']]
            # features['t{}'.format(i)]=get_temp_feature(weather_data[i])
            features.append(get_temp_feature(weather_data[i]))
        dataset['weather'] = weather_data
        dataset['features'] = features

        datasets[date] = dataset

    train_dates = sorted(list(datasets.keys()))[:-2]
    nFeatures = len(datasets[train_dates[0]]['features'])
    features = [datasets[date]['features'] for date in train_dates]

    print("Famine dataa loaded")
    return datasets, train_dates, nFeatures, features
