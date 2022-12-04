from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, SetPasswordForm
from .models import User


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='username', min_length=5, max_length=150,
                               widget=forms.TextInput(attrs={'autofocus': 'autofocus', 'placeholder': 'Никнейм', 'class': 'reg-form__input'}))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': 'Email', 'class': 'reg-form__input'}))
    password1 = forms.CharField(label='password', widget=forms.PasswordInput(
        attrs={"autocomplete": "new-password", 'placeholder': 'Пароль', 'class': 'reg-form__input'}))
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
        user.is_active = True

        if commit:
            user.save()
        return user


class AuthenticationUserForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'autofocus': 'autofocus', 'placeholder': 'Никнейм или email', 'class': 'reg-form__input'}))
    password = forms.CharField(label='password', widget=forms.PasswordInput(
        attrs={"autocomplete": "new-password", 'placeholder': 'Пароль', 'class': 'reg-form__input'}))

    class Meta:
        model = User


class EditUserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'username',
            'avatar',
            'email',
            'birth_date',
        )
        # widgets = {}


class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email", 'placeholder': 'Email', 'class': 'reg-form__input'}))


class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", 'placeholder': 'Новый пароль', 'class': 'reg-form__input'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="New password confirmation",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", 'placeholder': 'Подтверждение пароля', 'class': 'reg-form__input'}),
    )
