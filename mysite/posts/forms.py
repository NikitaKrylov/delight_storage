from django import forms
from accounts.models import User
from .models import Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
        # widgets = {}
