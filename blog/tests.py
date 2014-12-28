from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.utils import timezone
from blog.models import Entry, UserProfile


class UserTestCase(TestCase):
    def setUp(self):
        self.u1 = User.objects.create_user(username="user1",
                                           email="user1@example.com",
                                           password="foobar")

        self.e1 = Entry.objects.create(author=self.u1,
                                       title="testing",
                                       post="this is a post",
                                       pub_date=timezone.now())

        self.u1_profile = UserProfile(user=self.u1, about="about me")

    def test_author(self):
        self.assertEqual(self.u1.username, "user1")
        self.assertEqual(self.e1.author, self.u1)

    def test_is_authenticate(self):
        self.assertTrue(self.u1.is_authenticated())

    def test_user_profile(self):
        self.assertEqual(self.u1, self.u1_profile.user)
        self.assertEqual(self.u1_profile.about, "about me")

    def tearDown(self):
        self.u1.delete()
        self.e1.delete()


class FormsTestCase(TestCase):
    def setUp(self):
        c = Client()
        c.post('/blog/signup/', {'username': 'user2',
                                 'email': 'user2@example.com',
                                 'password': 'foobar'})
        c.login(username='user2', password='foobar')
        c.post('/blog/user/update_about/', {'about': 'about user2'})

    def test_signup_form(self):
        self.assertTrue(User.objects.get(username='user2'))

    def test_about_form(self):
        user = User.objects.get(username='user2')
        self.assertEqual(UserProfile.objects.get(user=user.id).about,
                         'about user2')
