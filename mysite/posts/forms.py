from django import forms
from django.core.exceptions import ValidationError
from django.forms import modelform_factory

from .models import PostTag, PostDelay, Post


class PostTagsForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for tag in PostTag.objects.all():
            self.fields[tag.slug] = forms.IntegerField(
                label=str(tag),
                widget=forms.NumberInput(
                    attrs={"class": "tags-list__checkbox hidden-input three-pos-inp", "value": 0, "tabindex": -1, "readonly": "", }),
            )
            self.fields[tag.slug].required = False


class CreatePostDelayForm(forms.ModelForm):

    class Meta:
        model = PostDelay
        fields = ('time',)
        widgets = {
            'time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['time'].required = False

    def is_valid(self):
        if not self.data['time'] or self.data['time'] is None:
            return False
        return super().is_valid()


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = (
            'only_for_adult',
            'for_autenticated_users',
            'disable_comments',
            'status',
            'description',
            'tags',
        )
        widgets = {
            'only_for_adult': forms.CheckboxInput(attrs={'class': 'checkbox__input hidden-input', }),
            'for_autenticated_users': forms.CheckboxInput(attrs={'class': 'checkbox__input hidden-input', }),
            'disable_comments': forms.CheckboxInput(attrs={'class': 'checkbox__input hidden-input', }),
            'description': forms.Textarea(attrs={'class': 'textarea__input textarea-autosize', 'placeholder': 'Придумайте описание', 'cols': '20', 'rows': '2', }),
            'tags': forms.CheckboxSelectMultiple(attrs={"class": "tags-list__checkbox hidden-input three-pos-inp", "tabindex": -1, "data-state": 0, }),
        }
