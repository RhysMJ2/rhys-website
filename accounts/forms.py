from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput(),
                            help_text="Required. You will have to verify this email before the account is activated")

    username = forms.CharField(max_length=15, required=True,
                               help_text="Required. 15 characters or less")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
