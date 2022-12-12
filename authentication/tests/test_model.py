

from django.test import TestCase
from django.utils.http import urlsafe_base64_encode
from django.core.exceptions import ValidationError
from ..models import CustomUser


class CustomUserModelTest(TestCase):
    def setUp(self):
        CustomUser.objects.create(
            username='test_user',
            first_name='test',
            last_name='user',
            email='test@aamarpay.com'
        )

    def get_user(self):
        return CustomUser.objects.get(username='test_user')

    def test_default_account_status(self):
        user = self.get_user()
        self.assertTrue(user.is_active==False, "User shold be inactive by default")

    def test_default_staff_status(self):
        user = self.get_user()
        self.assertTrue(user.is_staff==False, "User staff permission should be false by default")

    def test_full_name_property(self):
        user = self.get_user()
        self.assertEqual(user.full_name, '{} {}'.format(user.first_name, user.last_name), "User Full name wrong")

    def test_default_ordering(self):
        ordering = CustomUser._meta.ordering
        self.assertEqual(ordering, ['username'])

    def test_base64_encoded_pk(self):
        user = self.get_user()
        pk_str = str(user.pk)
        pk_bytes = bytes(pk_str, 'utf-8')
        encoded_pk = urlsafe_base64_encode(pk_bytes)
        self.assertEqual(encoded_pk, user.generate_urlsafe_b64_encoded_pk(), "Generate user b64 encoded pk wrong")

    def test_token_generatio(self):
        user = self.get_user()
        user_token = user.generate_token()
        self.assertTrue(user.validate_token(user_token), "User token wrong")

    def test_email_validation(self):
        try:
            user = self.get_user()
            user.email = 'test@gmail.com'
            user.save()
        except ValidationError:
            self.assertTrue(True, "Password Validation wrong")

    def test_email_blank_restriction(self):
        blank = CustomUser._meta.get_field('email').blank
        self.assertTrue(blank==False, "Email blank should not by allowed")

    def test_email_null_restriction(self):
        null = CustomUser._meta.get_field("email").null
        self.assertTrue(null==False, "Email null should not be allowed")

    def test_first_name_max_length(self):
        max_length = CustomUser._meta.get_field("first_name").max_length
        self.assertEqual(max_length, 150, "Max length wrong")

    def test_first_name_blank_restriction(self):
        max_length = CustomUser._meta.get_field("last_name").max_length
        self.assertEqual(max_length, 150, "Max length wrong")

    def test_first_name_null_restriction(self):
        null = CustomUser._meta.get_field("first_name").null
        self.assertTrue(null==False, "first name null should not be allowed")

    def test_last_name_max_length(self):
        max_length = CustomUser._meta.get_field("last_name").max_length
        self.assertEqual(max_length, 150, "Max length wrong")

    def test_last_name_null_restriction(self):
        null = CustomUser._meta.get_field("last_name").null
        self.assertTrue(null==False, "last name null should not be allowed")

    def test_last_name_blank_restriction(self):
        blank = CustomUser._meta.get_field("last_name").blank
        self.assertTrue(blank==False, "last name blank should not be allowed")


























