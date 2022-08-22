from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='username', min_length=5, max_length=150,
                               widget=forms.TextInput(attrs={'placeholder': 'Login'}))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(label='password', widget=forms.PasswordInput(
        attrs={"autocomplete": "new-password", 'placeholder': 'Password'}))
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
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Login or Email'}))
    password = forms.CharField(label='password', widget=forms.PasswordInput(
        attrs={"autocomplete": "new-password", 'placeholder': 'Password'}))

    class Meta:
        model = User
