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
                    attrs={"class": "tags-list__checkbox hidden-checkbox three-pos-inp", "value": 0, "tabindex": -1, "readonly": "", }),
            )
            self.fields[tag.slug].required = False


class CreatePostDelayForm(forms.ModelForm):

    class Meta:
        model = PostDelay
        fields = ('time',)
        widgets = {
            'time': forms.DateTimeInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['time'].required = False

    def is_valid(self):
        if not self.data['time']:
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
