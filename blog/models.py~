from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class Entry(models.Model):
    author = models.ForeignKey(User, blank=True)
    title = models.CharField(max_length=50)
    post = models.TextField(max_length=2000)
    pub_date = models.DateTimeField('date published')
    
    def __unicode__(self):
        return self.title
    
class Comment(models.Model):
    author = models.ForeignKey(User, blank=True)
    entry = models.ForeignKey(Entry)
    text = models.CharField(max_length=50)
    pub_date = models.DateTimeField('date published')
    
    def __unicode__(self):
        return self.text
        
class LoginForm(forms.Form):
    username = forms.CharField(max_length=25, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        return self.cleaned_data
        
    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user
    
class SignupForm(forms.Form):
    username = forms.CharField(max_length=25)
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
class PostForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['title', 'post']