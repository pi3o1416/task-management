
from django.test import TestCase
from ..serializers import PasswordResetSerializer



class PasswordResetSerializerTest(TestCase):
    def setUp(self):
        self.serializer_data = {
            "password": "1234567891@",
            "retype_password": "1234567891@"
        }

    def test_validation(self):
        is_valid = PasswordResetSerializer(data=self.serializer_data).is_valid()
        self.assertTrue(is_valid==True, "Serializer Validation with default data should be true")

    def test_password_mismatch(self):
        self.serializer_data["retype_password"] = "12345678911@"
        is_valid = PasswordResetSerializer(data=self.serializer_data).is_valid()
        self.assertTrue(is_valid==False, "Serializer Validation should be false with mispatch password")

    def test_password_password_validation(self):
        self.serializer_data["password"] = "1234"
        self.serializer_data["retype_password"] = "1234"
        is_valid = PasswordResetSerializer(data=self.serializer_data).is_valid()
        self.assertTrue(is_valid==False, "Serializer validation should be false with too short and common password")



