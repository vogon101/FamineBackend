import os

STAN_FIT_DIR = "stan{}fits{}".format(os.sep, os.sep)
STAN_MODEL_DIR = "stan{}src{}".format(os.sep, os.sep)
STAN_MODEL_CACHE = "stan{}model-cache".format(os.sep)

DATA_DIR = "..{}data{}".format(os.sep, os.sep)

DEVELOPMENT_MODE = True
REGIONS = ['Awdal', 'Gedo', 'Middle Juba'] if DEVELOPMENT_MODE else \
    ['Awdal', 'Bakool', 'Banadir', 'Bari', 'Bay', 'Galgaduud', 'Gedo', 'Hiraan', 'Lower Juba', 'Lower Shabelle',
     'Middle Juba', 'Middle Shabelle', 'Mudug', 'Nugaal', 'Sanaag', 'Sool', 'Togdheer', 'Woqooyi Galbeed']
