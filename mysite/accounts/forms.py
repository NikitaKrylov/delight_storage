from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.core.exceptions import ValidationError

from .models import User, PostComplaint, Folder
from posts.models import PostTag
from mediacore.forms import ClearableAvatarFileInput
from django.utils.translation import gettext_lazy as _


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(
        label="username",
        min_length=5,
        max_length=150,
        widget=forms.TextInput(
            attrs={"autocomplete": "off", "class": "reg-menu__input"}
        ),
    )
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={"autocomplete": "email", "class": "reg-menu__input"}
        )
    )
    password1 = forms.CharField(
        label="password",
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "reg-menu__input"}
        ),
    )
    password2 = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.pop("autofocus", None)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )

    def clean_username(self):
        data = self.cleaned_data["username"]
        if User.objects.filter(username=data).exists():
            raise ValidationError(_("Пользователь с таким именем уже существует"))
        return data

    def clean_email(self):
        data = self.cleaned_data["email"]
        if User.objects.filter(email=data).exists():
            raise ValidationError(_("Пользователь с такой почтой уже существует"))
        return data

    def save(self, commit=True):
        user = super(RegisterUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = True

        if commit:
            user.save()
        return user


class AuthenticationUserForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"autocomplete": "off", "class": "reg-menu__input"}
        )
    )
    password = forms.CharField(
        label="password",
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "reg-menu__input"}
        ),
    )

    class Meta:
        model = User


# ------------------- User Page ----------------------


class EditUserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "username",
            "avatar",
            "email",
            "birth_date",
        )
        widgets = {
            "avatar": ClearableAvatarFileInput(
                attrs={
                    "class": "input-file__input hidden-input",
                    "id": "input-file__input",
                }
            ),
            "birth_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "autocomplete": "off",
                    "style": "max-width: 232px; padding-right: 30px;",
                }
            ),
            "username": forms.TextInput(),
            "email": forms.EmailInput(),
        }


class UserFolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = (
            "icon",
            "name",
            "is_private",
            "description",
        )
        widgets = {
            "icon": forms.FileInput(
                attrs={
                    "class": "input-file__input hidden-input",
                    "id": "input-file__input",
                }
            ),
            "name": forms.TextInput(attrs={"placeholder": "Имя папки", "class": ""}),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Описание",
                    "class": "textarea__input",
                    "cols": 20,
                    "rows": 2,
                }
            ),
            "is_private": forms.CheckboxInput(
                attrs={"class": "hidden-input checkbox__input"}
            ),
        }


# ---------------------- Password ----------------------------


class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(
            attrs={"autocomplete": "email", "class": "reg-menu__input"}
        ),
    )


class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "reg-menu__input"}
        ),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="New password confirmation",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "reg-menu__input"}
        ),
    )


# ------------------------------ Complaint ----------------------------------


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = PostComplaint
        fields = (
            "type",
            "description",
        )
        widgets = {
            "type": forms.RadioSelect(),
            "description": forms.Textarea(
                attrs={
                    "class": "textarea__input",
                    "placeholder": "Опишите подробнее",
                    "cols": 20,
                    "rows": 2,
                }
            ),
        }
