from flask import Flask
from flask_restful import Resource, Api
from FamineStore import FamineStore
from api.ModelEndpoint import ModelResource
from multiprocessing import freeze_support

def main():
    freeze_support()

    app = Flask(__name__)
    api = Api(app)

    store = FamineStore()

    api.add_resource(ModelResource, '/model')

    app.run(debug=True, use_reloader=False)

if __name__ == '__main__':
    main()
    #app.run(debug=True)
    pass