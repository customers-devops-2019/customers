"""
Test Factory to make fake objects for testing
"""
import factory
from factory.fuzzy import FuzzyChoice
from app.models import Customer


class CustomerFactory(factory.Factory):
    """ Creates fake customers that you don't have to feed """
    class Meta:
        model = Customer
        exclude = ('number', 'street')
    id = factory.Sequence(lambda n: n)
    firstname = factory.Faker('first_name')
    lastname = factory.Faker('last_name')
    email = FuzzyChoice(choices=['fake1@email.com',
                                 'fake2@email.com', 'fake3@email.com', 'fake12@email.com', 'fake23@email.com'])
    subscribed = FuzzyChoice(choices=[True, False])
    number = factory.Faker('random_int')
    street = factory.Faker('street_name')
    address1 = factory.LazyAttribute(lambda p: '{} {}'.format(p.number, p.street))
    address2 = factory.Faker('secondary_address')
    city = factory.Faker('city')
    province = factory.Faker('state')
    country = factory.Faker('country')
    zip = factory.Faker('zipcode')


if __name__ == '__main__':
    for _ in range(10):
        customer = CustomerFactory()
        print(custoemr.serialize())
