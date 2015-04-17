from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class Entry(models.Model):
    author = models.ForeignKey(User, blank=True)
    title = models.CharField(max_length=50)
    post = models.TextField(max_length=2000)
    pub_date = models.DateTimeField('date published')

    @classmethod
    def get_dates(cls):
        seen = set()
        unique_datetimes = []
        entries_list = cls.objects.all().order_by('-pub_date')
        seq = [e.pub_date for e in entries_list]
        for date in seq:
            if (date.month, date.year) not in seen:
                unique_datetimes.append(date)
                seen.add((date.month, date.year))
        return unique_datetimes


    def __unicode__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User, blank=True)
    entry = models.ForeignKey(Entry)
    text = models.TextField(max_length=2000)
    pub_date = models.DateTimeField('date published')

    def __unicode__(self):
        return self.text


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    about = models.TextField(max_length=2000)

    def get_absolute_url(self):
        return reverse('blog.views.user_profile', args=[str(self.user.username)])
