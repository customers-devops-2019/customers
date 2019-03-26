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
        self.assertEqual(new_customer['firstname'], test_customer.firstname,
                         "First name does not match")
        self.assertEqual(new_customer['lastname'], test_customer.lastname,
                         "Last name does not match")
        self.assertEqual(new_customer['email'], test_customer.email,
                         "Emails do not match")
        self.assertEqual(new_customer['subscribed'], test_customer.subscribed,
                         "Subscribed does not match")
        self.assertEqual(new_customer['address']['address1'], test_customer.address1,
                         "Address1 do not match")
        self.assertEqual(new_customer['address']['address2'], test_customer.address2,
                         "Address2 do not match")
        self.assertEqual(new_customer['address']['city'], test_customer.city,
                         "City do not match")
        self.assertEqual(new_customer['address']['province'], test_customer.province,
                         "Province do not match")
        self.assertEqual(new_customer['address']['country'], test_customer.country,
                         "Country do not match")
        self.assertEqual(new_customer['address']['zip'], test_customer.zip,
                         "Zip do not match")

        # Check that the location header was correct
        resp = self.app.get(location,
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_customer = resp.get_json()
        self.assertEqual(new_customer['firstname'], test_customer.firstname,
                         "First name does not match")
        self.assertEqual(new_customer['lastname'], test_customer.lastname,
                         "Last name does not match")
        self.assertEqual(new_customer['email'], test_customer.email,
                         "Emails do not match")
        self.assertEqual(new_customer['subscribed'], test_customer.subscribed,
                         "Subscribed does not match")
        self.assertEqual(new_customer['address']['address1'], test_customer.address1,
                         "Address1 do not match")
        self.assertEqual(new_customer['address']['address2'], test_customer.address2,
                         "Address2 do not match")
        self.assertEqual(new_customer['address']['city'], test_customer.city,
                         "City do not match")
        self.assertEqual(new_customer['address']['province'], test_customer.province,
                         "Province do not match")
        self.assertEqual(new_customer['address']['country'], test_customer.country,
                         "Country do not match")
        self.assertEqual(new_customer['address']['zip'], test_customer.zip,
                         "Zip do not match")

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

    def test_delete_customer(self):
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

    def test_unsubscribe_customer(self):
        """ Unsubscribe an existing Customer """
        # create a customer
        test_customer = CustomerFactory()
        test_customer = test_customer.serialize()
        # set subscribed to true
        test_customer["subscribed"] = True
        resp = self.app.post('/customers',
                             json=test_customer,
                             content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the customer
        new_customer = resp.get_json()
        resp = self.app.put('/customers/{}/unsubscribe'.format(new_customer['id']),
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_customer = resp.get_json()
        self.assertEqual(updated_customer['subscribed'], False)

    def test_get_address(self):
        """ Get a address of Customer """
        # get the id of a customer
        test_customer = self._create_customers(1)[0]
        resp = self.app.get('/customers/{}/address'.format(test_customer.id),
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        test_obj = test_customer.serialize()
        self.assertEqual(data, test_obj["address"])

    def test_query_customer_list_email(self):
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

    def test_query_customer_list_fname(self):
        """ Query Customer by First name """
        customers = self._create_customers(10)
        test_firstname = customers[0].firstname
        firstname_customers = [customer for customer in customers
                               if customer.firstname == test_firstname]
        resp = self.app.get('/customers',
                            query_string='firstname={}'.format(test_firstname))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(firstname_customers))
        # check the data just to be sure
        for customer in data:
            self.assertEqual(customer['firstname'], test_firstname)

    def test_query_customer_list_lname(self):
        """ Query Customer by Last name """
        customers = self._create_customers(10)
        test_lastname = customers[0].lastname
        lastname_customers = [customer for customer in customers
                              if customer.lastname == test_lastname]
        resp = self.app.get('/customers',
                            query_string='lastname={}'.format(test_lastname))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(lastname_customers))
        # check the data just to be sure
        for customer in data:
            self.assertEqual(customer['lastname'], test_lastname)

    def test_query_customer_list_sub(self):
        """ Query Customer by Subscribed """
        customers = self._create_customers(10)
        test_subscribed = customers[0].subscribed
        print("the subscribed output is  %s", test_subscribed)
        subscribed_customers = [customer for customer in customers
                                if customer.subscribed == test_subscribed]
        resp = self.app.get('/customers',
                            query_string='subscribed={}'.format(test_subscribed))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(subscribed_customers))
        # check the data just to be sure
        for customer in data:
            self.assertEqual(customer['subscribed'], test_subscribed)

    def test_query_customer_list_addr1(self):
        """ Query Customer by Address 1 """
        customers = self._create_customers(10)
        test_a1 = customers[0].address1
        a1_customers = [customer for customer in customers if customer.address1 == test_a1]
        resp = self.app.get('/customers',
                            query_string='address1={}'.format(test_a1))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(a1_customers))
        # check the data just to be sure
        for customer in data:
            self.assertEqual(customer['address']['address1'], test_a1)

    def test_query_customer_list_addr2(self):
        """ Query Customer by Address 2 """
        customers = self._create_customers(10)
        test_a2 = customers[0].address2
        a2_customers = [customer for customer in customers if customer.address2 == test_a2]
        resp = self.app.get('/customers',
                            query_string='address2={}'.format(test_a2))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(a2_customers))
        # check the data just to be sure
        for customer in data:
            self.assertEqual(customer['address']['address2'], test_a2)

    def test_query_customer_list_city(self):
        """ Query Customer by City """
        customers = self._create_customers(10)
        test_city = customers[0].city
        city_customers = [customer for customer in customers if customer.city == test_city]
        resp = self.app.get('/customers',
                            query_string='city={}'.format(test_city))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(city_customers))
        # check the data just to be sure
        for customer in data:
            self.assertEqual(customer['address']['city'], test_city)

    def test_query_customer_list_prov(self):
        """ Query Customer by Province """
        customers = self._create_customers(10)
        test_province = customers[0].province
        province_customers = [customer for customer in customers
                              if customer.province == test_province]
        resp = self.app.get('/customers',
                            query_string='province={}'.format(test_province))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(province_customers))
        # check the data just to be sure
        for customer in data:
            self.assertEqual(customer['address']['province'], test_province)

    def test_query_customer_list_country(self):
        """ Query Customer by Country """
        customers = self._create_customers(10)
        test_country = customers[0].country
        country_customers = [customer for customer in customers if customer.country == test_country]
        resp = self.app.get('/customers',
                            query_string='country={}'.format(test_country))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(country_customers))
        # check the data just to be sure
        for customer in data:
            self.assertEqual(customer['address']['country'], test_country)

    def test_query_customer_list_zip(self):
        """ Query Customer by Zip """
        customers = self._create_customers(10)
        test_zi = customers[0].zip
        zi_customers = [customer for customer in customers if customer.zip == test_zi]
        resp = self.app.get('/customers',
                            query_string='zip={}'.format(test_zi))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(zi_customers))
        # check the data just to be sure
        for customer in data:
            self.assertEqual(customer['address']['zip'], test_zi)

    def test_method_not_allowed(self):
        """ Test Error Method Not Allowed """
        resp = self.app.get('/customers/1/unsubscribe')
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_resource_not_found(self):
        """ Test Error Not Found """
        resp = self.app.get('/customers/10')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_resource_not_found_update(self):
        """ Test Error Update Not Found """
        # create a customer to update
        test_customer = CustomerFactory()
        resp = self.app.put('/customers/10',
                            json=test_customer.serialize(),
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_server_error(self):
        """ Test Server Error """
        # create a customer to update
        test_customer = CustomerFactory()
        resp = self.app.post('/customers',
                             json=test_customer.serialize(),
                             content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the customer
        new_customer = resp.get_json()
        new_customer['subscribed'] = "Hello"
        resp = self.app.put('/customers/{}'.format(new_customer['id']),
                            json=new_customer,
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

        def test_bad_request(self):
            """ Test Error Bad Request """
            # create a customer to update
            test_customer = CustomerFactory()
            resp = self.app.post('/customers',
                                 json=test_customer.serialize(),
                                 content_type='application/json')
            self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

            # update the customer
            new_customer = resp.get_json()
            resp = self.app.put('/customers/{}'.format(new_customer['id']),
                                json=10,
                                content_type='application/json')
            self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        def test_unsupported_media_type(self):
            """ Test Unsupported Media Type Error """
            # create a customer to update
            test_customer = CustomerFactory()
            resp = self.app.post('/customers',
                                 json=test_customer.serialize(),
                                 content_type='application/json')
            self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

            # update the customer
            new_customer = resp.get_json()
            new_customer['subscribed'] = True
            resp = self.app.put('/customers/{}'.format(new_customer['id']),
                                json=new_customer,
                                content_type='application/zip')
            self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
