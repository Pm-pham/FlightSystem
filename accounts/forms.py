from django import forms
from django.forms import ModelForm
from .models import Account, Register

# create form
class RegisterForm(ModelForm):
    class Meta:
        model = Register
        fields = ['username','email', 'password']

class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ['username','password']