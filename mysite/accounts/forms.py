from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, SetPasswordForm
from .models import User
from posts.models import PostTag
from posts.models import Post


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='username', min_length=5, max_length=150,
                               widget=forms.TextInput(attrs={'class': 'reg-menu__input'}))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={"autocomplete": "email", 'class': 'reg-menu__input'}))
    password1 = forms.CharField(label='password', widget=forms.PasswordInput(
        attrs={"autocomplete": "new-password", 'class': 'reg-menu__input'}))
    password2 = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.pop('autofocus', None)

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
        attrs={'class': 'reg-menu__input'}))
    password = forms.CharField(label='password', widget=forms.PasswordInput(
        attrs={"autocomplete": "new-password", 'class': 'reg-menu__input'}))

    class Meta:
        model = User

# ------------------- User Page ----------------------


class EditUserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'username',
            'avatar',
            'email',
            'birth_date',
        )
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class': 'input-file__input hidden-input', 'id': 'input-file__input'}),
            'birth_date': forms.DateInput(),
            'username': forms.TextInput(),
            'email': forms.EmailInput(),
        }


class UserSettingsForm(forms.Form):
    ignored_tags = forms.ModelMultipleChoiceField(
        queryset=PostTag.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )

    def __init__(self, *args, user: User, **kwargs):
        super().__init__(*args, **kwargs)
        initial = []

        for i, choice in enumerate(self.fields['ignored_tags'].choices):
            if user.ignored_tags.filter(name=choice[1]).exists():
                initial.append(i+1)

        self.fields['ignored_tags'].initial = initial


# ---------------------- Password ----------------------------

class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email", 'class': 'reg-menu__input'}))


class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", 'class': 'reg-menu__input'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="New password confirmation",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", 'class': 'reg-menu__input'}),
    )
