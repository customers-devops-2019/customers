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
    id = factory.Sequence(lambda n: n)
    name = factory.Faker('first_name')
    email = FuzzyChoice(choices=['fake1@email.com',
                                 'fake2@email.com', 'fake3@email.com', 'fake12@email.com', 'fake23@email.com'])


if __name__ == '__main__':
    for _ in range(10):
        customer = CustomerFactory()
        print(custoemr.serialize())
