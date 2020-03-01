from config import REGIONS
from data_processing.data_prediction import predict_data
from data_processing.famine_processing import load_data, calculate_datasets
from modelling.StanModel import StanModel
import numpy as np

class FamineStore(object):
    FITTED_REGIONS = []

    per_region_data = None
    per_region_datasets = None
    per_region_model = None
    features = None

    prediction_date = (1, 2021)
    per_region_pred_models = dict()
    per_region_pred_data = dict()
    pre_region_pred_datasets = dict()

    def __init__(self):
        self.per_region_model = dict()
        self.per_region_data = load_data(REGIONS)
        self.per_region_datasets = calculate_datasets(REGIONS, self.per_region_data)
        self.per_region_pred_models = dict()
        for region in REGIONS:
            if self.per_region_data[region]:
                datasets = self.per_region_datasets[region]
                dates = sorted(datasets.keys())

                nFeatures = len(datasets[dates[0]]['features'])
                features = [datasets[date]['features'] for date in dates]
                response_2 = [max(datasets[date]['P2'], 1e-5) for date in dates]
                response_3 = [max(datasets[date]['P3'], 1e-5) for date in dates]
                response_4 = [max(datasets[date]['P4'], 1e-5) for date in dates]

                famine_model_data = dict(
                    N=len(dates),
                    K=nFeatures,
                    feats=features,
                    response_2=response_2,
                    response_3=response_3,
                    response_4=response_4
                )

                self.per_region_model[region] = StanModel("FamineModel_Beta", 1, famine_model_data)
                self.per_region_model[region].get_fit("famine_beta_1_" + region, control=dict(max_treedepth=12))
                
                
                self.per_region_pred_models[region] = dict()
                food_df = self.per_region_data[region]['food_df']
                for item in self.per_region_data[region]['_food_items']:
                    item_df = food_df[food_df.Item.eq(item)].sort_values(by="Date")
                    pred_model_data = dict(
                        N = 18,
                        y = np.log((item_df.Price.values/1e5).tolist()[-18:]),
                        K = 3
                    )
                    self.per_region_pred_models[region][item] = StanModel("PredictionModel", 1, pred_model_data)
                    self.per_region_pred_models[region][item].get_fit("prediction_1_"+region+"_"+item)
                
                ffood_df = self.per_region_data[region]['ffood_df']
                for item in self.per_region_data[region]['_ffood_items']:
                    item_df = ffood_df[ffood_df.Item.eq(item)].sort_values(by="Date")
                    pred_model_data = dict(
                        N = 18,
                        y = np.log((item_df.Price.values/1e5).tolist()[-18:]),
                        K = 3
                    )
                    self.per_region_pred_models[region][item] = StanModel("PredictionModel", 1, pred_model_data)
                    self.per_region_pred_models[region][item].get_fit("prediction_1_"+region+"_"+item)
                    
                weather_df = self.per_region_data[region]['weather_df'].sort_values(by="Date")
                pred_model_data = dict(
                    N = len(weather_df),
                    y = (weather_df.Temperature.values/1e2).tolist(),
                    K = 3
                )
                self.per_region_pred_models[region]['Temperature'] = StanModel("PredictionModel", 1, pred_model_data)
                self.per_region_pred_models[region]['Temperature'].get_fit("prediction_1_"+region+"_Temperature")
                
                self.per_region_pred_data[region] = predict_data(
                    self.per_region_data[region],
                    self.per_region_pred_models[region],
                    self.prediction_date[1],
                    self.prediction_date[0]
                )
                
                

        self.FITTED_REGIONS = [x for x in self.per_region_model.keys()]

        self.per_region_pred_datasets = calculate_datasets(self.FITTED_REGIONS, self.per_region_pred_data)

        print("Successfully loaded data, datasets and predictions for regions:")
        for x in self.FITTED_REGIONS:
            print("- {}".format(x))
        print("Skipped regions:")
        for x in REGIONS:
            if x not in self.FITTED_REGIONS:
                print("- {}".format(x))
