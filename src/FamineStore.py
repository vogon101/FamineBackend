from Store import Store
import numpy as np
import datetime as dt
import pandas as pd
from data_processing.famine_processing import get_famine_data
from modelling.StanModel import StanModel


class FamineStore(Store):
    REGIONS = ['Awdal', 'Bakool', 'Banadir', 'Bari', 'Bay', 'Galgaduud', 'Gedo', 'Hiraan', 'Lower Juba', 'Lower Shabelle', 'Middle Juba', 'Middle Shabelle', 'Mudug', 'Nugaal', 'Sanaag', 'Sool', 'Togdheer', 'Woqooyi Galbeed']
    per_region_data = None
    per_region_model = None
    datasets = None
    train_dates = None
    nFeatures = None
    features = None

    def __init__(self):
        per_region_data = dict()
        per_region_model = dict()
        for region in REGIONS:
            self.per_region_data[region] = get_famine_data(region)
            if(self.per_region_data[region]):
                region_datasets = self.per_region_data[region]['datasets']
                dates = sorted(region_datasets.keys())
                
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

        Store.__init__(self, "FamineStore", self.per_region_model, self.per_region_data)