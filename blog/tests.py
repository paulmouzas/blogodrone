from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from blog.models import Entry


class BlogTest(TestCase):

    def test_blog_entry_belongs_to_correct_user(self):
        me = User.objects.create_user('paul', 'paul.mouzas@gmail.com',
                                      'foobar')
        wrong_user = User.objects.create_user('foobar', 'foobar@example.com',
                                              'foobar')
        entry = Entry(author=me, title='My post', post='Here is my post',
                      pub_date=timezone.now())
        self.assertEqual(me, entry.author)
        self.assertNotEqual(wrong_user, entry.author)
