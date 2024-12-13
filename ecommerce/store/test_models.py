import os
import pytest

from django.db.utils import IntegrityError
from store.models import User, Order, CartItem


@pytest.mark.django_db
def test_user_creation():
    user = User.objects.create(
        name="Test User",
        email="testuser@example.com",
    )
    assert user.name == "Test User"
    assert user.email == "testuser@example.com"


@pytest.mark.django_db
def test_email_unique():
    User.objects.create(name="Test User 1", email="unique@example.com")
    with pytest.raises(IntegrityError):
        User.objects.create(name="Test User 2", email="unique@example.com")


@pytest.mark.django_db
def test_order_creation():
    user = User.objects.create(name="Test User", email="testuser@example.com")
    order = Order.objects.create(user=user, status="Pending")
    assert order.status == "Pending"
    assert order.user == user


@pytest.mark.django_db
def test_unique_pending_order_per_user():
    user = User.objects.create(name="Test User", email="testuser@example.com")
    Order.objects.create(user=user, status="Pending")
    with pytest.raises(ValueError):
        Order.objects.create(user=user, status="Pending")


@pytest.mark.django_db
def test_cart_item_creation():
    user = User.objects.create(name="Test User", email="testuser@example.com")
    order = Order.objects.create(user=user, status="Processed")
    cart_item = CartItem.objects.create(
        order=order, product_name="Test Product", quantity=2, price=20.00
    )
    assert cart_item.product_name == "Test Product"
    assert cart_item.quantity == 2
    assert cart_item.price == 20.00
    assert cart_item.order == order

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'ecommerce.settings'
    pytest.main()