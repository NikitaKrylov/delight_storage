from django import forms
from .models import PostTag

ORDER_TYPES = (
    (0, 'Просмотрам'),
    (1, 'Лайкам'),
    (2, 'Новинкам'),
    (3, 'Лучшее'),
)


class PostFilterForm(forms.Form):
    only_for_adult = forms.BooleanField(label="18+")
    order_type = forms.ChoiceField(choices=ORDER_TYPES, widget=forms.RadioSelect(attrs={}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tags = []

        for tag in PostTag.objects.all():
            self.fields["tag_{}".format(tag.slug)] = forms.IntegerField(min_value=0, max_value=2, default=0)
            self.tags.append("tag_{}".format(tag.slug))

