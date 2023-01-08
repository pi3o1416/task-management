
import factory
from factory.django import DjangoModelFactory
from .models import CustomUser


class UserFactory(DjangoModelFactory):
    class Meta:
        model=CustomUser

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")



