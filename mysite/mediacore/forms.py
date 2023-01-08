from django import forms
from django.forms import inlineformset_factory
from .models import ImageFile
from posts.models import Post


class PostImageWidget(forms.ClearableFileInput):
    template_name = 'mediacore/widgets/post_image_field.html'


class ImageFileForm(forms.ModelForm):
    class Meta:
        model = ImageFile
        fields = ['file']
        widgets = {
            'file': PostImageWidget()
        }


ImageFileFormSet = inlineformset_factory(
    Post, ImageFile, form=ImageFileForm, extra=1)
