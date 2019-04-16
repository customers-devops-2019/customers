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
#  PATH: /customers/{id}
######################################################################
class CustomerResource(Resource):
    """
    CustomerResource class

    Allows the manipulation of a single Customer
    GET /customer{id} - Returns a Customer with the id
    PUT /customer{id} - Update a Customer with the id
    DELETE /customer{id} -  Deletes a Customer with the id
    """

    def get(self, customer_id):
        """
        Retrieve a single Customer

        This endpoint will return a Customer based on it's id
        """
        app.logger.info("Request to Retrieve a customer with id [%s]", customer_id)
        customer = Customer.find(customer_id)
        if not customer:
            abort(status.HTTP_404_NOT_FOUND, "Customer with id '{}' was not found.".format(customer_id))
        return customer.serialize(), status.HTTP_200_OK

    def put(self, customer_id):
        """
        Update a Customer

        This endpoint will update a Customer based the body that is posted
        """
        app.logger.info('Request to Update a customer with id [%s]', customer_id)
        #check_content_type('application/json')
        customer = Customer.find(customer_id)
        if not customer:
            abort(status.HTTP_404_NOT_FOUND, "Customer with id '{}' was not found.".format(customer_id))

        payload = request.get_json()
        try:
            customer.deserialize(payload)
        except DataValidationError as error:
            raise BadRequest(str(error))

        customer.id = customer_id
        customer.save()
        return customer.serialize(), status.HTTP_200_OK

    def delete(self, customer_id):
        """
        Delete a Customer

        This endpoint will delete a Customer based the id specified in the path
        """
        app.logger.info('Request to Delete a customer with id [%s]', customer_id)
        customer = Customer.find(customer_id)
        if customer:
            customer.delete()
        return '', status.HTTP_204_NO_CONTENT
