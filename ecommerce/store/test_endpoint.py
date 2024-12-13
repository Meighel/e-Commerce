import pytest
from rest_framework.test import APIClient
from django.contrib.auth.hashers import make_password, check_password
from django.urls import reverse
from store.models import User


@pytest.fixture
def client():
    """Returns an API client instance."""
    return APIClient()


@pytest.fixture
def user(db):
    """Fixture for creating a test user."""
    return User.objects.create(
        name="testuser",
        email="testuser@example.com",
        password="password123"
    )


@pytest.fixture
def authenticated_client(client, user):
    """Fixture for an authenticated client."""
    user.is_authenticated = True 
    client.force_authenticate(user=user)
    return client


@pytest.mark.django_db
def test_user_list(authenticated_client):
    """Test retrieving the list of users."""
    url = reverse('user-list-create')  
    response = authenticated_client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_post_user(authenticated_client):
    """Test creating a new user."""
    url = reverse('user-list-create') 
    data = {
        "name": "newuser",
        "email": "newuser@example.com",
        "password": "newpassword123"
    }

    response = authenticated_client.post(url, data, format='json')

    # Assert the response status code
    assert response.status_code == 201

    # Verify the created user's data in the response
    assert response.data['name'] == data['name']
    assert response.data['email'] == data['email']

    # Verify the user is created in the database
    created_user = User.objects.get(email=data['email'])
    assert created_user.name == data['name']
    assert created_user.email == data['email']

    # Verify that the password matches directly (not hashed)
    assert created_user.password == data['password']



@pytest.mark.django_db
def test_get_user_detail(authenticated_client, user):
    """Test retrieving details of a specific user."""
    url = reverse('user-detail', kwargs={'user_id': str(user.id)})  # Use 'user_id' instead of 'pk'
    response = authenticated_client.get(url)
    assert response.status_code == 200
    assert response.data["name"] == user.name
    assert response.data["email"] == user.email
