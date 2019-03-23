"""
Customer API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
  codecov --token=$CODECOV_TOKEN
"""

import unittest
import os
import logging
from flask_api import status    # HTTP Status Codes
#from mock import MagicMock, patch
from app.models import Customer, DataValidationError, db
from .customer_factory import CustomerFactory
import app.service as service

DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///../db/test.db')

######################################################################
#  T E S T   C A S E S
######################################################################


class TestCustomerServer(unittest.TestCase):
    """ Customer Server Tests """

    @classmethod
    def setUpClass(cls):
        """ Run once before all tests """
        service.app.debug = False
        service.initialize_logging(logging.INFO)
        # Set up the test database
        service.app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        """ Runs before each test """
        service.init_db()
        db.drop_all()    # clean up the last tests
        db.create_all()  # create new tables
        self.app = service.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def _create_customers(self, count):
        """ Factory method to create customers in bulk """
        customers = []
        for _ in range(count):
            test_customer = CustomerFactory()
            resp = self.app.post('/customers',
                                 json=test_customer.serialize(),
                                 content_type='application/json')
            self.assertEqual(resp.status_code, status.HTTP_201_CREATED,
                             'Could not create test customer')
            new_customer = resp.get_json()
            test_customer.id = new_customer['id']
            customers.append(test_customer)
        return customers

    def test_index(self):
        """ Test the Home Page """
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data['name'], 'Customer Demo REST API Service')

    def test_get_customer_list(self):
        """ Get a list of Customers """
        self._create_customers(5)
        resp = self.app.get('/customers')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)

    def test_get_customer(self):
        """ Get a single Customer """
        # get the id of a customer
        test_customer = self._create_customers(1)[0]
        resp = self.app.get('/customers/{}'.format(test_customer.id),
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data['firstname'], test_customer.firstname)

    def test_get_customer_not_found(self):
        """ Get a Customer thats not found """
        resp = self.app.get('/customers/0')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_customer(self):
        """ Create a new Customer """
        test_customer = CustomerFactory()
        resp = self.app.post('/customers',
                             json=test_customer.serialize(),
                             content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get('Location', None)
        self.assertTrue(location != None)
        # Check the data is correct
        new_customer = resp.get_json()
        self.assertEqual(new_customer['firstname'], test_customer.firstname, "First name does not match")
        self.assertEqual(new_customer['lastname'], test_customer.lastname, "Last name does not match")
        self.assertEqual(new_customer['email'], test_customer.email, "Emails do not match")
        self.assertEqual(new_customer['subscribed'], test_customer.subscribed, "Subscribed does not match")
        self.assertEqual(new_customer['address']['address1'], test_customer.address1, "Address1 do not match")
        self.assertEqual(new_customer['address']['address2'], test_customer.address2, "Address2 do not match")
        self.assertEqual(new_customer['address']['city'], test_customer.city, "City do not match")
        self.assertEqual(new_customer['address']['province'], test_customer.province, "Province do not match")
        self.assertEqual(new_customer['address']['country'], test_customer.country, "Country do not match")
        self.assertEqual(new_customer['address']['zip'], test_customer.zip, "Zip do not match")

        # Check that the location header was correct
        resp = self.app.get(location,
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_customer = resp.get_json()
        self.assertEqual(new_customer['firstname'], test_customer.firstname, "First name does not match")
        self.assertEqual(new_customer['lastname'], test_customer.lastname, "Last name does not match")
        self.assertEqual(new_customer['email'], test_customer.email, "Emails do not match")
        self.assertEqual(new_customer['subscribed'], test_customer.subscribed, "Subscribed does not match")
        self.assertEqual(new_customer['address']['address1'], test_customer.address1, "Address1 do not match")
        self.assertEqual(new_customer['address']['address2'], test_customer.address2, "Address2 do not match")
        self.assertEqual(new_customer['address']['city'], test_customer.city, "City do not match")
        self.assertEqual(new_customer['address']['province'], test_customer.province, "Province do not match")
        self.assertEqual(new_customer['address']['country'], test_customer.country, "Country do not match")
        self.assertEqual(new_customer['address']['zip'], test_customer.zip, "Zip do not match")

    def test_update_customer_name(self):
        """ Update an existing Customer """
        # create a customer to update
        test_customer = CustomerFactory()
        resp = self.app.post('/customers',
                             json=test_customer.serialize(),
                             content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the customer
        new_customer = resp.get_json()
        new_customer['firstname'] = 'Isabel'
        resp = self.app.put('/customers/{}'.format(new_customer['id']),
                            json=new_customer,
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_customer = resp.get_json()
        self.assertEqual(updated_customer['firstname'], 'Isabel')

    def test_update_customer_email(self):
        """ Update an existing Customer email """
        # create a customer to update
        test_customer = CustomerFactory()
        resp = self.app.post('/customers',
                             json=test_customer.serialize(),
                             content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the customer
        new_customer = resp.get_json()
        new_customer['email'] = 'ethan@gmail.com'
        resp = self.app.put('/customers/{}'.format(new_customer['id']),
                            json=new_customer,
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_customer = resp.get_json()
        self.assertEqual(updated_customer['email'], 'ethan@gmail.com')

    def test_update_customer_email_and_name(self):
        """ Update an existing Customer email and name """
        # create a customer to update
        test_customer = CustomerFactory()
        resp = self.app.post('/customers',
                             json=test_customer.serialize(),
                             content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the customer
        new_customer = resp.get_json()
        new_customer['email'] = 'anthony@gmail.com'
        new_customer['firstname'] = 'Ted'
        resp = self.app.put('/customers/{}'.format(new_customer['id']),
                            json=new_customer,
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_customer = resp.get_json()
        self.assertEqual(updated_customer['email'], 'anthony@gmail.com')
        self.assertEqual(updated_customer['firstname'], 'Ted')

    def test_delete_pet(self):
        """ Delete a Customer """
        test_customer = self._create_customers(1)[0]
        resp = self.app.delete('/customers/{}'.format(test_customer.id),
                               content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        # make sure they are deleted
        resp = self.app.get('/customers/{}'.format(test_customer.id),
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_query_pet_list_by_category(self):
        """ Query Customer by Email """
        customers = self._create_customers(10)
        test_email = customers[0].email
        email_customers = [customer for customer in customers if customer.email == test_email]
        resp = self.app.get('/customers',
                            query_string='email={}'.format(test_email))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(email_customers))
        # check the data just to be sure
        for customer in data:
            self.assertEqual(customer['email'], test_email)

    # @patch('app.service.Pet.find_by_name')
    # def test_bad_request(self, bad_request_mock):
    #     """ Test a Bad Request error from Find By Name """
    #     bad_request_mock.side_effect = DataValidationError()
    #     resp = self.app.get('/pets', query_string='name=fido')
    #     self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
    #
    # @patch('app.service.Pet.find_by_name')
    # def test_mock_search_data(self, pet_find_mock):
    #     """ Test showing how to mock data """
    #     pet_find_mock.return_value = [MagicMock(serialize=lambda: {'name': 'fido'})]
    #     resp = self.app.get('/pets', query_string='name=fido')
    #     self.assertEqual(resp.status_code, status.HTTP_200_OK)


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
