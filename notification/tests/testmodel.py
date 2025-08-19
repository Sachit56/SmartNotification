from django.test import TestCase
from notification.models import *

class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(username='testuser',email='testuser@gmail.com', password='testpass')

        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@gmail.com')
        
class ThreadModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@gmail.com', password='testpass')

    def test_thread(self):
        thread = Threads.objects.create(title='Test Thread',author=self.user)

        self.assertEqual(thread.title, 'Test Thread')
        self.assertEqual(thread.author, self.user)

    def test_unique_title(self):
        Threads.objects.create(title='Unique Thread', author=self.user)
        with self.assertRaises(Exception):
            Threads.objects.create(title='Unique Thread', author=self.user)
