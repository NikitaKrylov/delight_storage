from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='username', min_length=5, max_length=150)
    email = forms.EmailField()
    password1 = forms.CharField(label='password', widget=forms.PasswordInput(
        attrs={"autocomplete": "new-password"}))
    password2 = None

    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )
        # widgets = {}

    def save(self, commit=True):
        user = super(RegisterUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class AuthenticationUserForm(AuthenticationForm):
    class Meta:
        model = User
