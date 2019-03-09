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
name (string) - the name of the customer
category (string) - the email

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
    name = db.Column(db.String(63))
    email = db.Column(db.String(63))

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
        return {"id": self.id,
                "name": self.name,
                "email": self.email}

    def deserialize(self, data):
        """
        Deserializes a Customer from a dictionary

        Args:
            data (dict): A dictionary containing the Customer data
        """
        try:
            self.name = data['name']
            self.email = data['email']
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
    def find_by_name(cls, name):
        """ Returns all Customers with the given name

        Args:
            name (string): the name of the Customers you want to match
        """
        cls.logger.info('Processing name query for %s ...', name)
        return cls.query.filter(cls.name == name)

    @classmethod
    def find_by_email(cls, email):
        """ Returns all of the Customers with a email

        Args:
            email (string): the email of the Customer you want to match
        """
        cls.logger.info('Processing email query for %s ...', email)
        return cls.query.filter(cls.email == email)
