from django.db import models
from django import forms

class Entry(models.Model):
    title = models.CharField(max_length=50)
    post = models.TextField(max_length=2000)
    pub_date = models.DateTimeField('date published')
    
    def __unicode__(self):
        return self.title
    
class Comment(models.Model):
    entry = models.ForeignKey(Entry)
    text = models.CharField(max_length=50)
    pub_date = models.DateTimeField('date published')
    
    def __unicode__(self):
        return self.text
