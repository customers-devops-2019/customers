# Copyright 2016, 2017 John Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Customer Model that uses Cloudant

You must initlaize this class before use by calling inititlize().
This class looks for an environment variable called VCAP_SERVICES
to get it's database credentials from. If it cannot find one, it
tries to connect to Cloudant on the localhost. If that fails it looks
for a server name 'cloudant' to connect to.

To use with Docker couchdb database use:
    docker run -d --name couchdb -p 5984:5984 -e COUCHDB_USER=admin -e COUCHDB_PASSWORD=pass couchdb

Docker Note:
    CouchDB uses /opt/couchdb/data to store its data, and is exposed as a volume
    e.g., to use current folder add: -v $(pwd):/opt/couchdb/data
    You can also use Docker volumes like this: -v couchdb_data:/opt/couchdb/data
"""
import os
import json
import logging
from retry import retry
from cloudant.client import Cloudant
from cloudant.query import Query
from requests import HTTPError, ConnectionError

# get configruation from enviuronment (12-factor)
ADMIN_PARTY = os.environ.get('ADMIN_PARTY', 'False').lower() == 'true'
CLOUDANT_HOST = os.environ.get('CLOUDANT_HOST', 'localhost')
CLOUDANT_USERNAME = os.environ.get('CLOUDANT_USERNAME', 'admin')
CLOUDANT_PASSWORD = os.environ.get('CLOUDANT_PASSWORD', 'pass')

class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    pass


class Customer(object):
    """
    Class that represents a Customer
    """
    logger = logging.getLogger(__name__)
    client = None   # cloudant.client.Cloudant
    database = None # cloudant.database.CloudantDatabase

    def __init__(self, firstname=None, lastname=None, email=None, address1=None, address2=None, city=None, province=None, country=None, zip=None, subscribed=True):
        """ Constructor """
        self.id = None
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.address1 = address1
        self.address2 = address2
        self.city = city
        self.province = province
        self.country = country
        self.zip = zip
        self.subscribed = subscribed

    @retry(HTTPError, delay=1, backoff=2, tries=5)
    def create(self):
        """
        Creates a Customer in the database
        """
        if self.firstname is None:
            raise DataValidationError('firstName attribute is not set')
        try:
            document = self.database.create_document(self.serialize())
        except HTTPError as err:
            Customer.logger.warning('Create failed: %s', err)
            return

        if document.exists():
            self.id = document['_id']

    @retry(HTTPError, delay=1, backoff=2, tries=5)
    def update(self):
        """
        Updates a Customer in the database
        """
        try:
            document = self.database[self.id]
        except KeyError:
            document = None
        if document:
            document.update(self.serialize())
            document.save()

    @retry(HTTPError, delay=1, backoff=2, tries=5)
    def save(self):
        """
        Saves a Customer to the data store
        """
        if self.firstname is None:
            raise DataValidationError('firstName attribute is not set')
        if self.id:
            self.update()
        else:
            self.create()

    @retry(HTTPError, delay=1, backoff=2, tries=5)
    def delete(self):
        """ Removes a Customer from the data store """
        try:
            document = self.database[self.id]
        except KeyError:
            document = None
        if document:
            document.delete()

    def serialize(self):
        """ Serializes a Customer into a dictionary """
        customer = {
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "subscribed": self.subscribed,
            "address": {
                "address1": self.address1,
                "address2": self.address2,
                "city": self.city,
                "province": self.province,
                "country": self.country,
                "zip": self.zip
            }}
        if self.id:
            customer['_id'] = self.id
        return customer

    def deserialize(self, data):
        """
        Deserializes a Customer from a dictionary

        Args:
            data (dict): A dictionary containing the Customer data
        """
        try:
            self.firstname = data['firstname']
            self.lastname = data['lastname']
            self.email = data['email']
            self.subscribed = data['subscribed']
            self.address1 = data['address']['address1']
            self.address2 = data['address']['address2']
            self.city = data['address']['city']
            self.province = data['address']['province']
            self.country = data['address']['country']
            self.zip = data['address']['zip']
        except KeyError as error:
            raise DataValidationError('Invalid customer: missing ' + error.args[0])
        except TypeError as error:
            raise DataValidationError('Invalid customer: body of request contained'
                                      'bad or no data')
        if not self.id and '_id' in data:
            self.id = data['_id']

        return self

######################################################################
#  S T A T I C   D A T A B S E   M E T H O D S
######################################################################

    @classmethod
    def connect(cls):
        """ Connect to the server """
        cls.client.connect()

    @classmethod
    def disconnect(cls):
        """ Disconnect from the server """
        cls.client.disconnect()

    @classmethod
    @retry(HTTPError, delay=1, backoff=2, tries=5)
    def create_query_index(cls, field_name, order='asc'):
        """ Creates a new query index for searching """
        cls.database.create_query_index(index_name=field_name, fields=[{field_name: order}])

    @classmethod
    @retry(HTTPError, delay=1, backoff=2, tries=5)
    def remove_all(cls):
        """ Removes all documents from the database (use for testing)  """
        for document in cls.database:
            document.delete()

    @classmethod
    @retry(HTTPError, delay=1, backoff=2, tries=5)
    def all(cls):
        """ Query that returns all Customers """
        results = []
        for doc in cls.database:
            customer = Customer().deserialize(doc)
            customer.id = doc['_id']
            results.append(customer)
        return results

######################################################################
#  F I N D E R   M E T H O D S
######################################################################

    @classmethod
    @retry(HTTPError, delay=1, backoff=2, tries=5)
    def find_by(cls, **kwargs):
        """ Find records using selector """
        query = Query(cls.database, selector=kwargs)
        results = []
        for doc in query.result:
            customer = Customer()
            customer.deserialize(doc)
            results.append(customer)
        return results

    @classmethod
    @retry(HTTPError, delay=1, backoff=2, tries=5)
    def find(cls, customer_id):
        """ Query that finds Customers by their ID """
        try:
            document = cls.database[customer_id]
            if 'firstname' in document:
                return Customer().deserialize(document)
            else :
                return None
        except KeyError:
            return None

    @classmethod
    def find_by_first_name(cls, firstname):
        """ Returns all Customers with the given first name
        """
        return cls.find_by(firstname=firstname)

    @classmethod
    def find_by_last_name(cls, lastname):
        """ Returns all Customers with the given last name
        """
        return cls.find_by(lastname=lastname)

    @classmethod
    def find_by_email(cls, email):
        """ Returns all of the Customers with a email
        """
        return cls.find_by(email=email)

    @classmethod
    def find_by_subscribed(cls,flag):
        """ Returns all of the Customers who are subscribed
        """
        return cls.find_by(subscribed=flag)

    @classmethod
    def find_by_address1(cls, address1):
        """ Returns all of the Customers with a address1
        """
        sel = {
           "address1": address1
        }
        return cls.find_by(address=sel)

    @classmethod
    def find_by_address2(cls, address2):
        """ Returns all of the Customers with a address2
        """
        sel = {
           "address2": address2
        }
        return cls.find_by(address=sel)

    @classmethod
    def find_by_email(cls, email):
        """ Returns all of the Customers with a email
        """
        return cls.find_by(email=email)

    @classmethod
    def find_by_city(cls, city):
        """ Returns all of the Customers with a city
        """
        sel = {
           "city": city
        }
        return cls.find_by(address=sel)

    @classmethod
    def find_by_province(cls, province):
        """ Returns all of the Customers with a province
        """
        sel = {
           "province": province
        }
        return cls.find_by(address=sel)

    @classmethod
    def find_by_country(cls, country):
        """ Returns all of the Customers with a country
        """
        sel = {
           "country": country
        }
        return cls.find_by(address=sel)

    @classmethod
    def find_by_zip(cls, zip):
        """ Returns all of the Customers with a zip
        """
        sel = {
           "zip": zip
        }
        return cls.find_by(address=sel)

############################################################
#  C L O U D A N T   D A T A B A S E   C O N N E C T I O N
############################################################

    @staticmethod
    def init_db(dbname='customers'):
        """
        Initialized Coundant database connection
        """
        opts = {}
        vcap_services = {}
        # Try and get VCAP from the environment or a file if developing
         if 'BINDING_CLOUDANT' in os.environ:
            Pet.logger.info('Found Kubernetes Bindings')
            creds = json.loads(os.environ['BINDING_CLOUDANT'])
            vcap_services = {"cloudantNoSQLDB": [{"credentials": creds}]}
        else:
            Customer.logger.info('VCAP_SERVICES and BINDING_CLOUDANT undefined.')
            creds = {
                "username": CLOUDANT_USERNAME,
                "password": CLOUDANT_PASSWORD,
                "host": CLOUDANT_HOST,
                "port": 5984,
                "url": "http://"+CLOUDANT_HOST+":5984/"
            }
            vcap_services = {"cloudantNoSQLDB": [{"credentials": creds}]}

        # Look for Cloudant in VCAP_SERVICES
        for service in vcap_services:
            if service.startswith('cloudantNoSQLDB'):
                cloudant_service = vcap_services[service][0]
                opts['username'] = cloudant_service['credentials']['username']
                opts['password'] = cloudant_service['credentials']['password']
                opts['host'] = cloudant_service['credentials']['host']
                opts['port'] = cloudant_service['credentials']['port']
                opts['url'] = cloudant_service['credentials']['url']

        if any(k not in opts for k in ('host', 'username', 'password', 'port', 'url')):
            Customer.logger.info('Error - Failed to retrieve options. ' \
                             'Check that app is bound to a Cloudant service.')
            exit(-1)

        Customer.logger.info('Cloudant Endpoint: %s', opts['url'])
        try:
            if ADMIN_PARTY:
                Customer.logger.info('Running in Admin Party Mode...')
            Customer.client = Cloudant(opts['username'],
                                  opts['password'],
                                  url=opts['url'],
                                  connect=True,
                                  auto_renew=True,
                                  admin_party=ADMIN_PARTY
                                 )
        except ConnectionError:
            raise AssertionError('Cloudant service could not be reached')

        # Create database if it doesn't exist
        try:
            Customer.database = Customer.client[dbname]
        except KeyError:
            # Create a database using an initialized client
            Customer.database = Customer.client.create_database(dbname)
        # check for success
        if not Customer.database.exists():
            raise AssertionError('Database [{}] could not be obtained'.format(dbname))
