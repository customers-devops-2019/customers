"""
Test cases for Customer Model

Test cases can be run with:
  nosetests
  coverage report -m
"""

import unittest
import os
from app.models import Customer, DataValidationError, db
from app import app

DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///../db/test.db')

######################################################################
#  T E S T   C A S E S
######################################################################


class TestCustomers(unittest.TestCase):
    """ Test Cases for Customers """

    @classmethod
    def setUpClass(cls):
        """ These run once per Test suite """
        app.debug = False
        # Set up the test database
        app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        Customer.init_db(app)
        db.drop_all()    # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_a_customer(self):
        """ Create a customer and assert that it exists """
        customer = Customer(name="Tim Apple", email="iphone_hacker@gmail.com")
        self.assertTrue(customer != None)
        self.assertEqual(customer.id, None)
        self.assertEqual(customer.name, "Tim Apple")
        self.assertEqual(customer.email, "iphone_hacker@gmail.com")

    def test_add_a_customer(self):
        """ Create a customer and add it to the database """
        customers = Customer.all()
        self.assertEqual(customers, [])
        customer = Customer(name="Tim Apple", email="iphone_hacker@gmail.com")
        self.assertTrue(customer != None)
        self.assertEqual(customer.id, None)
        customer.save()
        # Asert that it was assigned an id and shows up in the database
        self.assertEqual(customer.id, 1)
        customers = Customer.all()
        self.assertEqual(len(customers), 1)


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
