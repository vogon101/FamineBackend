from multiprocessing import freeze_support

from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from FamineStore import FamineStore
from api.DataEndpoints import *
from api.PredictionEndpoints import *


class FamineApp(object):
    famine_store = None

    def main(self):
        freeze_support()

        f_app = Flask(__name__)
        cors = CORS(f_app, resources={r"/*": {"origins": "*"}})
        api = Api(f_app)

        self.famine_store = FamineStore()

        api.add_resource(RegionsListEndpoint, '/data/region_list')
        api.add_resource(AllDataEndpoint, '/data/all')
        api.add_resource(GetRegionDataEndpoint, '/data/region/<string:region>')

        api.add_resource(RegionPredictionEndpoint, '/prediction/region/<string:region>')
        api.add_resource(PredictionSummaryEndpoint, '/prediction/summary')

        f_app.run(debug=True, use_reloader=True)


famine_app = FamineApp()
