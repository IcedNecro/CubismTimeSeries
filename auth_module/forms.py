__author__ = 'roman'

from django import forms
from django.contrib.auth import models

class LoginForm(forms.Form):
    login = forms.CharField(label='Your Login', max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

class RegistrationForm(forms.Form):
    login = forms.CharField(label='Your Login', required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirmPassword = forms.CharField(widget=forms.PasswordInput, required=True)

    def is_valid(self):
        import ipdb; ipdb.set_trace()
        password = self.data.get('password')
        confirmPassword = self.data.get('confirmPassword')
        login = self.data.get('login')
        if password == confirmPassword:
            try:
                models.User.objects.get(username=login)
                return False
            except:
                return True
        else:
            return False