from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.user.models import User


class UserViewSetPermissionTests(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_user(
            email='admin@test.com', password='Valid123!',
            first_name='Admin', last_name='User', role='ADMIN'
        )
        self.tech = User.objects.create_user(
            email='tech@test.com', password='Valid123!',
            first_name='Tech', last_name='User', role='TECHNICIAN'
        )
        self.other_tech = User.objects.create_user(
            email='other@test.com', password='Valid123!',
            first_name='Other', last_name='User', role='TECHNICIAN'
        )
        self.list_url = reverse('user-list')

    def test_non_admin_cannot_create_user(self):
        self.client.force_authenticate(self.tech)
        data = {
            'email': 'new@test.com', 'password': 'Valid123!',
            'first_name': 'New', 'last_name': 'User',
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_user(self):
        self.client.force_authenticate(self.admin)
        data = {
            'email': 'new@test.com', 'password': 'Valid123!',
            'first_name': 'New', 'last_name': 'User',
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_non_admin_cannot_list_users(self):
        self.client.force_authenticate(self.tech)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_list_users(self):
        self.client.force_authenticate(self.admin)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_retrieve_own_profile(self):
        self.client.force_authenticate(self.tech)
        url = reverse('user-detail', args=[self.tech.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_retrieve_other_profile(self):
        self.client.force_authenticate(self.tech)
        url = reverse('user-detail', args=[self.other_tech.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserViewSetDestroyTests(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_user(
            email='admin@test.com', password='Valid123!',
            first_name='Admin', last_name='User', role='ADMIN'
        )
        self.tech = User.objects.create_user(
            email='tech@test.com', password='Valid123!',
            first_name='Tech', last_name='User', role='TECHNICIAN'
        )

    def test_destroy_soft_deletes_user(self):
        self.client.force_authenticate(self.admin)
        url = reverse('user-detail', args=[self.tech.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.tech.refresh_from_db()
        self.assertFalse(self.tech.is_active)
        self.assertTrue(User.objects.filter(id=self.tech.id).exists())

    def test_soft_deleted_user_not_in_list(self):
        self.tech.is_active = False
        self.tech.save()
        self.client.force_authenticate(self.admin)
        response = self.client.get(reverse('user-list'))
        ids = [u['id'] for u in response.data]
        self.assertNotIn(self.tech.id, ids)


class UserViewSetSetRoleTests(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_user(
            email='admin@test.com', password='Valid123!',
            first_name='Admin', last_name='User', role='ADMIN'
        )
        self.tech = User.objects.create_user(
            email='tech@test.com', password='Valid123!',
            first_name='Tech', last_name='User', role='TECHNICIAN'
        )

    def test_admin_can_change_role(self):
        self.client.force_authenticate(self.admin)
        url = reverse('user-set-role', args=[self.tech.id])
        response = self.client.patch(url, {'role': 'ADMIN'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.tech.refresh_from_db()
        self.assertEqual(self.tech.role, 'ADMIN')

    def test_non_admin_cannot_change_own_role(self):
        self.client.force_authenticate(self.tech)
        url = reverse('user-set-role', args=[self.tech.id])
        response = self.client.patch(url, {'role': 'ADMIN'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_role_field_ignored_in_normal_update(self):
        self.client.force_authenticate(self.tech)
        url = reverse('user-detail', args=[self.tech.id])
        response = self.client.patch(url, {'role': 'ADMIN', 'first_name': 'Changed'})
        self.tech.refresh_from_db()
        self.assertEqual(self.tech.role, 'TECHNICIAN')
        self.assertEqual(self.tech.first_name, 'Changed')