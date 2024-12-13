import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from store.models import User, Order


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


@pytest.fixture
def order(db, user):
    """Fixture for creating a test order."""
    return Order.objects.create(
        user=user,
        status="pending"
    )

#USERS
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

    assert response.status_code == 201
    assert response.data['name'] == data['name']
    assert response.data['email'] == data['email']

    created_user = User.objects.get(email=data['email'])
    assert created_user.name == data['name']
    assert created_user.email == data['email']
    assert created_user.password == data['password']


#ORDERS
@pytest.mark.django_db
def test_get_user_detail(authenticated_client, user):
    """Test retrieving details of a specific user."""
    url = reverse('user-detail', kwargs={'user_id': str(user.id)}) 
    response = authenticated_client.get(url)
    assert response.status_code == 200
    assert response.data["name"] == user.name
    assert response.data["email"] == user.email


@pytest.mark.django_db
def test_get_orders(authenticated_client):
    """Test retrieving all orders."""
    url = reverse('order-list-create') 
    response = authenticated_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_post_order(authenticated_client, user):
    """Test creating a new order."""
    url = reverse('order-list-create') 
    data = {
        "user": user.id,
        "status": "Pending",
    }
    response = authenticated_client.post(url, data, format='json')
    assert response.status_code == 201
    assert response.data["status"] == data["status"]


@pytest.mark.django_db
def test_delete_orders(authenticated_client):
    """Test deleting all orders (if supported)."""
    url = reverse('order-list-create') 
    response = authenticated_client.delete(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_order_detail(authenticated_client, order):
    """Test retrieving a specific order by ID."""
    url = reverse('order-detail', kwargs={"order_id": order.id}) 
    response = authenticated_client.get(url)
    assert response.status_code == 200
    assert response.data["id"] == str(order.id)


@pytest.mark.django_db
def test_put_order(authenticated_client, order):
    """Test updating a specific order."""
    url = reverse('order-detail', kwargs={"order_id": order.id}) 
    data = {
        "status": "Pending",
    }
    response = authenticated_client.put(url, data, format='json')
    assert response.status_code == 200
    assert response.data["status"] == data["status"]


@pytest.mark.django_db 
def test_delete_order(authenticated_client, order):
    """Test deleting a specific order by ID."""
    url = reverse('order-detail', kwargs={"order_id": order.id})
    response = authenticated_client.delete(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_checkout_order(authenticated_client, order):
    """Test checking out a specific order."""       
    order.status = 'Pending'
    order.save()

    url = reverse('checkout', kwargs={"order_id": order.id})
    response = authenticated_client.put(url, format='json')
    assert response.status_code == 200
    assert response.data["message"] == "Order processed successfully."

