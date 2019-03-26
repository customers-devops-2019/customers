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
        customer = Customer(firstname="John", lastname="Doe", email="fake1@email.com",
                            subscribed=False, address1="123 Main St", address2="1B",
                            city="New York", country="USA", province="NY", zip="12310"
                           )
        self.assertTrue(customer != None)
        self.assertEqual(customer.id, None)
        self.assertEqual(customer.firstname, "John")
        self.assertEqual(customer.lastname, "Doe")
        self.assertEqual(customer.email, "fake1@email.com")
        self.assertEqual(customer.subscribed, False)
        self.assertEqual(customer.address1, "123 Main St")
        self.assertEqual(customer.address2, "1B")
        self.assertEqual(customer.city, "New York")
        self.assertEqual(customer.province, "NY")
        self.assertEqual(customer.country, "USA")
        self.assertEqual(customer.zip, "12310")

    def test_add_a_customer(self):
        """ Create a customer and add it to the database """
        customers = Customer.all()
        self.assertEqual(customers, [])
        customer = Customer(firstname="John", lastname="Doe", email="fake1@email.com",
                            subscribed=False, address1="123 Main St", address2="1B",
                            city="New York", country="USA", province="NY", zip="12310"
                           )
        self.assertTrue(customer != None)
        self.assertEqual(customer.id, None)
        customer.save()
        # Asert that it was assigned an id and shows up in the database
        self.assertEqual(customer.id, 1)
        customers = Customer.all()
        self.assertEqual(len(customers), 1)

    def test_update_a_customer_name(self):
        """ Update a Customer name """
        customer = Customer(firstname="John", lastname="Doe", email="fake1@email.com",
                            subscribed=False, address1="123 Main St", address2="1B",
                            city="New York", country="USA", province="NY", zip="12310"
                           )
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

    def test_update_a_customer_email(self):
        """ Update a Customer email """
        customer = Customer(firstname="John", lastname="Doe", email="fake1@email.com",
                            subscribed=False, address1="123 Main St", address2="1B",
                            city="New York", country="USA", province="NY", zip="12310"
                           )
        customer.save()
        self.assertEqual(customer.id, 1)
        # Change it an save it
        customer.email = "ethan@gmail.com"
        customer.save()
        self.assertEqual(customer.id, 1)
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        customers = customer.all()
        self.assertEqual(len(customers), 1)
        self.assertEqual(customers[0].email, "ethan@gmail.com")

    def test_update_cust_email_and_name(self):
        """ Update a Customer email and name"""
        customer = Customer(firstname="John", lastname="Doe", email="fake1@email.com",
                            subscribed=False, address1="123 Main St", address2="1B",
                            city="New York", country="USA", province="NY", zip="12310"
                           )
        customer.save()
        self.assertEqual(customer.id, 1)
        # Change it an save it
        customer.email = "ethan@gmail.com"
        customer.name = "Isabel"
        customer.save()
        self.assertEqual(customer.id, 1)
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        customers = customer.all()
        self.assertEqual(len(customers), 1)
        self.assertEqual(customers[0].email, "ethan@gmail.com")
        self.assertEqual(customers[0].name, "Isabel")

    def test_delete_a_customer(self):
        """ Delete a Customer """
        customer = Customer(firstname="John", lastname="Doe", email="fake1@email.com",
                            subscribed=False, address1="123 Main St", address2="1B",
                            city="New York", country="USA", province="NY", zip="12310"
                           )
        customer.save()
        self.assertEqual(len(customer.all()), 1)
        # delete the pet and make sure it isn't in the database
        customer.delete()
        self.assertEqual(len(customer.all()), 0)

    def test_serialize_a_customer(self):
        """ Test serialization of a Customer """
        customer = Customer(firstname="John", lastname="Doe", email="fake1@email.com",
                            subscribed=False, address1="123 Main St", address2="1B",
                            city="New York", country="USA", province="NY", zip="12310"
                           )
        data = customer.serialize()
        self.assertNotEqual(data, None)
        self.assertIn('id', data)
        self.assertEqual(data['id'], None)
        self.assertIn('firstname', data)
        self.assertEqual(data['firstname'], "John")
        self.assertIn('lastname', data)
        self.assertEqual(data['lastname'], "Doe")
        self.assertIn('email', data)
        self.assertEqual(data['email'], "fake1@email.com")
        self.assertIn('subscribed', data)
        self.assertEqual(data['subscribed'], False)
        self.assertIn('address1', data["address"])
        self.assertEqual(data['address']['address1'], "123 Main St")
        self.assertIn('address2', data["address"])
        self.assertEqual(data['address']['address2'], "1B")
        self.assertIn('city', data["address"])
        self.assertEqual(data['address']['city'], "New York")
        self.assertIn('province', data["address"])
        self.assertEqual(data['address']['province'], "NY")
        self.assertIn('country', data["address"])
        self.assertEqual(data['address']['country'], "USA")
        self.assertIn('zip', data["address"])
        self.assertEqual(data['address']['zip'], "12310")


    def test_deserialize_a_customer(self):
        """ Test deserialization of a Customer """
        data = {
            "id":1,
        	   "firstname":"John",
        	   "lastname":"Doe",
        	   "email":"fake1@email.com",
        	   "subscribed": False,
        	   "address": {
        		             "address1": "123 Main St",
        		             "address2":"1B",
        		             "city":"New York",
        		             "province":"NY",
        		             "country":"USA",
        		             "zip":"12310"
                       }
        }
        customer = Customer()
        customer.deserialize(data)
        self.assertNotEqual(customer, None)
        self.assertEqual(customer.id, None)
        self.assertEqual(customer.firstname, "John")
        self.assertEqual(customer.lastname, "Doe")
        self.assertEqual(customer.email, "fake1@email.com")
        self.assertEqual(customer.subscribed, False)
        self.assertEqual(customer.address1, "123 Main St")
        self.assertEqual(customer.address2, "1B")
        self.assertEqual(customer.city, "New York")
        self.assertEqual(customer.province, "NY")
        self.assertEqual(customer.country, "USA")
        self.assertEqual(customer.zip, "12310")

    def test_deserialize_bad_data(self):
        """ Test deserialization of bad data """
        data = "this is not a dictionary"
        customer = Customer()
        self.assertRaises(DataValidationError, customer.deserialize, data)

    def test_find_customer(self):
        """ Find a Customer by ID """
        customer = Customer(firstname="Sarah", lastname="Sally",
                            email="fake2@email.com", subscribed=False, address1="124 Main St",
                            address2="1E", city="New York", country="USA", province="NY",
                            zip="12310").save()
        new_customer = Customer(firstname="John", lastname="Doe",
                                email="fake1@email.com", subscribed=False,
                                address1="123 Main St", address2="1B", city="New York",
                                country="USA", province="NY", zip="12310"
                               )
        new_customer.save()
        customer = Customer.find(new_customer.id)
        self.assertIsNot(customer, None)
        self.assertEqual(customer.id, new_customer.id)
        self.assertEqual(customer.firstname, "John")
        self.assertEqual(customer.lastname, "Doe")
        self.assertEqual(customer.email, "fake1@email.com")
        self.assertEqual(customer.subscribed, False)
        self.assertEqual(customer.address1, "123 Main St")
        self.assertEqual(customer.address2, "1B")
        self.assertEqual(customer.city, "New York")
        self.assertEqual(customer.province, "NY")
        self.assertEqual(customer.country, "USA")
        self.assertEqual(customer.zip, "12310")


    def test_find_by_email(self):
        """ Find Customers by Email """
        Customer(firstname="John", lastname="Doe", email="fake1@email.com",
                 subscribed=False, address1="123 Main St", address2="1B",
                 city="New York", country="USA", province="NY", zip="12310").save()
        Customer(firstname="Sarah", lastname="Sally", email="fake2@email.com",
                 subscribed=False, address1="124 Main St", address2="1E",
                 city="New York", country="USA", province="NY", zip="12310").save()
        customers = Customer.find_by_email("fake1@email.com")
        self.assertEqual(customers[0].email, "fake1@email.com")
        self.assertEqual(customers[0].firstname, "John")
        self.assertEqual(customers[0].lastname, "Doe")
        self.assertEqual(customers[0].subscribed, False)
        self.assertEqual(customers[0].address1, "123 Main St")
        self.assertEqual(customers[0].address2, "1B")
        self.assertEqual(customers[0].city, "New York")
        self.assertEqual(customers[0].province, "NY")
        self.assertEqual(customers[0].country, "USA")
        self.assertEqual(customers[0].zip, "12310")


    def test_find_by_first_name(self):
        """ Find a Customer by First Name """
        Customer(firstname="John", lastname="Doe", email="fake1@email.com",
                 subscribed=False, address1="123 Main St", address2="1B",
                 city="New York", country="USA", province="NY", zip="12310").save()
        Customer(firstname="Sarah", lastname="Sally", email="fake2@email.com",
                 subscribed=False, address1="124 Main St", address2="1E",
                 city="New York", country="USA", province="NY", zip="12310").save()
        customers = Customer.find_by_first_name("John")
        self.assertEqual(customers[0].email, "fake1@email.com")
        self.assertEqual(customers[0].firstname, "John")
        self.assertEqual(customers[0].lastname, "Doe")
        self.assertEqual(customers[0].subscribed, False)
        self.assertEqual(customers[0].address1, "123 Main St")
        self.assertEqual(customers[0].address2, "1B")
        self.assertEqual(customers[0].city, "New York")
        self.assertEqual(customers[0].province, "NY")
        self.assertEqual(customers[0].country, "USA")
        self.assertEqual(customers[0].zip, "12310")

    def test_find_by_last_name(self):
        """ Find a Customer by Last Name """
        Customer(firstname="John", lastname="Doe", email="fake1@email.com",
                 subscribed=False, address1="123 Main St", address2="1B", city="New York",
                 country="USA", province="NY", zip="12310").save()
        Customer(firstname="Sarah", lastname="Sally", email="fake2@email.com",
                 subscribed=False, address1="124 Main St", address2="1E", city="New York",
                 country="USA", province="NY", zip="12310").save()
        customers = Customer.find_by_last_name("Doe")
        self.assertEqual(customers[0].email, "fake1@email.com")
        self.assertEqual(customers[0].firstname, "John")
        self.assertEqual(customers[0].lastname, "Doe")
        self.assertEqual(customers[0].subscribed, False)
        self.assertEqual(customers[0].address1, "123 Main St")
        self.assertEqual(customers[0].address2, "1B")
        self.assertEqual(customers[0].city, "New York")
        self.assertEqual(customers[0].province, "NY")
        self.assertEqual(customers[0].country, "USA")
        self.assertEqual(customers[0].zip, "12310")

    def test_find_by_address1(self):
        """ Find Customers by address1 """
        Customer(firstname="John", lastname="Doe", email="fake1@email.com",
                 subscribed=False, address1="123 Main St", address2="1B", city="New York",
                 country="USA", province="NY", zip="12310").save()
        Customer(firstname="Sarah", lastname="Sally", email="fake2@email.com",
                 subscribed=False, address1="124 Main St", address2="1E", city="New York",
                 country="USA", province="NY", zip="12310").save()
        customers = Customer.find_by_address1("123 Main St")
        self.assertEqual(customers[0].email, "fake1@email.com")
        self.assertEqual(customers[0].firstname, "John")
        self.assertEqual(customers[0].lastname, "Doe")
        self.assertEqual(customers[0].subscribed, False)
        self.assertEqual(customers[0].address1, "123 Main St")
        self.assertEqual(customers[0].address2, "1B")
        self.assertEqual(customers[0].city, "New York")
        self.assertEqual(customers[0].province, "NY")
        self.assertEqual(customers[0].country, "USA")
        self.assertEqual(customers[0].zip, "12310")

    def test_find_by_address2(self):
        """ Find Customers by address2 """
        Customer(firstname="John", lastname="Doe", email="fake1@email.com",
                 subscribed=False, address1="123 Main St", address2="1B", city="New York",
                 country="USA", province="NY", zip="12310").save()
        Customer(firstname="Sarah", lastname="Sally", email="fake2@email.com",
                 subscribed=False, address1="124 Main St", address2="1E", city="New York",
                 country="USA", province="NY", zip="12310").save()
        customers = Customer.find_by_address2("1B")
        self.assertEqual(customers[0].email, "fake1@email.com")
        self.assertEqual(customers[0].firstname, "John")
        self.assertEqual(customers[0].lastname, "Doe")
        self.assertEqual(customers[0].subscribed, False)
        self.assertEqual(customers[0].address1, "123 Main St")
        self.assertEqual(customers[0].address2, "1B")
        self.assertEqual(customers[0].city, "New York")
        self.assertEqual(customers[0].province, "NY")
        self.assertEqual(customers[0].country, "USA")
        self.assertEqual(customers[0].zip, "12310")

    def test_find_by_city(self):
        """ Find Customers by city """
        Customer(firstname="John", lastname="Doe", email="fake1@email.com",
                 subscribed=False, address1="123 Main St", address2="1B", city="New York",
                 country="USA", province="NY", zip="12310").save()
        Customer(firstname="Sarah", lastname="Sally", email="fake2@email.com",
                 subscribed=False, address1="124 Main St", address2="1E", city="New York",
                 country="USA", province="NY", zip="12310").save()
        customers = Customer.find_by_city("New York")
        self.assertEqual(customers[0].email, "fake1@email.com")
        self.assertEqual(customers[0].firstname, "John")
        self.assertEqual(customers[0].lastname, "Doe")
        self.assertEqual(customers[0].subscribed, False)
        self.assertEqual(customers[0].address1, "123 Main St")
        self.assertEqual(customers[0].address2, "1B")
        self.assertEqual(customers[0].city, "New York")
        self.assertEqual(customers[0].province, "NY")
        self.assertEqual(customers[0].country, "USA")
        self.assertEqual(customers[0].zip, "12310")

    def test_find_by_province(self):
        """ Find Customers by state(province) """
        Customer(firstname="John", lastname="Doe", email="fake1@email.com",
                 subscribed=False, address1="123 Main St", address2="1B", city="New York",
                 country="USA", province="NY", zip="12310").save()
        Customer(firstname="Sarah", lastname="Sally", email="fake2@email.com",
                 subscribed=False, address1="124 Main St", address2="1E", city="New York",
                 country="USA", province="NY", zip="12310").save()
        customers = Customer.find_by_province("NY")
        self.assertEqual(customers[0].email, "fake1@email.com")
        self.assertEqual(customers[0].firstname, "John")
        self.assertEqual(customers[0].lastname, "Doe")
        self.assertEqual(customers[0].subscribed, False)
        self.assertEqual(customers[0].address1, "123 Main St")
        self.assertEqual(customers[0].address2, "1B")
        self.assertEqual(customers[0].city, "New York")
        self.assertEqual(customers[0].province, "NY")
        self.assertEqual(customers[0].country, "USA")
        self.assertEqual(customers[0].zip, "12310")

    def test_find_by_country(self):
        """ Find Customers by country """
        Customer(firstname="John", lastname="Doe", email="fake1@email.com",
                 subscribed=False, address1="123 Main St", address2="1B", city="New York",
                 country="USA", province="NY", zip="12310").save()
        Customer(firstname="Sarah", lastname="Sally", email="fake2@email.com",
                 subscribed=False, address1="124 Main St", address2="1E", city="New York",
                 country="USA", province="NY", zip="12310").save()
        customers = Customer.find_by_country("USA")
        self.assertEqual(customers[0].email, "fake1@email.com")
        self.assertEqual(customers[0].firstname, "John")
        self.assertEqual(customers[0].lastname, "Doe")
        self.assertEqual(customers[0].subscribed, False)
        self.assertEqual(customers[0].address1, "123 Main St")
        self.assertEqual(customers[0].address2, "1B")
        self.assertEqual(customers[0].city, "New York")
        self.assertEqual(customers[0].province, "NY")
        self.assertEqual(customers[0].country, "USA")
        self.assertEqual(customers[0].zip, "12310")

    def test_find_by_zip(self):
        """ Find Customers by zip """
        Customer(firstname="John", lastname="Doe", email="fake1@email.com",
                 subscribed=False, address1="123 Main St", address2="1B", city="New York",
                 country="USA", province="NY", zip="12310").save()
        Customer(firstname="Sarah", lastname="Sally", email="fake2@email.com",
                 subscribed=False, address1="124 Main St", address2="1E", city="New York",
                 country="USA", province="NY", zip="12310").save()
        customers = Customer.find_by_zip("12310")
        self.assertEqual(customers[0].email, "fake1@email.com")
        self.assertEqual(customers[0].firstname, "John")
        self.assertEqual(customers[0].lastname, "Doe")
        self.assertEqual(customers[0].subscribed, False)
        self.assertEqual(customers[0].address1, "123 Main St")
        self.assertEqual(customers[0].address2, "1B")
        self.assertEqual(customers[0].city, "New York")
        self.assertEqual(customers[0].province, "NY")
        self.assertEqual(customers[0].country, "USA")
        self.assertEqual(customers[0].zip, "12310")

    def test_find_by_subscribed(self):
        """ Find Customers by subscribed """
        Customer(firstname="John", lastname="Doe", email="fake1@email.com",
                 subscribed=False, address1="123 Main St", address2="1B", city="New York",
                 country="USA", province="NY", zip="12310").save()
        Customer(firstname="Sarah", lastname="Sally", email="fake2@email.com",
                 subscribed=False, address1="124 Main St", address2="1E", city="New York",
                 country="USA", province="NY", zip="12310").save()
        customers = Customer.find_by_subscribed(False)
        self.assertEqual(customers[0].email, "fake1@email.com")
        self.assertEqual(customers[0].firstname, "John")
        self.assertEqual(customers[0].lastname, "Doe")
        self.assertEqual(customers[0].subscribed, False)
        self.assertEqual(customers[0].address1, "123 Main St")
        self.assertEqual(customers[0].address2, "1B")
        self.assertEqual(customers[0].city, "New York")
        self.assertEqual(customers[0].province, "NY")
        self.assertEqual(customers[0].country, "USA")
        self.assertEqual(customers[0].zip, "12310")


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
