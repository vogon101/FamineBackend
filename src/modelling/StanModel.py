import pystan
from stan_utils import StanModel_cache
import pickle
from config import *
import StanModelFit


class StanModel(object):

    name = None
    version = None
    code_path = None
    code_hash = None
    fit_data = None

    __instance: pystan.StanModel = None

    __fit = None

    def __init__(self, name, ver, data=None):
        self.name = name
        self.version = ver
        self.code_path = STAN_MODEL_DIR + self.name + "_v" + str(self.version) + ".stan"
        self.fit_data = data

        with open(self.code_path, "r") as f:
            self.__instance, self.code_hash = StanModel_cache(model_code=f.read(), model_name=self.name)

    @property
    def instance(self) -> pystan.StanModel:
        return self.__instance

    @property
    def fit(self):
        return self.__fit

    def get_fit(self, dataid, iters=1000, chains=4, control = dict()):
        uuid = dataid + "_" + self.code_hash
        if self.fit is not None and self.fit.uuid == uuid:
            return self.fit
        else:
            try:
                self.__fit = StanModelFit.StanModelFit.FromPath(self, uuid)
            except FileNotFoundError as e:
                print("Failed to load fit with exception " + str(e))
                if self.fit_data is not None:
                    print("Attempting to fit the model from given data")
                    self.__fit = StanModelFit.StanModelFit.FromCalculation(self, uuid, iters, chains, control)
                else:
                    raise Exception("Data not available for fitting model")
        return self.fit









