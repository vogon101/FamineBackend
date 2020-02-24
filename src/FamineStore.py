from Store import Store
import numpy as np
import datetime as dt
import pandas as pd
from data_processing.famine_processing import load_data, calculate_datasets,get_famine_data
from modelling.StanModel import StanModel
from config import *
from data_processing.data_prediction import predict_data


class FamineStore(Store):

    REGIONS = ['Awdal']#['Awdal', 'Bakool', 'Banadir', 'Bari', 'Bay', 'Galgaduud', 'Gedo', 'Hiraan', 'Lower Juba', 'Lower Shabelle', 'Middle Juba', 'Middle Shabelle', 'Mudug', 'Nugaal', 'Sanaag', 'Sool', 'Togdheer', 'Woqooyi Galbeed']
    FITTED_REGIONS = []

    per_region_data = None
    per_region_datasets = None
    per_region_model = None
    features = None

    prediction_date = (1, 2020)
    per_region_pred_data = dict()
    pre_region_pred_datasets = dict()

    def __init__(self):
        self.per_region_model = dict()
        self.per_region_data = load_data(self.REGIONS)
        self.per_region_datasets = calculate_datasets(self.REGIONS, self.per_region_data)

        for region in self.REGIONS:
            if self.per_region_data[region]:
                datasets = self.per_region_datasets[region]
                dates = sorted(datasets.keys())
                
                nFeatures = len(datasets[dates[0]]['features'])
                features = [datasets[date]['features'] for date in dates]
                response_2 = [max(datasets[date]['P2'], 1e-5) for date in dates]
                response_3 = [max(datasets[date]['P3'], 1e-5)  for date in dates]
                response_4 = [max(datasets[date]['P4'], 1e-5)  for date in dates]
                
            
                famine_model_data = dict(
                    N = len(dates),
                    K = nFeatures,
                    feats = features,
                    response_2 = response_2,
                    response_3 = response_3,
                    response_4 = response_4
                )

                self.per_region_model[region] = StanModel("FamineModel_Beta", 1, famine_model_data)
                self.per_region_model[region].get_fit("famine_beta_1_" + region, control=dict(max_treedepth=12))

                self.per_region_pred_data[region] = predict_data(
                    self.per_region_data[region],
                    self.prediction_date[1],
                    self.prediction_date[0]
                )

        self.FITTED_REGIONS = [x for x in self.per_region_model.keys()]

        self.per_region_pred_datasets = calculate_datasets(self.FITTED_REGIONS, self.per_region_pred_data)

        print("Successfully loaded data, datasets and predictions for regions:")
        for x in self.FITTED_REGIONS:
            print("- {}".format(x))
        print("Skipped regions:")
        for x in self.REGIONS:
            if x not in self.FITTED_REGIONS:
                print("- {}".format(x))

        Store.__init__(self, "FamineStore", self.per_region_model, self.per_region_data)