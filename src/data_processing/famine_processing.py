from data_processing.data_constants import *
from data_processing.data_utils import *
import pandas as pd
from config import DATA_DIR

def load_data(regions):

    print("Loading data for all regions")

    data_by_region = dict()

    for region in regions:
        data_by_region[region] = get_famine_data(region)

    return data_by_region



def calculate_datasets(regions, data_by_region):

    datasets_by_region = dict()

    for region in regions:

        if data_by_region[region] is None:
            print("Region {} not defined, skipping".format(region))
            datasets_by_region[region] = None
            continue

        datasets = dict()

        food_items = data_by_region[region]["_food_items"]
        ffood_items = data_by_region[region]["_ffood_items"]

        ipc_df = data_by_region[region]["ipc_df"]
        food_df = data_by_region[region]["food_df"]
        ffood_df = data_by_region[region]["ffood_df"]
        conflict_df = data_by_region[region]["conflict_df"]
        weather_df = data_by_region[region]["weather_df"]

        for (i, row) in ipc_df.iterrows():
            year = row.Year
            quarter = row.Quarter
            nDays = getDays(year, quarter)
            dataset = dict()

            dataset['P2'] = row.P2perc
            dataset['P3'] = row.P3perc
            dataset['P4'] = row.P4perc

            features = []


            for item in food_items:
                market = food_df[food_df.Item.eq(item)].Market.values[0]
                t_item_df = food_df[food_df.Year.eq(year) & food_df.Quarter.eq(quarter) & food_df.Item.eq(item)]
                # dataset["{} - {}".format(item, market)] = t_item_df
                features.append(np.mean(t_item_df.Price.values) / 1e4)

            for item in ffood_items:
                market = ffood_df[ffood_df.Item.eq(item)].Market.values[0]
                t_item_df = ffood_df[ffood_df.Year.eq(year) & ffood_df.Quarter.eq(quarter) & ffood_df.Item.eq(item)]
                # dataset["{} - {}".format(item, market)] = t_item_df
                features.append(np.mean(t_item_df.Price.values) / 1e4)

            t_conflict_df = conflict_df[conflict_df.Year.eq(year) & conflict_df.Quarter.eq(quarter)]
            # dataset["Fatalities"] = t_conflict_df
            features.append(np.sum(t_conflict_df.Fatalities.values) / nDays)

            t_weather_df = weather_df[weather_df.Year.eq(year) & weather_df.Quarter.eq(quarter)]
            cycle = 1

            while (len(t_weather_df) < 10):
                t_weather_df = weather_df[weather_df.Year.eq(year + cycle) & weather_df.Quarter.eq(quarter)]
                cycle += 1
            # dataset["Temperature"] = t_weather_df
            features.append(np.mean(t_weather_df.Temperature.values))

            dataset['features'] = features
            datasets[year * 10 + quarter] = dataset
        datasets_by_region[region] = datasets
        print("Famine dataset loaded for {}".format(region))
    return datasets_by_region


def get_famine_data(region):
    print("Loading famine data for {}".format(region))
    # Transform food data:
    data = dict()

    feature_names = []

    food_df = pd.read_csv(DATA_DIR + 'clean_food.csv')
    food_df = food_df[food_df.Region.eq(region)]
    data['food_df'] = food_df

    food_items = sorted(set(food_df.Item.values))
    for food_item in food_items:
        market = food_df[food_df.Item.eq(food_item)].Market.values[0]
        feature_names.append("{} - {}".format(food_item, market))

    # Constrained by food data dates, get the earliest and latest dates here:
    e_y = min(food_df.Year.values)
    e_q = min(food_df[food_df.Year.eq(e_y)].Quarter.values)
    l_y = max(food_df.Year.values)
    l_q = max(food_df[food_df.Year.eq(l_y)].Quarter.values)

    ffood_df = pd.read_csv(DATA_DIR + 'clean_fews.csv')
    ffood_df = ffood_df[ffood_df.Item.isin(WANTEDFEWSFOOD) & ffood_df.Region.eq(region)]
    ffood_df = ffood_df[(ffood_df.Year.eq(e_y) & ffood_df.Quarter.ge(e_q)) | (ffood_df.Year.gt(e_y))]
    ffood_df = ffood_df[(ffood_df.Year.eq(l_y) & ffood_df.Quarter.le(l_q)) | (ffood_df.Year.lt(l_y))]
    data['ffood_df'] = ffood_df

    ffood_items = sorted(set(ffood_df.Item.values))
    for ffood_item in ffood_items:
        market = ffood_df[ffood_df.Item.eq(ffood_item)].Market.values[0]
        feature_names.append("{} - {}".format(ffood_item, market))

    conflict_df = pd.read_csv(DATA_DIR + "clean_conflict.csv")
    conflict_df = conflict_df[conflict_df.Region.eq(region)]
    conflict_df = conflict_df[(conflict_df.Year.eq(e_y) & conflict_df.Quarter.ge(e_q)) | (conflict_df.Year.gt(e_y))]
    conflict_df = conflict_df[(conflict_df.Year.eq(l_y) & conflict_df.Quarter.le(l_q)) | (conflict_df.Year.lt(l_y))]
    data['conflict_df'] = conflict_df

    feature_names.append("Fatalities")

    ipc_df = pd.read_csv(DATA_DIR + 'clean_ipc.csv')
    ipc_df = ipc_df[ipc_df.Region.eq(region)]
    ipc_df = ipc_df[(ipc_df.Year.eq(e_y) & ipc_df.Quarter.ge(e_q)) | (ipc_df.Year.gt(e_y))]
    ipc_df = ipc_df[(ipc_df.Year.eq(l_y) & ipc_df.Quarter.le(l_q)) | (ipc_df.Year.lt(l_y))]
    data['ipc_df'] = ipc_df

    weather_df = pd.read_csv(DATA_DIR + 'clean_weather.csv')
    weather_df = weather_df[weather_df.Station.isin(WANTEDSTATIONS)]
    weather_df = weather_df[(weather_df.Year.eq(e_y) & weather_df.Quarter.ge(e_q)) | (weather_df.Year.gt(e_y))]
    weather_df = weather_df[(weather_df.Year.eq(l_y) & weather_df.Quarter.le(l_q)) | (weather_df.Year.lt(l_y))]
    data['weather_df'] = weather_df

    feature_names.append("Temperature")

    if (len(ipc_df) <= 12):
        print("Insufficient data for region {}, trying to fit with data will give an over-fitted model".format(region))
        return None

    data["_feature_names"] = feature_names

    data["_start_year"] = e_y
    data["_start_quarter"] = e_q
    data["_end_year"] = l_y
    data["_end_quater"] = l_q

    data["_food_items"] = food_items
    data["_ffood_items"] = ffood_items

    return data


def get_famine_data_old(region):
    print("Loading famine data for {}".format(region))
    # Transform food data:
    data = dict()

    feature_names = []

    food_df = pd.read_csv(DATA_DIR + 'clean_food.csv')
    food_df = food_df[food_df.Region.eq(region)]
    data['food_df'] = food_df

    food_items = sorted(set(food_df.Item.values))
    for food_item in food_items:
        market = food_df[food_df.Item.eq(food_item)].Market.values[0]
        feature_names.append("{} - {}".format(food_item, market))

    # Constrained by food data dates, get the earliest and latest dates here:
    e_y = min(food_df.Year.values)
    e_q = min(food_df[food_df.Year.eq(e_y)].Quarter.values)
    l_y = max(food_df.Year.values)
    l_q = max(food_df[food_df.Year.eq(l_y)].Quarter.values)

    ffood_df = pd.read_csv(DATA_DIR + 'clean_fews.csv')
    ffood_df = ffood_df[ffood_df.Item.isin(WANTEDFEWSFOOD) & ffood_df.Region.eq(region)]
    ffood_df = ffood_df[(ffood_df.Year.eq(e_y) & ffood_df.Quarter.ge(e_q)) | (ffood_df.Year.gt(e_y))]
    ffood_df = ffood_df[(ffood_df.Year.eq(l_y) & ffood_df.Quarter.le(l_q)) | (ffood_df.Year.lt(l_y))]
    data['ffood_df'] = ffood_df

    ffood_items = sorted(set(ffood_df.Item.values))
    for ffood_item in ffood_items:
        market = ffood_df[ffood_df.Item.eq(ffood_item)].Market.values[0]
        feature_names.append("{} - {}".format(ffood_item, market))

    conflict_df = pd.read_csv(DATA_DIR + "clean_conflict.csv")
    conflict_df = conflict_df[conflict_df.Region.eq(region)]
    conflict_df = conflict_df[(conflict_df.Year.eq(e_y) & conflict_df.Quarter.ge(e_q)) | (conflict_df.Year.gt(e_y))]
    conflict_df = conflict_df[(conflict_df.Year.eq(l_y) & conflict_df.Quarter.le(l_q)) | (conflict_df.Year.lt(l_y))]
    data['conflict_df'] = conflict_df

    feature_names.append("Fatalities")

    ipc_df = pd.read_csv(DATA_DIR + 'clean_ipc.csv')
    ipc_df = ipc_df[ipc_df.Region.eq(region)]
    ipc_df = ipc_df[(ipc_df.Year.eq(e_y) & ipc_df.Quarter.ge(e_q)) | (ipc_df.Year.gt(e_y))]
    ipc_df = ipc_df[(ipc_df.Year.eq(l_y) & ipc_df.Quarter.le(l_q)) | (ipc_df.Year.lt(l_y))]
    data['ipc_df'] = ipc_df

    weather_df = pd.read_csv(DATA_DIR + 'clean_weather.csv')
    weather_df = weather_df[weather_df.Station.isin(WANTEDSTATIONS)]
    weather_df = weather_df[(weather_df.Year.eq(e_y) & weather_df.Quarter.ge(e_q)) | (weather_df.Year.gt(e_y))]
    weather_df = weather_df[(weather_df.Year.eq(l_y) & weather_df.Quarter.le(l_q)) | (weather_df.Year.lt(l_y))]
    data['weather_df'] = weather_df

    feature_names.append("Temperature")

    if (len(ipc_df) <= 12):
        # Insufficient data, trying to fit with data will give an over-fitted model
        return None

    datasets = dict()
    data['feature_names'] = feature_names

    for (i, row) in ipc_df.iterrows():
        year = row.Year
        quarter = row.Quarter
        nDays = getDays(year, quarter)
        dataset = dict()

        dataset['P2'] = row.P2perc
        dataset['P3'] = row.P3perc
        dataset['P4'] = row.P4perc

        features = []

        for item in food_items:
            market = food_df[food_df.Item.eq(item)].Market.values[0]
            t_item_df = food_df[food_df.Year.eq(year) & food_df.Quarter.eq(quarter) & food_df.Item.eq(item)]
            # dataset["{} - {}".format(item, market)] = t_item_df
            features.append(np.mean(t_item_df.Price.values) / 1e4)

        for item in ffood_items:
            market = ffood_df[ffood_df.Item.eq(item)].Market.values[0]
            t_item_df = ffood_df[ffood_df.Year.eq(year) & ffood_df.Quarter.eq(quarter) & ffood_df.Item.eq(item)]
            # dataset["{} - {}".format(item, market)] = t_item_df
            features.append(np.mean(t_item_df.Price.values) / 1e4)

        t_conflict_df = conflict_df[conflict_df.Year.eq(year) & conflict_df.Quarter.eq(quarter)]
        # dataset["Fatalities"] = t_conflict_df
        features.append(np.sum(t_conflict_df.Fatalities.values) / nDays)

        t_weather_df = weather_df[weather_df.Year.eq(year) & weather_df.Quarter.eq(quarter)]
        cycle = 1

        while (len(t_weather_df) < 10):
            t_weather_df = weather_df[weather_df.Year.eq(year + cycle) & weather_df.Quarter.eq(quarter)]
            cycle += 1
        # dataset["Temperature"] = t_weather_df
        features.append(np.mean(t_weather_df.Temperature.values))

        dataset['features'] = features
        datasets[year * 10 + quarter] = dataset
    data['datasets'] = datasets
    print("Famine data loaded for {}".format(region))
    return data

