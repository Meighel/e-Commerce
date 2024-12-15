import os
import pytest
import django
from django.db.utils import IntegrityError
from store.models import User, Order, CartItem


@pytest.mark.django_db
def test_user_creation():
    user = User.objects.create(
        name="Test User",
        email="testuser@example.com",
        address = "Manila, Philippines",
        phone = "09246387490", 
        password = "testerpassword", 

    )
    assert user.name == "Test User"
    assert user.email == "testuser@example.com"
    assert user.address == "Manila, Philippines"
    assert user.phone == "09246387490" 
    assert user.password == "testerpassword" 


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
def test_unique_pending_order_per_user_edge_case():
    user = User.objects.create(name="Test User", email="testuser@example.com")
    
    first_order = Order.objects.create(user=user, status="Pending")
    
    with pytest.raises(IntegrityError): 
        Order.objects.create(user=user, status="Pending")

    with pytest.raises(ValueError, match="User can only have one pending order"):
        if Order.objects.filter(user=user, status="Pending").exists():
            raise ValueError("User can only have one pending order")
        else:
            Order.objects.create(user=user, status="Pending")

    from threading import Thread

    def create_order():
        Order.objects.create(user=user, status="Pending")

    thread1 = Thread(target=create_order)
    thread2 = Thread(target=create_order)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    assert Order.objects.filter(user=user, status="Pending").count() == 1

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