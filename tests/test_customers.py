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
        customer = Customer(name="John Doe", email="fake1@email.com")
        self.assertTrue(customer != None)
        self.assertEqual(customer.id, None)
        self.assertEqual(customer.name, "John Doe")
        self.assertEqual(customer.email, "fake1@email.com")

    def test_add_a_customer(self):
        """ Create a customer and add it to the database """
        customers = Customer.all()
        self.assertEqual(customers, [])
        customer = Customer(name="John Doe", email="fake1@email.com")
        self.assertTrue(customer != None)
        self.assertEqual(customer.id, None)
        customer.save()
        # Asert that it was assigned an id and shows up in the database
        self.assertEqual(customer.id, 1)
        customers = Customer.all()
        self.assertEqual(len(customers), 1)

    def test_update_a_customer(self):
        """ Update a Customer """
        customer = Customer(name="John Doe", email="fake1@email.com")
        customer.save()
        self.assertEqual(customer.id, 1)
        # Change it an save it
        customer.name = "Isabel"
        customer.save()
        self.assertEqual(customer.id, 1)
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        customers = customer.all()
        self.assertEqual(len(customers), 1)
        self.assertEqual(customers[0].name, "Isabel")

    def test_delete_a_customer(self):
        """ Delete a Customer """
        customer = Customer(name="John Doe", email="fake1@email.com")
        customer.save()
        self.assertEqual(len(customer.all()), 1)
        # delete the pet and make sure it isn't in the database
        customer.delete()
        self.assertEqual(len(customer.all()), 0)

    def test_serialize_a_customer(self):
        """ Test serialization of a Customer """
        customer = Customer(name="Tim", email="fake1@email.com")
        data = customer.serialize()
        self.assertNotEqual(data, None)
        self.assertIn('id', data)
        self.assertEqual(data['id'], None)
        self.assertIn('name', data)
        self.assertEqual(data['name'], "Tim")
        self.assertIn('email', data)
        self.assertEqual(data['email'], "fake1@email.com")

    def test_deserialize_a_customer(self):
        """ Test deserialization of a Customer """
        data = {"id": 1, "name": "Tim", "email": "fake1@email.com"}
        customer = Customer()
        customer.deserialize(data)
        self.assertNotEqual(customer, None)
        self.assertEqual(customer.id, None)
        self.assertEqual(customer.name, "Tim")
        self.assertEqual(customer.email, "fake1@email.com")

    def test_deserialize_bad_data(self):
        """ Test deserialization of bad data """
        data = "this is not a dictionary"
        customer = Customer()
        self.assertRaises(DataValidationError, customer.deserialize, data)

    def test_find_customer(self):
        """ Find a Customer by ID """
        Customer(name="Tim", email="fake1@email.com").save()
        newCustomer = Customer(name="Tim", email="fake1@email.com")
        newCustomer.save()
        customer = Customer.find(newCustomer.id)
        self.assertIsNot(customer, None)
        self.assertEqual(customer.id, newCustomer.id)
        self.assertEqual(customer.name, "Tim")
        self.assertEqual(customer.email, "fake1@email.com")

    def test_find_by_email(self):
        """ Find Customers by Email """
        Customer(name="Tim", email="fake1@email.com").save()
        Customer(name="Sarah", email="fake2@email.com").save()
        customers = Customer.find_by_email("fake1@email.com")
        self.assertEqual(customers[0].email, "fake1@email.com")
        self.assertEqual(customers[0].name, "Tim")

    def test_find_by_name(self):
        """ Find a Customer by Name """
        Customer(name="Tim", email="fake1@email.com").save()
        Customer(name="Sarah", email="fake2@email.com").save()
        customers = Customer.find_by_name("Tim")
        self.assertEqual(customers[0].email, "fake1@email.com")
        self.assertEqual(customers[0].name, "Tim")


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
