from django.test import TestCase
from store.models import User, Order, CartItem
from django.db.utils import IntegrityError

class UserModelTest(TestCase):
    def test_user_creation(self):
        user = User.objects.create(
            name="Test User",
            email="testuser@example.com",
        )
        self.assertEqual(user.name, "Test User")
        self.assertEqual(user.email, "testuser@example.com")

    def test_email_unique(self):
        User.objects.create(name="Test User 1", email="unique@example.com")
        with self.assertRaises(IntegrityError):
            User.objects.create(name="Test User 2", email="unique@example.com")

class OrderModelTest(TestCase):
    def test_order_creation(self):
        user = User.objects.create(name="Test User", email="testuser@example.com")
        order = Order.objects.create(user=user, status="Pending")
        self.assertEqual(order.status, "Pending")
        self.assertEqual(order.user, user)

    def test_unique_pending_order_per_user(self):
        user = User.objects.create(name="Test User", email="testuser@example.com")
        Order.objects.create(user=user, status="Pending")
        with self.assertRaises(ValueError):
            Order.objects.create(user=user, status="Pending")

class CartItemModelTest(TestCase):
    def test_cart_item_creation(self):
        user = User.objects.create(name="Test User", email="testuser@example.com")
        order = Order.objects.create(user=user, status="Processed")
        cart_item = CartItem.objects.create(order=order, product_name="Test Product", quantity=2, price=20.00)
        self.assertEqual(cart_item.product_name, "Test Product")
        self.assertEqual(cart_item.quantity, 2)
        self.assertEqual(cart_item.price, 20.00)
        self.assertEqual(cart_item.order, order)
