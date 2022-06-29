from flask_restful import Resource, Api
from app.configs import app
from index import EmployeeResource

api = Api(app)

api.add_resource(EmployeeResource, "/api", methods=["GET"])
