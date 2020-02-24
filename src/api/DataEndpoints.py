from flask import Flask
from flask_restful import Resource
import pandas as pd

def app():
    from FamineApp import famine_app
    return famine_app

def store():
    from FamineApp import famine_app
    return famine_app.famine_store

class AllDataEndpoint(Resource):

    def get(self):

        historical_data = dict()
        predicted_data = dict()

        for region in store().REGIONS:
            r_hd = dict()
            r_pd = dict()
            for (k,v) in store().per_region_data[region].items():
                if isinstance(v, pd.DataFrame): r_hd[k] = v.to_json()
                elif isinstance(v, list): r_hd[k] = v
                else: r_hd[k] = str(v)

            for (k,v) in store().per_region_pred_data[region].items():
                if isinstance(v, pd.DataFrame): r_pd[k] = v.to_json()
                elif isinstance(v, list): r_pd[k] = v
                else: r_pd[k] = str(v)

            historical_data[region] = r_hd
            predicted_data[region] = r_pd

        response = dict(
            success = True,
            historical_data = historical_data,
            predicted_data = predicted_data
        )
        return response


class RegionsListEndpoint(Resource):

    def get(self):
        return dict(
            all_regions = app().famine_store.REGIONS,
            fitted_regions = app().famine_store.FITTED_REGIONS
        )