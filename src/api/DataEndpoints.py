from flask import Response
from flask_restful import Resource
import pandas as pd
from config import REGIONS
from api.utils import DataFrameConverters as dfcs

def app():
    from FamineApp import famine_app
    return famine_app

def store():
    from FamineApp import famine_app
    return famine_app.famine_store



def region_to_json(region):
    r_hd = dict()
    r_pd = dict()

    rename_map = dict(
        ipc_df="famine_risk",
        weather_df="Temperature",
        conflict_df="{} - Fatalities due to Conflict".format(region)
    )

    region_data = store().per_region_data[region]
    region_pred = store().per_region_pred_data[region]

    for (data,res) in [(region_data, r_hd), (region_pred, r_pd)]:
        for (k, v) in data.items():
            if k[0] == "_":
                res[k] = dfcs.JsonStr(dfcs.to_json_string(v))
            elif k == "food_df" or k == "ffood_df":
                f_df = v
                print(f_df)
                for item in data["_food_item_names"] if k[0:2] == "fo" else data["_ffood_item_names"]:
                    print(item)
                    item_df = f_df[f_df.Item_Name == item]
                    res[item] = dfcs.JsonStr(dfcs.to_json_string(item_df))
            elif k in rename_map:
                res[rename_map[k]] = dfcs.JsonStr(dfcs.to_json_string(v))
            else:
                res[k] = dfcs.JsonStr(dfcs.to_json_string(v))

    for (k, v) in store().per_region_pred_data[region].items():
        if k[0] == "_":
            pass
        else:
            r_pd[k] = dfcs.to_json_string(v)
    return (r_hd, r_pd)


class AllDataEndpoint(Resource):

    def get(self):

        historical_data = dict()
        predicted_data = dict()

        for region in REGIONS:
            if region in store().FITTED_REGIONS:
                historical_data[region], predicted_data[region] = region_to_json(region)
            else:
                historical_data[region] = {}
                predicted_data[region] = {}



        response = dict(
            success = True,
            historical_data = historical_data,
            predicted_data = predicted_data
        )
        return response


class GetRegionDataEndpoint(Resource):

    def get(self, region):
        if region not in REGIONS:
            return dict(success = False, error="Region does not exist")

        if region not in store().FITTED_REGIONS:
            return dict(success = False, error="Region not fitted: not enough data")

        historical_data, predicted_data = region_to_json(region)

        response = dfcs.to_json_string(dict(
            success=True,
            historical_data=historical_data,
            predicted_data=predicted_data
        ))
        return Response(response, mimetype="application/json")


class RegionsListEndpoint(Resource):

    def get(self):
        return dict(
            all_regions = REGIONS,
            fitted_regions = store().FITTED_REGIONS
        )