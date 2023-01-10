
import factory
from factory.django import DjangoModelFactory
from .models import Department, DepartmentMember, Designations



class DepartmentFactory(DjangoModelFactory):
    class Meta:
        model=Department
    name = factory.Faker('name')
    description = factory.Faker('description')
