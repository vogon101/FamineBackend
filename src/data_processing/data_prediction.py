from data_processing.data_constants import *
from data_processing.data_utils import *
import copy
import math
import pandas as pd

#Assumed data is per-region already
def predict_data(data, end_year, end_quarter):
    print("Calculating prediction data up to q{}/{}".format(end_quarter, end_year))
    new_data = dict()
    #feature_names = data['feature_names'][:]
    
    food_df = data['food_df'].copy()
    ffood_df = data['ffood_df'].copy()
    weather_df = data['weather_df'].copy()
    conflict_df = data['conflict_df'].copy()
    new_data['ipc_df'] = data['ipc_df'].copy()
    end_month = [0, 3, 6, 9, 12][end_quarter]
    end_day = [0, 31, 30, 30, 31][end_quarter]
    print(conflict_df)
    new_rows = []
    food_items = sorted(set(food_df.Item.values))
    for item in food_items:
        
        t_item_df = food_df[food_df.Item.eq(item)]
        
        market = t_item_df.Market.values[0]
        region = t_item_df.Region.values[0]
        last_year = max(t_item_df.Year.values)
        last_quarter = max(t_item_df[t_item_df.Year.eq(last_year)].Quarter.values)
        last_month = max(t_item_df[t_item_df.Year.eq(last_year)].Month.values)
        last_price = t_item_df.loc[t_item_df.Year.eq(last_year) & t_item_df.Month.eq(last_month)].Price.values[0]
        
        for new_year in range(last_year, end_year+1):
            month_start = last_month+1 if new_year == last_year else 1
            month_end = end_month+1 if new_year == end_year else 13
            for new_month in range(month_start, month_end):
                new_rows.append(dict(
                    Date = getDate(new_year, new_month, 1),
                    Region = region,
                    Market = market,
                    Item = item,
                    Price = last_price,
                    Year = new_year,
                    Month = new_month,
                    Quarter = math.ceil(new_month/3)
                ))
    food_df = food_df.append(new_rows).sort_values(by=['Item', 'Date']).reset_index(drop=True)
    new_data['food_df'] = food_df
    
    ffood_items = sorted(set(ffood_df.Item))
    new_rows=[]
    for item in ffood_items:
        
        t_item_df = ffood_df[ffood_df.Item.eq(item)]
        
        market = t_item_df.Market.values[0]
        region = t_item_df.Region.values[0]
        last_year = max(t_item_df.Year.values)
        last_quarter = max(t_item_df[t_item_df.Year.eq(last_year)].Quarter.values)
        last_month = max(t_item_df[t_item_df.Year.eq(last_year)].Month.values)
        last_price = t_item_df.loc[t_item_df.Year.eq(last_year) & t_item_df.Month.eq(last_month)].Price.values[0]
        
        for new_year in range(last_year, end_year+1):
            if(last_month==12 and new_year == last_year):
                continue
            month_start = last_month+1 if new_year == last_year else 1
            month_end = end_month+1 if new_year == end_year else 13
            for new_month in range(month_start, month_end):
                new_rows.append(dict(
                    Date = getDate(new_year, new_month, 1),
                    Region = region,
                    Market = market,
                    Item = item,
                    Price = last_price,
                    Year = new_year,
                    Month = new_month,
                    Quarter = math.ceil(new_month/3)
                ))
    ffood_df = ffood_df.append(new_rows).sort_values(by=['Item', 'Date']).reset_index(drop=True)
    new_data['ffood_df'] = ffood_df
    
    new_rows = []
    region = conflict_df.Region.values[0]
    last_year = max(conflict_df.Year.values)
    last_month = max(conflict_df[conflict_df.Year.eq(last_year)].Month.values)
    last_fatality = conflict_df.loc[conflict_df.Year.eq(last_year) & conflict_df.Month.eq(last_month)].Fatalities.values[0]
    
    for new_year in range(last_year, end_year+1):
        month_start = last_month+1 if new_year == last_year else 1
        month_end = end_month+1 if new_year == end_year else 13
        for new_month in range(month_start, month_end):
            new_rows.append(dict(
                Region = region,
                Date = getDate(new_year, new_month, 1),
                Fatalities = last_fatality,
                Year = new_year,
                Month = new_month,
                Quarter = math.ceil(new_month/3)
            ))
    conflict_df = conflict_df.append(new_rows).sort_values(by=['Date']).reset_index(drop=True)
    new_data['conflict_df'] = conflict_df
    
    new_rows = []
    station = weather_df.Station.values[0]
    last_year = max(weather_df.Year.values)
    last_month = max(weather_df[weather_df.Year.eq(last_year)].Month.values)
    last_temperature = weather_df[weather_df.Year.eq(last_year) & weather_df.Month.eq(last_month)].Temperature.values[0]
    
    for new_year in range(last_year, end_year+1):
        month_start = last_month+1 if new_year == last_year else 1
        month_end = end_month+1 if new_year == end_year else 13
        for new_month in range(month_start, month_end):
            new_rows.append(dict(
                Station = station,
                Date = getDate(new_year, new_month, 1),
                Temperature = last_temperature,
                Year = new_year,
                Month = new_month,
                Quarter = math.ceil(new_month/3)
            ))    
    weather_df = weather_df.append(new_rows).sort_values(by=['Date']).reset_index(drop=True)
    new_data['weather_df'] = weather_df

    new_data["_food_items"] = food_items
    new_data["_ffood_items"] = ffood_items

    """
    datasets = copy.deepcopy(data['datasets'])
    
    last_date = max(datasets.keys())
    last_year = last_date//10
    last_quarter = last_date%10
    
    for new_year in range(last_year, end_year+1):
        quarter_start = last_quarter+1 if new_year == last_year else 1
        quarter_end = end_quarter+1 if new_year == end_year else 5
        for new_quarter in range(quarter_start, quarter_end):
            nDays = getDays(new_year, new_quarter)
            dataset = dict()
            features=  []
            
            for item in food_items:
                market = food_df[food_df.Item.eq(item)].Market.values[0]
                t_item_df = food_df[food_df.Year.eq(new_year) & food_df.Quarter.eq(new_quarter) & food_df.Item.eq(item)]
                features.append(np.mean(t_item_df.Price.values)/1e4)
                
            for item in ffood_items:
                market = ffood_df[ffood_df.Item.eq(item)].Market.values[0]
                t_item_df = ffood_df[ffood_df.Year.eq(new_year) & ffood_df.Quarter.eq(new_quarter) & ffood_df.Item.eq(item)]
                features.append(np.mean(t_item_df.Price.values)/1e4)

            t_conflict_df = conflict_df[conflict_df.Year.eq(new_year) & conflict_df.Quarter.eq(new_quarter)]
            features.append(np.sum(t_conflict_df.Fatalities.values)/nDays)

            t_weather_df = weather_df[weather_df.Year.eq(new_year) & weather_df.Quarter.eq(new_quarter)]
            features.append(np.mean(t_weather_df.Temperature.values))

            dataset['features'] = features
            datasets[new_year*10+new_quarter] = dataset
    new_data['datasets'] = datasets
    """
    return new_data
        