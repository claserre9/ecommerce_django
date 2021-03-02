from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    fisrt_name = forms.CharField(min_length=4, max_length=100, required=True)
    last_name = forms.CharField(min_length=4, max_length=100, required=True)
    email = forms.EmailField(max_length=250, required=True)
    field_order = ('username', 'email', 'fisrt_name', 'last_name',  'password1', 'password2',)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)

