from django import forms
from .models import PostTag


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
