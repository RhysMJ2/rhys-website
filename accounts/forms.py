from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput(),
                            help_text="Required. You will have to verify this email before the account is activated")

    username = forms.CharField(max_length=15, required=True,
                               help_text="Required. 15 characters or less")

    def clean(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exists():
            raise ValidationError({'email': ["This email is already associated with an account.", ]})
        if User.objects.filter(username=username).exists():
            raise ValidationError({'username': ["Username already taken.", ]})
        return self.cleaned_data

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserUpdateForm(forms.ModelForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput(),
                            help_text="While we upgrade our systems you cannot change the email on the account ",
                            disabled=True)

    def clean(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError({'email': ["This email is already associated with an account.", ]})

        return self.cleaned_data

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)
