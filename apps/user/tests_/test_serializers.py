from django.test import TestCase
from apps.user.serializers import UserCreateSerializer

class UserCreateSerializerTests(TestCase):

    def test_valid_data_is_correct(self):
        data = {
            'email': 'test@test.com',
            'password': 'Valid123!',
            'first_name': 'Ana',
            'last_name': 'Lopez',
            'role': 'TECHNICIAN',
        }
        serializer = UserCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())