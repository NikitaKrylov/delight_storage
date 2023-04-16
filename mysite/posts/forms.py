from django import forms
from .models import PostTag, Post


class PostTagsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for tag in PostTag.objects.all():
            self.fields[tag.slug] = forms.IntegerField(
                label=str(tag),
                widget=forms.NumberInput(
                    attrs={
                        "class": "tags-list__checkbox hidden-input three-pos-inp",
                        "value": 0,
                        "tabindex": -1,
                        "readonly": "",
                    }
                ),
            )
            self.fields[tag.slug].required = False


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            "only_for_adult",
            "for_autenticated_users",
            "disable_comments",
            "status",
            "description",
            "tags",
            "delayed_publication_time",
        )
        widgets = {
            "only_for_adult": forms.CheckboxInput(
                attrs={
                    "class": "checkbox__input hidden-input",
                }
            ),
            "for_autenticated_users": forms.CheckboxInput(
                attrs={
                    "class": "checkbox__input hidden-input",
                }
            ),
            "disable_comments": forms.CheckboxInput(
                attrs={
                    "class": "checkbox__input hidden-input",
                }
            ),
            "status": forms.RadioSelect(
                attrs={
                    "class": "status-post__input hidden-input",
                }
            ),
            "delayed_publication_time": forms.DateTimeInput(
                attrs={"class": "input-calendar", "type": "datetime-local"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "textarea__input textarea-autosize",
                    "placeholder": "Описание",
                    "cols": "20",
                    "rows": "2",
                }
            ),
            "tags": forms.CheckboxSelectMultiple(
                attrs={
                    "class": "tags-list__checkbox hidden-input three-pos-inp",
                    "tabindex": -1,
                    "data-state": 0,
                }
            ),
        }


class PostTagForm(forms.ModelForm):
    class Meta:
        model = PostTag
        fields = ("name",)
        widgets = {"name": forms.TextInput(attrs={"class": ""})}


class SearchForm(forms.Form):
    TYPE_CHOICES = (
        ("likes_amount", "Лайкам"),
        ("views_amount", "Просмотрам"),
        ("pub_date", "Дате"),
    )
    text = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "search__input-form input-form",
                "autocomplete": "off",
                "placeholder": "Поиск...",
            }
        ),
    )
    type = forms.ChoiceField(
        choices=TYPE_CHOICES,
        initial="pub_date",
        widget=forms.RadioSelect(attrs={"class": "search-sort__input hidden-input"}),
        required=False,
    )
    is_desc = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={"class": "hidden-input", "value": "-"}),
    )


class CreatePostTagForm(forms.ModelForm):
    class Meta:
        model = PostTag
        fields = ("name",)
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "input-user-tags input-form",
                    "placeholder": "Название",
                    "autocomplete": "off",
                }
            )
        }
