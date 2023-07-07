from django import forms
from django.forms import inlineformset_factory
from .models import ImageFile, VideoFile
from posts.models import Post
from django.forms import BaseInlineFormSet


class ClearableFileInput(forms.ClearableFileInput):
    template_name = "mediacore/widgets/post_image_field.html"


class ClearableAvatarFileInput(forms.ClearableFileInput):
    template_name = "mediacore/widgets/account_image_field.html"


class ImageFileForm(forms.ModelForm):
    class Meta:
        model = ImageFile
        fields = ["file"]
        widgets = {"file": ClearableFileInput}


class ImageInlineFormSet(BaseInlineFormSet):
    deletion_widget = forms.CheckboxInput(
        attrs={"class": "add-file__del-btn checkbox__input hidden-input"}
    )


ImageFileFormSet = inlineformset_factory(
    Post, ImageFile, form=ImageFileForm, formset=ImageInlineFormSet, extra=1
)


class VideoFileForm(forms.ModelForm):
    class Meta:
        model = VideoFile
        fields = ["file"]
        widgets = {"file": ClearableFileInput, "": None}


class VideoInlineFormSet(BaseInlineFormSet):
    deletion_widget = forms.CheckboxInput(
        attrs={"class": "add-file__del-btn checkbox__input hidden-input"}
    )


VideoFileFormSet = inlineformset_factory(
    Post, VideoFile, form=VideoFileForm, formset=VideoInlineFormSet, extra=1
)
