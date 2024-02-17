from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

class YourTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.base_url = '/api/'
        self.data = {
            'first_name': 'Anas',
            'last_name': 'Ouh',
            'username': 'anas',
            'password': 'F1rstPassword!',
            'email': 'unit@test.com',
        }

    def test_user_authentication_flow(self):
        response = self.client.post(self.base_url + 'auth/signup/', self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(self.base_url + 'auth/login/', self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get('token')

        response = self.client.post(self.base_url + 'auth/token/verify/', {'token': token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        new_password_data = {
            'old_password': 'F1rstPassword!',
            'new_password': 'Secon2Password!',
        }
        headers = {'HTTP_AUTHORIZATION': 'Token ' + token}
        response = self.client.post(self.base_url + 'auth/password/change/', new_password_data, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        login_with_new_password_data = {
            'username': 'anas',
            'password': 'Secon2Password!',
        }
        response = self.client.post(self.base_url + 'auth/login/', login_with_new_password_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_token = response.data.get('token')

        password_reset_data = {
            'old_password': 'Secon2Password!',
            'new_password': 'F1rstPassword!',
        }
        headers = {'HTTP_AUTHORIZATION': 'Token ' + new_token}
        response = self.client.post(self.base_url + 'auth/password/change/', password_reset_data, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        headers = {'HTTP_AUTHORIZATION': 'Token ' + new_token}
        response = self.client.get(self.base_url + 'auth/logout/', **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_login_with_wrong_password(self):
        response = self.client.post(self.base_url + 'auth/signup/', self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        login_with_wrong_password_data = {
            'username': 'anas',
            'password': 'WrongPassword!',
        }
        response = self.client.post(self.base_url + 'auth/login/', login_with_wrong_password_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_change_password_with_wrong_old_password(self):
        # Create a new user
        response = self.client.post(self.base_url + 'auth/signup/', self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        token = response.data.get('token')

        new_password_data = {
            'old_password': 'WrongPassword!',
            'new_password': 'Secon2Password!',
        }
        headers = {'HTTP_AUTHORIZATION': 'Token ' + token}
        response = self.client.post(self.base_url + 'auth/password/change/', new_password_data, **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_signup_with_existing_username(self):
        response = self.client.post(self.base_url + 'auth/signup/', self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(self.base_url + 'auth/signup/', self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_signup_with_existing_email(self):
        response = self.client.post(self.base_url + 'auth/signup/', self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.data['username'] = 'anas2'
        response = self.client.post(self.base_url + 'auth/signup/', self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_signup_with_invalid_email(self):
        self.data['email'] = 'anasouhtrcg'
        response = self.client.post(self.base_url + 'auth/signup/', self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_signup_with_invalid_password(self):
        self.data['password'] = 'password'
        response = self.client.post(self.base_url + 'auth/signup/', self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_signup_with_invalid_username(self):
        self.data['username'] = 'a'
        response = self.client.post(self.base_url + 'auth/signup/', self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)