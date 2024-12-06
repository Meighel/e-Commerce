from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient
from store.models import User  # Adjust import based on your app's models

class UserAuthenticationTest(TestCase):
    
    def setUp(self):
        # Create a user to use for valid authentication tests
        self.user = User.objects.create_user(username='testuser', password='password123')

        # Set up the API client
        self.client = APIClient()

        # Define your protected URL (adjust to the specific view you want to test)
        self.url = reverse('user-list')  # Adjust to the actual URL name

    def test_unauthorized_access_without_credentials(self):
        # Test that trying to access the protected resource without credentials returns 401
        response = self.client.get(self.url)  # Make a GET request without any authentication
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # Check for 401 Unauthorized

    def test_unauthorized_access_with_invalid_credentials(self):
        # Test that providing invalid credentials returns 401
        self.client.credentials(HTTP_AUTHORIZATION='Basic invalid_token')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # Check for 401 Unauthorized

    def test_authorized_access_with_valid_credentials(self):
        # Log in with valid credentials
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Should be OK if credentials are valid
