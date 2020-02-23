import pystan
import pickle
from hashlib import md5
import os
from config import STAN_MODEL_CACHE


def StanModel_cache(model_code, model_name=None, **kwargs) -> (pystan.StanModel, str):
    if not os.path.isdir(STAN_MODEL_CACHE):
        os.mkdir(STAN_MODEL_CACHE)
    """Use just as you would `stan`"""
    code_hash = md5(model_code.encode('ascii')).hexdigest()
    if model_name is None:
        cache_fn = STAN_MODEL_CACHE + '\cached-model-{}.pkl'.format(code_hash)
    else:
        cache_fn = STAN_MODEL_CACHE + '\cached-{}-{}.pkl'.format(model_name, code_hash)
    try:
        sm = pickle.load(open(cache_fn, 'rb'))
    except:
        sm = pystan.StanModel(model_code=model_code, model_name=model_name)
        with open(cache_fn, 'wb') as f:
            pickle.dump(sm, f)
    else:
        print("Using cached StanModel")
    return sm,code_hash


pystan.SM_cache = StanModel_cache
