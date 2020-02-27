import pickle

from config import *


class StanModelFit(object):
    uuid = None
    model = None
    fit = None

    def __init__(self, model, uuid, fit):
        self.uuid = uuid
        self.model = model
        self.fit = fit

    @staticmethod
    def FromPath(model, uuid):
        path = STAN_FIT_DIR + model.name + "_v" + str(model.version) + "_fit_" + str(uuid) + ".fit"
        print("Reading model fit from {}".format(path))

        assert model.instance is not None, "Model must be loaded before fit"

        with open(path, "rb") as f:
            fit_obj = pickle.load(f)
            return StanModelFit(model, uuid, fit_obj)

    @staticmethod
    def FromCalculation(model, uuid, iters=1000, chains=4, save=True, control=None):
        if control is None:
            control = dict()
        model_fit = model.instance.sampling(data=model.fit_data, iter=iters, chains=chains, control=control)
        if save:
            os.makedirs(STAN_FIT_DIR, exist_ok=True)
            path = STAN_FIT_DIR + model.name + "_v" + str(model.version) + "_fit_" + str(uuid) + ".fit"
            print("Saving model fit to {}".format(path))

            with open(path, "wb") as f:
                pickle.dump(model_fit, f)

        else:
            print("Not saving model fit")
        return StanModelFit(model, uuid, model_fit)
