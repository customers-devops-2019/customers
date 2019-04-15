"""
This module contains the Customer Collection Resource
"""
from flask import request, abort
from flask_restful import Resource
from flask_api import status    # HTTP Status Codes
from werkzeug.exceptions import BadRequest
from service import app, api
from service.models import Customer, DataValidationError
from . import CustomerResource

class CustomerCollection(Resource):
    """ Handles all interactions with collections of Customers """

    def get(self):
        """ Returns all of the Customers """
        app.logger.info('Request to list Customers...')
        customers = []
        email = request.args.get('email')
        firstname = request.args.get('firstname')
        lastname = request.args.get('lastname')
        subscribed = request.args.get('subscribed')
        address1 = request.args.get('address1')
        address2 = request.args.get('address2')
        city = request.args.get('city')
        province = request.args.get('province')
        country = request.args.get('country')
        zip = request.args.get('zip')

        if email:
            customers = Customer.find_by_email(email)
        elif firstname:
            customers = Customer.find_by_first_name(firstname)
        elif lastname:
            customers = Customer.find_by_last_name(lastname)
        elif subscribed:
            customers = Customer.find_by_subscribed(subscribed.lower() in ('true', '1'))
        elif address1:
            customers = Customer.find_by_address1(address1)
        elif address2:
            customers = Customer.find_by_address2(address2)
        elif city:
            customers = Customer.find_by_city(city)
        elif province:
            customers = Customer.find_by_province(province)
        elif country:
            customers = Customer.find_by_country(country)
        elif zip:
            customers = Customer.find_by_zip(zip)
        else:
            customers = Customer.all()

        app.logger.info('[%s] Customers returned', len(customers))
        results = [customer.serialize() for customer in customers]
        return results, status.HTTP_200_OK

    def post(self):
        """
        Creates a Customer

        This endpoint will create a Customer based the data in the body that is posted
        or data that is sent via an html form post.
        """
        app.logger.info('Request to Create a Customer')
        content_type = request.headers.get('Content-Type')
        if not content_type:
            abort(status.HTTP_400_BAD_REQUEST, "No Content-Type set")

        data = {}
        if content_type == 'application/x-www-form-urlencoded':
            app.logger.info('Processing FORM data')
            app.logger.info(type(request.form))
            app.logger.info(request.form)
            data = {
                'firstname': request.form['firstname'],
                'lastname': request.form['lastname'],
                'email': request.form['email'],
                'subscribed': False if request.form['subscribed'] == "false" else True,
                'address': {
                    'province': request.form['province'],
                    'city': request.form['city'],
                    'zip': request.form['zip'],
                    'address1': request.form['address1'],
                    'address2': request.form['address2'],
                    'country': request.form['country']
                }
            }
        elif content_type == 'application/json':
            app.logger.info('Processing JSON data')
            data = request.get_json()

        else:
            message = 'Unsupported Content-Type: {}'.format(content_type)
            app.logger.info(message)
            abort(status.HTTP_400_BAD_REQUEST, message)

        customer = Customer()
        try:
            customer.deserialize(data)
        except DataValidationError as error:
            raise BadRequest(str(error))
        customer.save()
        app.logger.info('Customer with new id [%s] saved!', customer.id)
        location_url = api.url_for(CustomerResource, customer_id=customer.id, _external=True)
        return customer.serialize(), status.HTTP_201_CREATED, {'Location': location_url}
