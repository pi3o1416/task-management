
from django.contrib.auth import get_user_model
from django.test import TestCase
from ..models import Department, Designations, DepartmentMember

User = get_user_model()


class DepartmentTest(TestCase):
    def setUp(self):
        Department.objects.create(
            name="test department",
            description="this is test",
        )

    def get_department(self):
        return Department.objects.get(
            name="test department"
        )

    def test_slug_field(self):
        department = self.get_department()
        slug = department.slug
        self.assertTrue(slug, "Slug should not be null")

    def test_department_name_max_length(self):
        max_length = Department._meta.get_field('name').max_length
        self.assertEqual(max_length, 200, "Department max lenght should be 200")

    def test_department_name_null_restriction(self):
        null = Department._meta.get_field('name').null
        self.assertTrue(null==False, "Department name null should be false")

    def test_department_name_blank_restriction(self):
        blank = Department._meta.get_field('name').blank
        self.assertTrue(blank==False, "Department name blank should be false")

    def test_department_name_unique_restriction(self):
        unique = Department._meta.get_field('name').unique
        self.assertTrue(unique==True, "Department name unique should be true")

    def test_department_slug_unique_restriction(self):
        unique = Department._meta.get_field('slug').unique
        self.assertTrue(unique==True, "Department slug unique should be true")

    def test_department_slug_null_restriction(self):
        null = Department._meta.get_field('slug').null
        self.assertTrue(null==False, "Department slug null should be false")

    def test_department_description_null_restriction(self):
        null = Department._meta.get_field('description').null
        self.assertTrue(null==False, "Department description null should be false")

    def test_department_description_blank_restriction(self):
        blank = Department._meta.get_field('description').blank
        self.assertTrue(blank==False, "Department description blank should be false")


class DesignationTest(TestCase):
    def setUp(self):
        self.department = Department.objects.create(
            name="test",
            description = "test description"
        )
        self.designaiton = Designations.objects.create(
            department = self.department,
            title = "test designation"
        )

class DepartmentMemberTest(TestCase):
    def setUp(self):
        self.department = Department.objects.create(
            name="test",
            description = "test description"
        )
        self.user = User.objects.create(
            username='test_user',
            first_name='test',
            last_name='user',
            email='test@aamarpay.com'
        )
        self.designation = Designations.objects.create(
            department = self.department,
            title = "test designation"
        )
        self.member = DepartmentMember.objects.create(
            member = self.user,
            designation = self.designation,
            department = self.department
        )
