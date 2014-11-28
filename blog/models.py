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
    username = forms.CharField(max_length=25, required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), required=True)
    
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
    
class SignupForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    username = forms.CharField(required=True, max_length=25, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'class':'form-control'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        return self.cleaned_data
    
class PostForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['title', 'post']
    title = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    post = forms.CharField(max_length=2000, required=True, widget=forms.Textarea(attrs={'class':'form-control'}))

    def clean(self):
        title = self.cleaned_data.get('title')
        post = self.cleaned_data.get('post')
        return self.cleaned_data

class UpdateProfile(forms.ModelForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
        return email

    def save(self, commit=True):
        user = User.objects.get(username=username)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user
        
