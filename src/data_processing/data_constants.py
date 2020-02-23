import numpy as np

# Constants:
WANTEDPRODUCTS = {'Rice (imported) - Retail': 0, 'Maize (white) - Retail': 1, 'Sorghum (red) - Retail': 2}
# WANTEDPRODUCTS = {'Maize (white) - Retail':1}
WANTEDFEWSFOOD = {'Cowpeas (Red)'}
# WANTEDSTATIONS = {'EGAL INTL':0, 'MOGADISHU': 1, 'BOSASO':2}
WANTEDSTATIONS = {'EGAL INTL': 0}

MONTHS = list(np.cumsum([0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]))
LEAPS = list(np.cumsum([0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]))