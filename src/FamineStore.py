from Store import Store
import numpy as np
import datetime as dt
import pandas as pd
from data_processing.famine_processing import get_famine_data
from modelling.StanModel import StanModel


class FamineStore(Store):

    datasets = None
    train_dates = None
    nFeatures = None
    features = None

    def __init__(self):
        REGION = "Bakool"
        STARTTIME = 2016

        self.datasets, self.train_dates, self.nFeatures, self.features = get_famine_data(REGION, STARTTIME)

        response = [self.datasets[date]['ipc'][0]['p3perc'] for date in self.train_dates]
        famine_model_data = dict(
            N=len(self.train_dates),
            K=self.nFeatures,
            feats=self.features,
            # K = newNFeatures,
            # feats = new_features,
            response=response
        )

        self.model = StanModel("FamineModel_Proto", 1, famine_model_data)
        self.model.get_fit("famine_proto_1_" + REGION + "_" + str(STARTTIME))

        Store.__init__(self, "FamineStore", self.model)