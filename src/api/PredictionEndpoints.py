from flask_restful import Resource, reqparse
from flask import Response
from utils.utils import store, app
from copy import deepcopy
import utils.DataFrameConverters as dfcs
import famine_prediction
from data_processing import famine_processing
import pandas as pd

# TODO: Merge this with DataEndpoints
def transform_data(region_pred, region):
    r_pd = dict()

    rename_map = dict(
        ipc_df="famine_risk",
        weather_df="Temperature",
        conflict_df="{} - Fatalities due to Conflict".format(region),
    )

    for (data,res) in [(region_pred, r_pd)]:
        for (k, v) in data.items():
            if k in rename_map:
                res[rename_map[k]] = v
            elif k[0] == "_":
                res[k] = v
            elif k == "food_df" or k == "ffood_df":
                f_df = v
                for item in data["_food_item_names"] if k[0:2] == "fo" else data["_ffood_item_names"]:
                    item_df = f_df[f_df.Item_Name == item]
                    res[item] = item_df
            else:
                res[k] = v
    return r_pd

def transform_data_back(data, region):
    res = dict()

    rename_map = {
        "famine_risk":"ipc_df",
        "Temperature":"weather_df",
        "{} - Fatalities due to Conflict".format(region) : "conflict_df",
        "_features":"features"
    }

    cols = ['Date', 'Region', 'Market', 'Item', 'Price', 'Year', 'Month', 'Quarter',
       'Item_Name']

    food_df = pd.DataFrame(columns=cols)
    ffood_df = pd.DataFrame(columns=cols)
    for (k, v) in data.items():
        if k in rename_map:
            res[rename_map[k]] = v
        elif k[0] == "_":
            res[k] = v
        elif k in data["_food_item_names"]:
            # Build food_df
            print(v)
            food_df = food_df.append(v, ignore_index=True)
        elif k in data["_ffood_item_names"]:
            # Build ffood_df
            ffood_df = ffood_df.append(v, ignore_index=True)
        else:
            res[k] = v

    print(food_df)
    res["food_df"] = food_df
    res["ffood_df"] = ffood_df

    return res




class RegionPredictionEndpoint(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("changes", type=list, location="json", required=True)
        super(RegionPredictionEndpoint, self).__init__()

    def post(self, region):
        args = self.reqparse.parse_args()
        changes = args["changes"]

        print(changes)
        data = store().per_region_pred_data[region].copy()
        if len(changes) != 0:
            for (k, v) in data.items():
                data[k] = deepcopy(v)
            data = transform_data(data, region)

            for change in changes:
                print("Changing {} @ {},{} to {}".format(*change.values()))
                df = data[change["source"]]
                df2 = df[df.Year == change["year"]]
                df2 = df2[df2.Month == change["month"]]
                df[change["column"]][df2.index[0]] = change["value"]

            data = transform_data_back(data, region)

        res = famine_prediction.predict_famine(
            store().per_region_model[region].fit.fit,
            famine_processing.calculate_datasets([region], {region:data})[region]
        )

        response = dict(
            success=True,
            region=region,
            data=res
        )

        return Response(dfcs.to_json_string(response), mimetype="application/json")
