"""
Customer API Service Test Suite

Test cases can be run with the following:
nosetests -v --with-spec --spec-color
"""

import unittest
import json
from werkzeug.datastructures import MultiDict, ImmutableMultiDict
from service import app
from .customer_factory import CustomerFactory
from service.models import Customer

# Status Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_405_METHOD_NOT_ALLOWED = 405
HTTP_409_CONFLICT = 409

######################################################################
#  T E S T   C A S E S
######################################################################


class TestCustomerServer(unittest.TestCase):
    """ Test Cases for Customer Server """

    def setUp(self):
        """ Initialize the Cloudant database """
        self.app = app.test_client()
        Customer.init_db("tests")
        Customer.remove_all()

    def _create_customers(self, count):
        """ Factory method to create customers in bulk """
        customers = []
        for _ in range(count):
            test_customer = CustomerFactory()
            resp = self.app.post('/customers',
                                 json=test_customer.serialize(),
                                 content_type='application/json')
            self.assertEqual(resp.status_code, HTTP_201_CREATED,
                             'Could not create test customer')
            new_customer = resp.get_json()
            test_customer._id = new_customer['_id']
            customers.append(test_customer)
        return customers

    def test_index(self):
        """ Test the Home Page """
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, HTTP_200_OK)
        data = resp.get_json()
        self.assertIn('Customer Demo REST API Service', resp.data)

    def test_get_customer_list(self):
        """ Get a list of Customers """
        self._create_customers(5)
        resp = self.app.get('/customers')
        self.assertEqual(resp.status_code, HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)

    def test_get_customer(self):
        """ Get a single Customer """
        # get the _id of a customer
        test_customer = self._create_customers(1)[0]
        resp = self.app.get('/customers/{}'.format(test_customer._id),
                            content_type='application/json')
        self.assertEqual(resp.status_code, HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data['firstname'], test_customer.firstname)

    def test_get_customer_not_found(self):
        """ Get a Customer thats not found """
        resp = self.app.get('/customers/0')
        self.assertEqual(resp.status_code, HTTP_404_NOT_FOUND)

    def test_create_customer(self):
        """ Create a new Customer """
        test_customer = CustomerFactory()
        resp = self.app.post('/customers',
                             json=test_customer.serialize(),
                             content_type='application/json')
        self.assertEqual(resp.status_code, HTTP_201_CREATED)
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
        self.assertEqual(resp.status_code, HTTP_200_OK)
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
        self.assertEqual(resp.status_code, HTTP_201_CREATED)

        # update the customer
        new_customer = resp.get_json()
        new_customer['firstname'] = 'Isabel'
        resp = self.app.put('/customers/{}'.format(new_customer['_id']),
                            json=new_customer,
                            content_type='application/json')
        self.assertEqual(resp.status_code, HTTP_200_OK)
        updated_customer = resp.get_json()
        self.assertEqual(updated_customer['firstname'], 'Isabel')

    def test_update_customer_email(self):
        """ Update an existing Customer email """
        # create a customer to update
        test_customer = CustomerFactory()
        resp = self.app.post('/customers',
                             json=test_customer.serialize(),
                             content_type='application/json')
        self.assertEqual(resp.status_code, HTTP_201_CREATED)

        # update the customer
        new_customer = resp.get_json()
        new_customer['email'] = 'ethan@gmail.com'
        resp = self.app.put('/customers/{}'.format(new_customer['_id']),
                            json=new_customer,
                            content_type='application/json')
        self.assertEqual(resp.status_code, HTTP_200_OK)
        updated_customer = resp.get_json()
        self.assertEqual(updated_customer['email'], 'ethan@gmail.com')

    def test_update_customer_email_and_name(self):
        """ Update an existing Customer email and name """
        # create a customer to update
        test_customer = CustomerFactory()
        resp = self.app.post('/customers',
                             json=test_customer.serialize(),
                             content_type='application/json')
        self.assertEqual(resp.status_code, HTTP_201_CREATED)

        # update the customer
        new_customer = resp.get_json()
        new_customer['email'] = 'anthony@gmail.com'
        new_customer['firstname'] = 'Ted'
        resp = self.app.put('/customers/{}'.format(new_customer['_id']),
                            json=new_customer,
                            content_type='application/json')
        self.assertEqual(resp.status_code, HTTP_200_OK)
        updated_customer = resp.get_json()
        self.assertEqual(updated_customer['email'], 'anthony@gmail.com')
        self.assertEqual(updated_customer['firstname'], 'Ted')

    def test_delete_customer(self):
        """ Delete a Customer """
        test_customer = self._create_customers(1)[0]
        resp = self.app.delete('/customers/{}'.format(test_customer._id),
                               content_type='application/json')
        self.assertEqual(resp.status_code, HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        # make sure they are deleted
        resp = self.app.get('/customers/{}'.format(test_customer._id),
                            content_type='application/json')
        self.assertEqual(resp.status_code, HTTP_404_NOT_FOUND)

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
        self.assertEqual(resp.status_code, HTTP_201_CREATED)

        # update the customer
        new_customer = resp.get_json()
        resp = self.app.put('/customers/{}/unsubscribe'.format(new_customer['_id']),
                            content_type='application/json')
        self.assertEqual(resp.status_code, HTTP_200_OK)
        updated_customer = resp.get_json()
        self.assertEqual(updated_customer['subscribed'], False)

    def test_get_address(self):
        """ Get a address of Customer """
        # get the _id of a customer
        test_customer = self._create_customers(1)[0]
        resp = self.app.get('/customers/{}/address'.format(test_customer._id),
                            content_type='application/json')
        self.assertEqual(resp.status_code, HTTP_200_OK)
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
        self.assertEqual(resp.status_code, HTTP_200_OK)
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
        self.assertEqual(resp.status_code, HTTP_200_OK)
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
        self.assertEqual(resp.status_code, HTTP_200_OK)
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
        self.assertEqual(resp.status_code, HTTP_200_OK)
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
        self.assertEqual(resp.status_code, HTTP_200_OK)
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
        self.assertEqual(resp.status_code, HTTP_200_OK)
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
        self.assertEqual(resp.status_code, HTTP_200_OK)
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
        self.assertEqual(resp.status_code, HTTP_200_OK)
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
        self.assertEqual(resp.status_code, HTTP_200_OK)
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
        self.assertEqual(resp.status_code, HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(zi_customers))
        # check the data just to be sure
        for customer in data:
            self.assertEqual(customer['address']['zip'], test_zi)

    def test_method_not_allowed(self):
        """ Test Error Method Not Allowed """
        resp = self.app.get('/customers/1/unsubscribe')
        self.assertEqual(resp.status_code, HTTP_405_METHOD_NOT_ALLOWED)

    def test_resource_not_found(self):
        """ Test Error Not Found """
        resp = self.app.get('/customers/10')
        self.assertEqual(resp.status_code, HTTP_404_NOT_FOUND)

    def test_resource_not_found_update(self):
        """ Test Error Update Not Found """
        # create a customer to update
        test_customer = CustomerFactory()
        resp = self.app.put('/customers/10',
                            json=test_customer.serialize(),
                            content_type='application/json')
        self.assertEqual(resp.status_code, HTTP_404_NOT_FOUND)

    def test_bad_request(self):
        """ Test Error Bad Request """
        # create a customer to update
        test_customer = CustomerFactory()
        resp = self.app.post('/customers',
                             json=test_customer.serialize(),
                             content_type='application/json')
        self.assertEqual(resp.status_code, HTTP_201_CREATED)

        # update the customer
        new_customer = resp.get_json()
        resp = self.app.put('/customers/{}'.format(new_customer['_id']),
                            json=10,
                            content_type='application/json')
        self.assertEqual(resp.status_code, HTTP_400_BAD_REQUEST)

    def test_create_customer_no_content_type(self):
        """ Create a customer with no Content-Type """
        new_customer = {'firstname': 'Sammy', 'lastname': 'Woods', 'email': 'snake@hotmail.com',
                        'address1': '12 Main st', 'address2': '3', 'city': 'Denver',
                        'country': 'Canada', 'province': 'NY', 'zip': '80290'}
        data = json.dumps(new_customer)
        resp = self.app.post('/customers', data=data)
        self.assertEqual(resp.status_code, HTTP_400_BAD_REQUEST)

    def test_create_customer_wrong_content_type(self):
        """ Create a Customer with wrong Content-Type """
        data = "Isabel the Ecuadorian"
        resp = self.app.post('/customers', data=data, content_type='plain/text')
        self.assertEqual(resp.status_code, HTTP_400_BAD_REQUEST)


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
