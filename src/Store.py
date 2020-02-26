"""
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


"""
