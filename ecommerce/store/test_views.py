from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from store.models import User
from django.test import TestCase
from django.contrib.auth.hashers import make_password
from unittest.mock import patch

class UserViewsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Manually hash the password using make_password
        hashed_password = make_password("password123")
        self.user = User.objects.create(
            name="Test User",
            email="testuser@example.com",
            password=hashed_password  # Store the hashed password
        )
        
        # Add 'is_authenticated' attribute for the user
        self.user.is_authenticated = True
        self.client.force_authenticate(user=self.user)

    def test_create_user(self):
        url = reverse('user-list-create')
        data = {
            "name": "New User",
            "email": "newuser@example.com",
            "password": "password123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], "newuser@example.com")

    def test_get_users(self):
        url = reverse('user-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_get_user_detail(self):
        url = reverse('user-detail', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)
