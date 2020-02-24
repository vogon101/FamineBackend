import pandas
import pystan
from modelling.StanModel import StanModel
from modelling.StanModelFit import StanModelFit

class Store(object):

    name = "Store"

    model = None

    data = None
    
    def __init__(self, name, model, data):
        object.__init__(self)
        self.name = name
        self.model = model
        self.data = data

    @property
    def features(self):
        return []

    @property
    def feature_names(self, region):
        if(data[region]):
            return data[region]['feature_names']
        else:
            return None

    @property
    def fit_data(self):
        return {}


class ClimateStore(Store):

    climate_data = None

    def __init__(self):

        climate = pandas.read_csv('https://teachingfiles.blob.core.windows.net/datasets/climate.csv')
        df = climate.loc[(climate.station == 'Cambridge') & (climate.yyyy >= 1985)].copy()
        df['t'] = df.yyyy + (df.mm - 1) / 12
        df['temp'] = (df.tmin + df.tmax) / 2
        self.climate_data = df
        self.model_data = {"J": len(df), "dates": df['t'], "y": df["temp"]}

        self.model = StanModel("ClimateModel", 1, self.model_data)
        #self.model.__fit = StanModelFit.FromCalulation(self.model, "data1")
        self.model.get_fit("data_1")

        Store.__init__(self, "ClimateStore", self.model)


