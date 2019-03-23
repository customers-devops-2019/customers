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
Models for Customer Demo Service

All of the models are stored in this module

Models
------
Customer - A Customer who buys online

Attributes:
-----------
firstname (string) - the first name of the customer
lastname (string) - the last name of the customer
email (string) - the email
subscribed (boolean) - is customer subscribed
address1 (string) - the address1
address2 (string) - the address2
city (string) - the city
province (string) - the province
country (string) - the country
zip (string) - the zip code

"""
import logging
from flask_sqlalchemy import SQLAlchemy

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    pass


class Customer(db.Model):
    """
    Class that represents a Customer

    This version uses a relational database for persistence which is hidden
    from us by SQLAlchemy's object relational mappings (ORM)
    """
    logger = logging.getLogger(__name__)
    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(63))
    lastname = db.Column(db.String(63))
    email = db.Column(db.String(63))
    address1 = db.Column(db.String(63))
    address2 = db.Column(db.String(63))
    city = db.Column(db.String(63))
    province = db.Column(db.String(63))
    country = db.Column(db.String(63))
    zip = db.Column(db.String(63))
    subscribed = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return '<Customer %r>' % (self.name)

    def save(self):
        """
        Saves a Customer to the data store
        """
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        """ Removes a Customer from the data store """
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a Customer into a dictionary """
        return {
            "id": self.id,
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
        return self

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        cls.logger.info('Initializing database')
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the Customers in the database """
        cls.logger.info('Processing all Customers')
        return cls.query.all()

    @classmethod
    def find(cls, customer_id):
        """ Finds a Customer by it's ID """
        cls.logger.info('Processing lookup for id %s ...', customer_id)
        return cls.query.get(customer_id)

    @classmethod
    def find_or_404(cls, customer_id):
        """ Find a Customer by it's id """
        cls.logger.info('Processing lookup or 404 for id %s ...', customer_id)
        return cls.query.get_or_404(customer_id)

    @classmethod
    def find_by_first_name(cls, firstname):
        """ Returns all Customers with the given first name

        Args:
            firstname (string): the first name of the Customers you want to match
        """
        cls.logger.info('Processing first name query for %s ...', firstname)
        return cls.query.filter(cls.firstname == firstname)

    @classmethod
    def find_by_last_name(cls, lastname):
        """ Returns all Customers with the given last name

        Args:
            lastname (string): the last name of the Customers you want to match
        """
        cls.logger.info('Processing last name query for %s ...', lastname)
        return cls.query.filter(cls.lastname == lastname)

    @classmethod
    def find_by_email(cls, email):
        """ Returns all of the Customers with a email

        Args:
            email (string): the email of the Customer you want to match
        """
        cls.logger.info('Processing email query for %s ...', email)
        return cls.query.filter(cls.email == email)

    @classmethod
    def find_by_subscribed(cls):
        """ Returns all of the Customers who are subscribed

        Args:
            none
        """
        cls.logger.info('Processing subscription query ...',)
        return cls.query.filter(cls.subscribed == True)

    @classmethod
    def find_by_address1(cls, address1):
        """ Returns all of the Customers with a address1

        Args:
            address1 (string): the address1 of the Customer you want to match
        """
        cls.logger.info('Processing address1 query for %s ...', address1)
        return cls.query.filter(cls.address1 == address1)

    @classmethod
    def find_by_address2(cls, address2):
        """ Returns all of the Customers with a address2

        Args:
            address2 (string): the address2 of the Customer you want to match
        """
        cls.logger.info('Processing address2 query for %s ...', address2)
        return cls.query.filter(cls.address2 == address2)

    @classmethod
    def find_by_email(cls, email):
        """ Returns all of the Customers with a email

        Args:
            email (string): the email of the Customer you want to match
        """
        cls.logger.info('Processing email query for %s ...', email)
        return cls.query.filter(cls.email == email)

    @classmethod
    def find_by_city(cls, city):
        """ Returns all of the Customers with a city

        Args:
            city (string): the city of the Customer you want to match
        """
        cls.logger.info('Processing city query for %s ...', city)
        return cls.query.filter(cls.city == city)

    @classmethod
    def find_by_province(cls, province):
        """ Returns all of the Customers with a province

        Args:
            province (string): the province of the Customer you want to match
        """
        cls.logger.info('Processing province query for %s ...', province)
        return cls.query.filter(cls.province == province)

    @classmethod
    def find_by_country(cls, country):
        """ Returns all of the Customers with a country

        Args:
            country (string): the country of the Customer you want to match
        """
        cls.logger.info('Processing country query for %s ...', country)
        return cls.query.filter(cls.country == country)

    @classmethod
    def find_by_zip(cls, zip):
        """ Returns all of the Customers with a zip

        Args:
            zip (string): the zip of the Customer you want to match
        """
        cls.logger.info('Processing zip query for %s ...', zip)
        return cls.query.filter(cls.zip == zip)
