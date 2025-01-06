from rest_framework.test import APITestCase
from rest_framework import status
from user.models import User


class TestLoginUser(APITestCase):
    def setUp(self):
        self.login_url = '/profile/login/'
        self.user = User.objects.create_user(
            username='testusername',
            password='tester123',
            email='testemail@example.com',
            is_verified=True
        )
    def test_login_valid_credentials(self):
        data = {
            "username": "testusername",
            "password": "tester123"
        }
        if self.user.is_verified == True:
            response = self.client.post(self.login_url, data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        elif self.user.is_verified == False:
            response = self.client.post(self.login_url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    
    def test_login_unverified_credentials(self):
        data = {
            "username": "testuser",
            "password": "tester1234"
        }
        if self.user.is_verified == False:
            response = self.client.post(self.login_url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        elif self.user.is_verified == True and (data['username'] == self.user.username and data['password'] == self.user.password) or (data['username'] != self.user.username or data['password'] != self.user.password):
            response = self.client.post(self.login_url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
