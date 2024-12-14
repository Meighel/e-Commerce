import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from store.models import User, Order, CartItem


@pytest.fixture
def client():
    """Returns an API client instance."""
    return APIClient()


@pytest.fixture
def user(db):
    """Fixture for creating a test user."""
    return User.objects.create(
        name="Test User",
        email="testuser@example.com",
        address="123 Test St",
        phone="1234567890",
        password="testpassword123"
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
        status="Pending"
    )

@pytest.fixture
def unique_pending_order(db, user):
    """Fixture for creating a single pending order."""
    return Order.objects.create(user=user, status="Pending")

@pytest.fixture
def cart_item_data(order):
    """Fixture for cart item data."""
    return {
        "order": order.id,
        "product_name": "Test Product",
        "quantity": 2,
        "price": 19.99
    }


@pytest.fixture
def cart_item(db, order):
    """Fixture for creating a test cart item."""
    return CartItem.objects.create(
        order=order,
        product_name="Test Product",
        quantity=1,
        price=10.99
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
        "name": "New User",
        "email": "newuser@example.com",
        "address": "456 Another St",
        "phone": "9876543210",
        "password": "securepassword"
    }

    response = authenticated_client.post(url, data, format='json')

    assert response.status_code == 201
    assert response.data['name'] == data['name']
    assert response.data['email'] == data['email']
    assert response.data['address'] == data['address']
    assert response.data['phone'] == data['phone']
    assert response.data['password'] == data['password']

    created_user = User.objects.get(email=data['email'])
    assert created_user.name == data['name']
    assert created_user.email == data['email']
    assert created_user.password == data['password']


@pytest.mark.django_db
def test_get_user_detail(authenticated_client, user):
    """Test retrieving details of a specific user."""
    url = reverse('user-detail', kwargs={'user_id': str(user.id)}) 
    response = authenticated_client.get(url)
    assert response.status_code == 200
    assert response.data["name"] == user.name
    assert response.data["email"] == user.email


#ORDERS
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

    order.status = "Processed"
    order.save()

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
def test_checkout_order(authenticated_client, user, order):
    """Test checking out a specific order."""
    Order.objects.filter(user=user, status="Pending").update(status="Processed")

    pending_order = Order.objects.create(user=user, status="Pending")

    url = reverse('checkout', kwargs={"order_id": pending_order.id})
    response = authenticated_client.put(url)  # Use PUT instead of POST

    assert response.status_code == 200
    assert response.data["message"] == "Order processed successfully."



#CART ITEMS
@pytest.mark.django_db
def test_get_cart_items(authenticated_client, cart_item):
    """Test retrieving all cart items."""
    url = reverse('cart-item-list')
    response = authenticated_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_cart_item(authenticated_client, cart_item_data):
    """Test creating a cart item."""
    url = reverse('cart-item-list')
    response = authenticated_client.post(url, data=cart_item_data, format='json')
    assert response.status_code == 201
    assert CartItem.objects.filter(product_name=cart_item_data["product_name"]).exists()


@pytest.mark.django_db
def test_get_cart_item(authenticated_client, cart_item):
    """Test retrieving a specific cart item."""
    url = reverse('cart-item-detail', kwargs={'cart_item_id': cart_item.id})
    response = authenticated_client.get(url)
    assert response.status_code == 200
    assert response.data['id'] == str(cart_item.id)


@pytest.mark.django_db
def test_update_cart_item(authenticated_client, cart_item):
    """Test updating a specific cart item."""
    url = reverse('cart-item-detail', kwargs={'cart_item_id': cart_item.id})
    data = {"quantity": 5}
    response = authenticated_client.put(url, data, format='json')
    assert response.status_code == 200
    assert response.data['quantity'] == 5


@pytest.mark.django_db
def test_delete_cart_item(authenticated_client, cart_item):
    """Test deleting a specific cart item."""
    url = reverse('cart-item-detail', kwargs={'cart_item_id': cart_item.id})
    response = authenticated_client.delete(url)
    assert response.status_code == 200
    assert not CartItem.objects.filter(id=cart_item.id).exists()
