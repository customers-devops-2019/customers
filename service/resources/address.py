"""
This module contains routes without Resources
"""
from flask import abort
from flask_api import status
from flask_restful import Resource
from service.models import Customer

######################################################################
# Address
######################################################################
class Address(Resource):
    def get(self, customer_id):
        """
        Retrieve a single Customer Address
        This endpoint will return a Customer based on it's id
        """
        customer = Customer.find(customer_id)
        if not customer:
            abort(status.HTTP_404_NOT_FOUND, "Customer with id '{}' was not found.".format(customer_id))
        return customer.serialize()["address"], status.HTTP_200_OK
