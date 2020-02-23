from flask import Flask
from flask_restful import Resource

class ModelResource(Resource):

    def get(self):
        return {"model" : "model"}