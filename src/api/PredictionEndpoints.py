from copy import deepcopy

import pandas as pd
from flask import Response
from flask_restful import Resource, reqparse

import famine_prediction
import utils.DataFrameConverters as dfcs
from config import REGIONS
from data_processing import famine_processing
from utils.utils import store


# TODO: Merge this with DataEndpoints
def transform_data(region_pred, region):
    r_pd = dict()

    rename_map = dict(
        ipc_df="famine_risk",
        weather_df="Temperature",
        conflict_df="{} - Fatalities due to Conflict".format(region),
    )

    for (data, res) in [(region_pred, r_pd)]:
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
        "famine_risk": "ipc_df",
        "Temperature": "weather_df",
        "{} - Fatalities due to Conflict".format(region): "conflict_df",
        "_features": "features"
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
            food_df = food_df.append(v, ignore_index=True)
        elif k in data["_ffood_item_names"]:
            # Build ffood_df
            ffood_df = ffood_df.append(v, ignore_index=True)
        else:
            res[k] = v

    res["food_df"] = food_df
    res["ffood_df"] = ffood_df

    return res


def predict_region(region, changes):
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
        famine_processing.calculate_datasets([region], {region: data})[region]
    )

    return res


class RegionPredictionEndpoint(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("changes", type=list, location="json", required=True)
        super(RegionPredictionEndpoint, self).__init__()

    def get(self, region):

        if region not in REGIONS:
            return dict(success=False, error="Region does not exist")

        if region not in store().FITTED_REGIONS:
            return dict(success=False, error="Region not fitted: not enough data")

        response = dict(
            success=True,
            region=region,
            data=predict_region(region, [])
        )

        return Response(dfcs.to_json_string(response), mimetype="application/json")

    def post(self, region):

        if region not in REGIONS:
            return dict(success=False, error="Region does not exist")

        if region not in store().FITTED_REGIONS:
            return dict(success=False, error="Region not fitted: not enough data")

        args = self.reqparse.parse_args()
        changes = args["changes"]

        print(changes)

        response = dict(
            success=True,
            region=region,
            data=predict_region(region, changes)
        )

        return Response(dfcs.to_json_string(response), mimetype="application/json")


class PredictionSummaryEndpoint(Resource):

    def get(self):

        region_json = dict()

        for region in REGIONS:
            if region in store().FITTED_REGIONS:
                region_json[region] = dict(
                    fitted=True,
                    data=predict_region(region, [])
                )
            else:
                region_json[region] = dict(fitted=False)

        response = dict(
            success=True,
            data=region_json
        )

        return Response(dfcs.to_json_string(response), mimetype="application/json")
