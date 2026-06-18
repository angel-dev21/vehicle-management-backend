from rest_framework.test import APITestCase
from rest_framework import status
from apps.user.models import User

class UserViewSetTests(APITestCase):
    
    def setUp(self):
        self.admin = User.objects.create_user(
            email='admin@test.com', password='Admin123!', role='ADMIN', is_staff=True
        )
        self.technician = User.objects.create_user(
            email='tech@test.com', password='Tech123!', role='TECHNICIAN'
        )

    def test_admin_can_create_user(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post('/users/', {
            'email': 'new@test.com',
            'password': 'New1234!',
            'first_name': 'Carlos',
            'last_name': 'Perez',
            'role': 'MECHANIC',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_technician_cannot_create_user(self):
        self.client.force_authenticate(user=self.technician)
        response = self.client.post('/users/', {
            'email': 'new2@test.com',
            'password': 'New1234!',
            'first_name': 'Carlos',
            'last_name': 'Perez',
            'role': 'MECHANIC',
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)