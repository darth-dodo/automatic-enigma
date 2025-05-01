from django.test import TestCase
from .models import User

class UserTestCase(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(username="testuser", password="testpass")
        self.assertEqual(str(user), "testuser")
