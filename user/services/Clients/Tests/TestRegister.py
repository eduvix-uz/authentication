from rest_framework.test import APITestCase
from rest_framework import status
from user.models import User

class TestRegisterUser(APITestCase):
    def setUp(self):
        self.register_url = '/profile/register/'
        self.user_data = {
            "email": "6aBv2@example.com",
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "password": "tester1234",
        }

    def test_register_user(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

        