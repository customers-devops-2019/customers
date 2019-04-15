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
class UnsubscribeAction(Resource):
    """ Resource to Unsubscribe a Customer """
    def put(self, customer_id):
        """ Unsubscribe a Customer """
        customer = Customer.find(customer_id)
        if not customer:
            abort(status.HTTP_404_NOT_FOUND, "Customer with id '{}' was not found.".format(customer_id))
        customer.subscribed = False
        customer.save()
        return customer.serialize(), status.HTTP_200_OK
