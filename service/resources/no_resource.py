"""
This module contains all of Resources for the Customer API
"""
from flask import abort, request
from flask_restful import Resource
from flask_api import status    # HTTP Status Codes
from werkzeug.exceptions import BadRequest
from service import app, api
from service.models import Customer, DataValidationError

######################################################################
#  PATH: /customers/}
######################################################################
class NoResource(Resource):

    def get(self):
        app.logger.info("Request to Retrieve a customer with no id")
        abort(status.HTTP_404_NOT_FOUND, "Customer id is undefined. Please enter a customer id")

    def put(self):
        app.logger.info("Request to Retrieve a customer with no id")
        abort(status.HTTP_404_NOT_FOUND, "Customer id is undefined. Please enter a customer id")

    def delete(self):
        app.logger.info("Request to Retrieve a customer with no id")
        abort(status.HTTP_404_NOT_FOUND, "Customer id is undefined. Please enter a customer id")
