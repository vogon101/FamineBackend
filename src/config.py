STAN_FIT_DIR = "stan\\fits\\"
STAN_MODEL_DIR = "stan\\src\\"
STAN_MODEL_CACHE = "stan\\model-cache"

DATA_DIR = "..\\data\\"

DEVELOPMENT_MODE = True
REGIONS = ['Awdal', 'Gedo'] if DEVELOPMENT_MODE else\
    ['Awdal', 'Bakool', 'Banadir', 'Bari', 'Bay', 'Galgaduud', 'Gedo', 'Hiraan', 'Lower Juba', 'Lower Shabelle',
     'Middle Juba', 'Middle Shabelle', 'Mudug', 'Nugaal', 'Sanaag', 'Sool', 'Togdheer', 'Woqooyi Galbeed']