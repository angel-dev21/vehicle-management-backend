from django.test import TestCase
from apps.user.models import User
from apps.user.serializers import UserSerializer


class UserCreateSerializerTests(TestCase):

    def setUp(self):
        self.valid_data = {
            'email': 'test@test.com',
            'password': 'Valid123!',
            'first_name': 'Ana',
            'last_name': 'Lopez',
            'role': 'TECHNICIAN',
        }

    def test_valid_data_is_correct(self):
        serializer = UserSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_password_too_short_is_invalid(self):
        data = self.valid_data.copy()
        data['password'] = 'short1'
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

    def test_missing_email_is_invalid(self):
        data = self.valid_data.copy()
        data.pop('email')
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_invalid_email_format_is_invalid(self):
        data = self.valid_data.copy()
        data['email'] = 'not-an-email'
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_password_is_write_only(self):
        serializer = UserSerializer(data=self.valid_data)
        serializer.is_valid()
        self.assertNotIn('password', serializer.data)

    def test_create_hashes_password(self):
        serializer = UserSerializer(data=self.valid_data)
        serializer.is_valid()
        user = serializer.save()
        self.assertNotEqual(user.password, self.valid_data['password'])
        self.assertTrue(user.check_password(self.valid_data['password']))

    def test_create_persists_user_in_db(self):
        serializer = UserSerializer(data=self.valid_data)
        serializer.is_valid()
        serializer.save()
        self.assertTrue(User.objects.filter(email='test@test.com').exists())