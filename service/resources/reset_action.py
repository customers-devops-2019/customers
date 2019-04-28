"""
This module contains routes without Resources
"""
from flask import abort
from flask_api import status
from flask_restful import Resource
from service.models import Customer

######################################################################
# UNSUBSCRIBE
######################################################################
class ResetAction(Resource):
    """ Resource to Unsubscribe a Customer """
    def delete(self):
        """ Delete all Customers """
        Customer.remove_all()
        return '', status.HTTP_204_NO_CONTENT
