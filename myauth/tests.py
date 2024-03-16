from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status


class GenerateTokenTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_generate_token(self):
        url = reverse('token_obtain_pair')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIsInstance(response, Response)


class RefreshTokenTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.refresh_token = str(RefreshToken())

    def test_refresh_token_success(self):
        url = reverse('token_refresh')
        response = self.client.post(url, {'refresh_token': self.refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)
        self.assertIsInstance(response, Response)

    def test_refresh_token_invalid(self):
        url = reverse('token_refresh')
        response = self.client.post(url, {'refresh_token': 'invalid_token'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Invalid refresh token')

    def test_refresh_token_no_token_provided(self):
        url = reverse('token_refresh')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Refresh token not provided')
