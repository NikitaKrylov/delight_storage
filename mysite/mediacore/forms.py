from django import forms
from django.forms import inlineformset_factory
from .models import ImageFile
from posts.models import Post


class ImageFileForm(forms.ModelForm):
    class Meta:
        model = ImageFile
        fields = ['file']

        widgets = {
            'file': forms.ClearableFileInput(attrs={'class': 'add-image__input', }),
            # 'file': forms.ClearableFileInput(attrs={}),
        }


ImageFileFormSet = inlineformset_factory(
    Post, ImageFile, form=ImageFileForm, extra=1)
