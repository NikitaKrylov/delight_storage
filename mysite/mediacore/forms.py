from django import forms
from django.forms import inlineformset_factory
from .models import ImageFile
from posts.models import Post


class ImageFileForm(forms.ModelForm):
    class Meta:
        model = ImageFile
        fields = ['file']


ImageFileFormSet = inlineformset_factory(Post, ImageFile, form=ImageFileForm, extra=1)
