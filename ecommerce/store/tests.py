from django.test import TestCase
from store.models import User

class UserModelTest(TestCase):
    def setUp(self):
        # Create a sample user for testing
        self.user = User.objects.create(
            name="Test User",
            email="test@example.com",
            address="123 Test Lane",
            phone="123-456-7890"
        )

    def test_user_creation(self):
        # Test that the user is created correctly
        self.assertEqual(self.user.name, "Test User")
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(self.user.address, "123 Test Lane")
        self.assertEqual(self.user.phone, "123-456-7890")

    def test_str_method(self):
        # Test the __str__ method of the User model
        self.assertEqual(str(self.user), "Test User")
