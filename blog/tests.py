from django.test import TestCase

from blog.models import Entry

class EntryTestCase(TestCase):
    def setUp(self):
        self.u1 = User.objects.create(username="user1")
        self.e1 = Entry.objects.create(author=self.u1, title="testing", 
                                       post="this is a post", pub_date=datetime.now())

    def testA(self):
        self.assertEqual(self.u1.username, "user1")
        self.assertEqual(self.e1.author, self.u1) 

    def tearDown(self):
        self.u1.delete()
        self.e1.delete()
