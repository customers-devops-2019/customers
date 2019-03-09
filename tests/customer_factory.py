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
    name = factory.Faker('John Doe')
    email = FuzzyChoice(choices=['iphone_hacker@gmail.com',
                                 'gold_to_ship@prince.com', 'ubreakifix@nsa.org'])


if __name__ == '__main__':
    for _ in range(10):
        customer = CustomerFactory()
        print(custoemr.serialize())
