from django import forms
from django.forms import inlineformset_factory
from .models import ImageFile
from posts.models import Post
from django.forms import BaseInlineFormSet


class PostImageWidget(forms.ClearableFileInput):
    template_name = 'mediacore/widgets/post_image_field.html'


class ImageFileForm(forms.ModelForm):
    class Meta:
        model = ImageFile
        fields = ['file']
        widgets = {
            'file': PostImageWidget
        }


class ImageInlineFormSet(BaseInlineFormSet):
    deletion_widget = forms.CheckboxInput(
        attrs={"class": "add-image__del-btn checkbox__input hidden-input"})


ImageFileFormSet = inlineformset_factory(
    Post, ImageFile, form=ImageFileForm, formset=ImageInlineFormSet, extra=1)
