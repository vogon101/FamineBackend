from flask import Flask
from flask_restful import Resource
import pandas as pd
from config import REGIONS

def app():
    from FamineApp import famine_app
    return famine_app

def store():
    from FamineApp import famine_app
    return famine_app.famine_store

def region_to_json(region):
    r_hd = dict()
    r_pd = dict()
    for (k, v) in store().per_region_data[region].items():
        if isinstance(v, pd.DataFrame):
            r_hd[k] = v.to_json()
        elif isinstance(v, list):
            r_hd[k] = v
        else:
            r_hd[k] = str(v)

    for (k, v) in store().per_region_pred_data[region].items():
        if isinstance(v, pd.DataFrame):
            r_pd[k] = v.to_json()
        elif isinstance(v, list):
            r_pd[k] = v
        else:
            r_pd[k] = str(v)
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
        historical_data = dict()
        predicted_data = dict()

        historical_data[region], predicted_data[region] = region_to_json(region)

        response = dict(
            success=True,
            historical_data=historical_data,
            predicted_data=predicted_data
        )
        return response


class RegionsListEndpoint(Resource):

    def get(self):
        return dict(
            all_regions = REGIONS,
            fitted_regions = store().FITTED_REGIONS
        )