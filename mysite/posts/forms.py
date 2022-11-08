from django import forms
from .models import PostTag


class PostTagsForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tags = []

        for tag in PostTag.objects.all():
            self.fields["tag_{}".format(tag.slug)] = forms.IntegerField(
                label=tag.name,
                widget=forms.CheckboxInput(attrs={"class": ""})
            )

            self.tags.append("tag_{}".format(tag.slug))

