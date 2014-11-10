from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from models import SignupForm, Entry

from blog.models import Entry

class EntryTestCase(TestCase):
    def setUp(self):
        self.u1 = User.objects.create_user(username="user1", email="user1@example.com", password="foobar")
        self.e1 = Entry.objects.create(author=self.u1, title="testing", 
                                       post="this is a post", pub_date=timezone.now())

    def testA(self):
        self.assertEqual(self.u1.username, "user1")
        self.assertEqual(self.e1.author, self.u1) 

    def tearDown(self):
        self.u1.delete()
        self.e1.delete()
